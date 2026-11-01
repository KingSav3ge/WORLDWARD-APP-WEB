# Continue WORLDWARD-APP-WEB

## Independent launcher fixture candidate — 1 November 2026

The same App owner is the sole writer of
`review/app-launcher-fixtures-20261101`, based on published App
`c04ba5524ae95316c7e826fc63085a4916d7dd67`. This is separate published-source
work, not recovery/adoption of inaccessible owner work. Keep failed sessions,
snapshots and unique changes for later CMRR.

The bounded source update changes only `IRGS_Web/tests/test_launcher.py`,
its App manifest hash and these notes. Runtime launchers, host behavior,
product policy and all committed dependency pointers remain unchanged.
Fixtures use the existing App build_identity.running_build snapshot, including
edition/classification and all six App/Engine/Catalog fingerprints. The selected
identity is passed to Get-IrgsHostState and returned by synthetic session health.
Nine authored methods cover matching reuse, changed/missing/malformed identity,
unrelated/incomplete health, a closed fixture port, preservation of occupied
listeners, actionable -Port guidance, repeated reuse, and entrypoint parsing.

Paired test selection is REQUIRED: set the normal IRGS_ENGINE_ROOT to IRGS_3_3
from a verified Engine `6b88eb6f9006b3fa4927401cc21734f73c2dfd57` checkout.
That Engine review is based on the committed dependency
`ecca8094a2d2cdb8a11e018a085487288b26e88d`; the App gitlink is not advanced.
Keep the normal IRGS_CATALOG_ROOT on Catalog
`a18cb48928da25d40d057a182c69f71ef149ce80`.
The paired launcher source/limits are described in Engine
`engine/LAUNCHER_IDENTITY_REVIEW.md` at that exact review commit.

In an already permitted fixture environment, run:
`python3 -B -m unittest discover -s IRGS_Web/tests -p test_launcher.py -v`
and `python3 -B tools/verify_components.py --component app`.
The tests require an available PowerShell executable and the existing explicit
IRGS_LAUNCHER_TEST_POLICY_ALLOWED admission. The fixture never sets that opt-in,
changes execution policy or passes an execution-policy switch. Missing runtime
or admission gives clear skips. One ordinary dot-source admission occurs before
HTTP fixtures; a policy denial skips the class without a retry or inline/copied
launcher fallback. A later denial stops remaining probes as well.
Do not set an opt-in to retry the policy-blocked Windows relay. Its denied
pre-HTTP probe remains denied and unqualified.

Start/reuse cases isolate synthetic listener decisions: selected-build lookup
and release verification are stubbed, process/browser starts and process stops
are forbidden. Only a child process receives a temporary synthetic USERPROFILE
with a never-executed Python-path sentinel. No real campaign, host or policy is
changed. Engine-owned resolver/integrity checks remain separately required.
No fixture, Python compilation or PowerShell execution has run in the App owner
environment. Coordinator execution/admission and actual pass/skip counts remain
pending. Portable PowerShell tests cannot qualify native Windows or G01 alone.

Other candidates remain independent and unchanged:
- Saves `197d41a910b37b5c8b27d0f7dc9224b068244364`.
- Store `6381803b402f48492efeda74d64a1d33582e2130`: coordinator reports the
  corrected original bare command with PYTHONPATH absent passed all four methods,
  zero skips, plus component integrity. The earlier f8 source loader failure
  and its separate PYTHONPATH diagnostic remain in their original history.
- Preview `1fa64ca1b9710826a8990fc03f8bbef05fc56fcf`: coordinator reports
  focused host tests, 165 DOM checks and component integrity passed; full Web
  ran 284 tests, seven Windows skips, zero failures/errors. Actual desktop/mobile
  preview journeys remain in progress. These are relayed exact-source results,
  not execution by this owner or qualifications transferred to this candidate.

Merge convergence supersedes the optional next G09 feature suggestion. Finish
present work only. The finite App selection is Saves197d41a + Store6381803 +
preview1fa64ca, with preview browser qualification and the coordinator-selected
Engine/Catalog merged SHAs still required before a qualified App main merge.
This launcher-fixture/Engine6b88 pair stays a separate optional candidate and
is excluded unless ordinary permitted qualification finishes. Do not bypass
the native denial to include it. The existing owner will combine selected source
and hashes, deliberately commit only authorized exact dependency pins, obtain
same-candidate coordinator tests, then use an ordinary permitted App merge.
Old PR/source history remains; no force-push or PR approval is authorized.
No new G09/runtime feature starts during convergence. Durable Creator creation
stays unavailable and all twelve 5.0 gates remain open. Published main/version
and joined publication ownership stay with the existing coordinator.

Current edition: **3.4.8 Pre-Alpha**; previous_version: **3.3.3**.
Next unified main publication: **3.4.9**. Functional Alpha 4.0 remains unqualified.

T!DEMARCH Studios is the parent studio, WorldWard the product, and Fulcrum Engine
the simulation technology. IRGS remains the internal initiative. Canonical public
repositories are KingSav3ge/WorldWard, KingSav3ge/Fulcrum-Engine,
KingSav3ge/WORLDWARD-APP-WEB and KingSav3ge/WorldWard-Catalog. Preserve existing
technical paths, schemas, fixtures, original archives, saves and settings.

This edition consolidates completed design/instruction deliveries, the proposed
Creator handoff and exact compatible component pins. Runtime mechanics are those
of the qualified 3.4.7 baseline. Rise building limits and expansion permission are
a user-adopted requirement; numeric profiles and runtime implementation are still
open. Creator preview/durable playtest creation is proposed, not executable.

Keep one authoritative Core, the nine existing K owners and six Directors,
actor-scoped information, conserved resources, atomic rejection and immutable
original-result recovery. Time, causal sequence and storage revision remain
distinct. No live provider, native Windows, arbitrary world authoring or Alpha
qualification follows from this documentation update.

## Existing owner

Thread: 01a164a6-687b-723a-ac81-acb55e3d50d2.

## Next bounded work after unification

After the unification checkpoint, first reproduce and patch the stale Saves
revision summary found by the ordinary 30 October playtest, using the existing
App save/list state and a browser regression. Keep this independent of Engine
rights/schema work. Then implement only the bounded Creator preview portion of
WB_APP_01_CREATOR_DRAFT_HANDOFF; durable creation remains disabled until its two
Engine/coordinator contract questions are resolved. Consume Rise allowance
controls only after published Engine DTOs and authored Catalog rules. Preserve
the chronological tale, latest response form, exact words, drafts and recovery.

Read COORDINATOR_WORK_ORDER_RISE_EXPANSION_01.md for the adopted Rise requirement.

## Delivery and coordination

Preserve local work and history. Pull the correct origin/main only into clean
compatible source; never force-push, auto-stash or reset over user work. Use
synthetic campaigns, temporary test stores and the existing Core/K/Director
owners. Report exact commits, pins, executed checks/skips and limitations.
Only the coordinator joins a reviewed compatible set after integration, fresh
operation capture, joined regression, browser/independent consumers and a clean
extracted package. Every joined main push increments the edition.

These files do not wake owner chats. Current owner-chat reads/dispatch are
unavailable through the coordinator bridge. Resume the existing owner, not a
replacement project/chat. The earlier Vercel source-copy denial remains binding:
do not retry or route around that transfer. No external deployment is part of
this work. DLVA is separate and receives no WorldWard files.
