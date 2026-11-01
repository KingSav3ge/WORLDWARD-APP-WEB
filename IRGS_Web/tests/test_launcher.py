"""Synthetic selected-build launcher fixtures; never overrides script policy.

Run only in an already permitted environment with an explicitly admitted launcher
fixture run. A policy denial stops admission before HTTP fixtures and is not
retried. Portable PowerShell checks do not establish native Windows qualification.
"""
import copy
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'IRGS_Web'))
from engine_paths import ENGINE_ROOT

CANONICAL = ENGINE_ROOT / 'Start-IRGS-3.3.ps1'
WEB = ROOT / 'IRGS_Web' / 'Start-IRGS.ps1'
POWERSHELL = shutil.which('powershell.exe') or shutil.which('pwsh')
PERMITTED = os.environ.get('IRGS_LAUNCHER_TEST_POLICY_ALLOWED') == '1'
HASH_FIELDS = ('app_manifest_sha256', 'host_source_sha256', 'engine_manifest_sha256',
               'engine_core_sha256', 'catalog_manifest_sha256', 'catalog_portfolio_sha256')
USE_SELECTED = object()
OMIT_BUILD = object()
SESSION_TOKEN = 'synthetic-local-session-token'


def ps_quote(value):
    return "'" + str(value).replace("'", "''") + "'"


def policy_denied(result):
    message = (result.stdout + result.stderr).casefold()
    return (any(marker in message for marker in
                ('pssecurityexception', 'running scripts is disabled',
                 'execution of scripts is disabled', 'is not digitally signed',
                 'authorizationmanager check failed'))
            or ('cannot be loaded because' in message and 'execution policy' in message))


@unittest.skipUnless(POWERSHELL and PERMITTED,
                     'Requires PowerShell and explicitly admitted ordinary script execution; no policy override')
class LauncherTests(unittest.TestCase):
    policy_block = None

    @classmethod
    def setUpClass(cls):
        # One ordinary dot-source admission, before starting any HTTP fixture.
        # Do not set the opt-in or fall back to copied/inline launcher source.
        command = ("$ErrorActionPreference='Stop'; . " + ps_quote(CANONICAL)
                   + "; if (-not (Get-Command Test-IrgsBuildIdentity -CommandType Function "
                   + "-ErrorAction SilentlyContinue)) { throw 'Select the paired Engine "
                   + "6b88eb6f9006b3fa4927401cc21734f73c2dfd57 through IRGS_ENGINE_ROOT; "
                   + "the build-identity launcher contract is required.' }; "
                   + "Write-Output 'IRGS-APP-LAUNCHER-ADMITTED'")
        result = subprocess.run([POWERSHELL, '-NoProfile', '-NonInteractive', '-Command', command],
                                capture_output=True, text=True, timeout=20)
        if policy_denied(result):
            cls.policy_block = 'Ordinary launcher script denied by execution policy before HTTP; no override or retry'
            raise unittest.SkipTest(cls.policy_block)
        if result.returncode != 0 or 'IRGS-APP-LAUNCHER-ADMITTED' not in result.stdout:
            raise AssertionError('Launcher fixture admission failed: ' + result.stdout + result.stderr)

    def setUp(self):
        if type(self).policy_block:
            self.skipTest(type(self).policy_block)
        # The real App startup identity, with the normally selected dependency
        # roots. No copied constant or invented component fingerprint is reused.
        from build_identity import running_build
        self.expected = running_build()
        self.assertEqual(self.expected['schema_version'], 1)
        self.assertRegex(self.expected['edition'] or '', r'^\d+\.\d+\.\d+$')
        self.assertEqual(self.expected['classification'],
                         'pre_alpha' if self.expected['edition'].startswith('3.') else 'unclassified')
        for field in HASH_FIELDS:
            self.assertTrue(re.fullmatch(r'[0-9a-f]{64}', self.expected[field] or ''), field)

    def powershell(self, command, *, timeout=25, env=None):
        if type(self).policy_block:
            self.skipTest(type(self).policy_block)
        result = subprocess.run([POWERSHELL, '-NoProfile', '-NonInteractive', '-Command',
                                 "$ErrorActionPreference='Stop'; " + command],
                                capture_output=True, text=True, timeout=timeout, env=env)
        if policy_denied(result):
            type(self).policy_block = 'Ordinary launcher script denied by execution policy; remaining probes skipped without retry'
            self.skipTest(type(self).policy_block)
        return result

    def fixture(self, *, valid=False, session=True, build=USE_SELECTED):
        paths = []
        snapshot = self.expected if build is USE_SELECTED else build
        state = {'valid': valid, 'session': session,
                 'build': OMIT_BUILD if snapshot is OMIT_BUILD else copy.deepcopy(snapshot)}

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                paths.append(self.path)
                if self.path == '/api/catalog' and state['valid']:
                    data = {'core': {'id': 'IRGS-CORE-3.3', 'version': '3.3',
                                     'single_world_per_campaign': True}}
                elif self.path == '/api/campaigns' and state['session']:
                    data = {'campaigns': [], 'token': SESSION_TOKEN}
                    if state['build'] is not OMIT_BUILD:
                        data['build'] = state['build']
                else:
                    data = {'message': 'Unrelated listener; no IRGS host health'}
                raw = json.dumps(data).encode()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)

            def do_POST(self):
                paths.append('POST ' + self.path)
                self.send_error(405)

            def log_message(self, *args):
                pass

        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(server.server_close)
        self.addCleanup(thread.join)
        self.addCleanup(server.shutdown)
        return server, paths, state

    def probe(self, port, *, expected=USE_SELECTED):
        selected = self.expected if expected is USE_SELECTED else expected
        command = ('. ' + ps_quote(CANONICAL) + '; $expected = '
                   + ps_quote(json.dumps(selected, separators=(',', ':')))
                   + ' | ConvertFrom-Json; Get-IrgsHostState -HostPort ' + str(port)
                   + ' -ExpectedBuild $expected')
        result = self.powershell(command)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result.stdout.strip()

    def selected_start(self, port, profile):
        # This fixture isolates the reuse/occupied-port decision. Selected-build
        # calculation and release verification have their own Engine tests.
        # The sentinel satisfies the launcher's existence check and is NEVER
        # executed. No real host or browser may start, and no process may stop.
        bundled = profile / '.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
        bundled.parent.mkdir(parents=True, exist_ok=True)
        bundled.write_bytes(b'fixture sentinel; never executed')
        command = ('. ' + ps_quote(CANONICAL) + ' -AppRoot ' + ps_quote(WEB.parent)
                   + '; $fixtureExpected = ' + ps_quote(json.dumps(self.expected))
                   + ' | ConvertFrom-Json; '
                   + 'function Get-IrgsExpectedBuild { return $fixtureExpected }; '
                   + 'function Confirm-IrgsRelease {}; '
                   + "function Start-Process { throw 'Unexpected host or browser launch' }; "
                   + "function Stop-Process { throw 'Unexpected listener termination' }; "
                   + 'try { Start-IrgsWebsite -HostPort ' + str(port)
                   + ' -OpenBrowser $false -WaitSeconds 2; exit 0 } '
                   + 'catch { Write-Output $_.Exception.Message; exit 1 }')
        # Child-only synthetic profile; no policy/permission setting is changed.
        return self.powershell(command, env={**os.environ, 'USERPROFILE': str(profile)})

    def assert_listener_preserved(self, server):
        with urlopen('http://127.0.0.1:' + str(server.server_port) + '/api/campaigns', timeout=3) as response:
            self.assertEqual(json.load(response)['token'], SESSION_TOKEN)

    def test_powershell_entrypoints_parse(self):
        for path in (CANONICAL, WEB):
            with self.subTest(path=path):
                result = self.powershell(
                    "$t=$null;$e=$null;[System.Management.Automation.Language.Parser]::ParseFile("
                    + ps_quote(path) + ",[ref]$t,[ref]$e)|Out-Null;if($e.Count){$e|Out-String;exit 1}")
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_complete_selected_health_is_ready_and_uses_only_read_routes(self):
        server, paths, _ = self.fixture(valid=True)
        self.assertEqual(self.probe(server.server_port), 'Ready')
        self.assertEqual(paths, ['/api/catalog', '/api/campaigns'])

    def test_unrelated_http_listener_is_occupied_not_reused(self):
        server, paths, _ = self.fixture()
        self.assertEqual(self.probe(server.server_port), 'Occupied')
        self.assertEqual(paths, ['/api/catalog'])

    def test_catalog_without_session_health_is_occupied(self):
        server, paths, _ = self.fixture(valid=True, session=False)
        self.assertEqual(self.probe(server.server_port), 'Occupied')
        self.assertEqual(paths, ['/api/catalog', '/api/campaigns'])

    def test_each_changed_fingerprint_or_identity_field_prevents_reuse(self):
        server, paths, state = self.fixture(valid=True)
        changed = [(field, '0' * 64 if self.expected[field] != '0' * 64 else '1' * 64)
                   for field in HASH_FIELDS]
        changed += [('schema_version', 2), ('edition', '0.0.0'), ('classification', 'other')]
        for field, value in changed:
            with self.subTest(field=field):
                state['build'] = {**self.expected, field: value}
                self.assertEqual(self.probe(server.server_port), 'Occupied')
        self.assertEqual(paths, ['/api/catalog', '/api/campaigns'] * len(changed))
        self.assert_listener_preserved(server)

    def test_missing_malformed_or_unknown_build_identity_prevents_reuse(self):
        server, paths, state = self.fixture(valid=True)
        broken = [OMIT_BUILD, None, {}, [], {**self.expected, 'schema_version': '1'},
                  {**self.expected, 'host_source_sha256': None},
                  {**self.expected, 'engine_core_sha256': 'short'},
                  {**self.expected, 'catalog_portfolio_sha256': 'A' * 64}]
        for index, snapshot in enumerate(broken):
            with self.subTest(case=index):
                state['build'] = snapshot
                self.assertEqual(self.probe(server.server_port), 'Occupied')
        state['build'] = self.expected
        self.assertEqual(self.probe(server.server_port, expected=None), 'Occupied')
        self.assertEqual(paths, ['/api/catalog', '/api/campaigns'] * (len(broken) + 1))
        self.assert_listener_preserved(server)

    def test_closed_listener_is_stopped(self):
        server, _, _ = self.fixture(valid=True)
        port = server.server_port
        server.shutdown()
        server.server_close()
        self.assertEqual(self.probe(port), 'Stopped')

    def test_occupied_selected_start_preserves_listener_and_explains_alternate_port(self):
        for label, valid, build in [
                ('unrelated', False, USE_SELECTED), ('missing identity', True, OMIT_BUILD),
                ('different build', True, {**self.expected, 'app_manifest_sha256': '0' * 64
                                          if self.expected['app_manifest_sha256'] != '0' * 64 else '1' * 64})]:
            with self.subTest(listener=label):
                server, paths, _ = self.fixture(valid=valid, build=build)
                with tempfile.TemporaryDirectory(prefix='worldward-launcher-profile-') as folder:
                    result = self.selected_start(server.server_port, Path(folder))
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn('occupied', result.stdout)
                self.assertIn('left running', result.stdout)
                self.assertIn('Choose another port', result.stdout)
                self.assertIn('-Port', result.stdout)
                self.assertEqual(paths, ['/api/catalog', '/api/campaigns'] if valid else ['/api/catalog'])
                self.assert_listener_preserved(server)

    def test_repeated_matching_launches_reuse_without_process_or_browser_start(self):
        server, paths, _ = self.fixture(valid=True)
        with tempfile.TemporaryDirectory(prefix='worldward-launcher-profile-') as folder:
            for _ in range(2):
                result = self.selected_start(server.server_port, Path(folder))
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn('Reusing the existing website', result.stdout)
        # Initial check, post-verification check and pre-reuse check per launch.
        self.assertEqual(paths, ['/api/catalog', '/api/campaigns'] * 6)
        self.assert_listener_preserved(server)


if __name__ == '__main__':
    unittest.main()
