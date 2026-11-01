# Continue WORLDWARD-APP-WEB

## Independent Store characterization candidate — 1 November 2026

The existing App owner is preparing a separate published-source review candidate
on `review/app-store-characterization-20261101`, based on published App
`c04ba5524ae95316c7e826fc63085a4916d7dd67`. This is not restoration or adoption
of inaccessible owner work. Preserve failed sessions, snapshots and unique old
changes for CMRR before later adoption.

The source-only test module `IRGS_Web/tests/test_store_write_characterization.py`
exercises real Store writes in temporary synthetic directories. It injects file
fsync and replacement failures before publication, parent-sync failure after
replacement, repeated sync uncertainty, and real POSIX directory-sync confirmation
without another record write or replacement. It deliberately characterizes JSON
file storage, not initialized Core worlds, a Creator envelope or crash recovery.
The POSIX confirmation case skips on Windows because sync_parent is a no-op there.

Execution is pending the existing coordinator's exact-commit run:
`python3 -B -m unittest discover -s IRGS_Web/tests -p test_store_write_characterization.py -v`
and `python3 -B tools/verify_components.py --component app`.
No test pass, filesystem crash qualification or Alpha gate closure is claimed.

Stable Saves candidate `197d41a910b37b5c8b27d0f7dc9224b068244364` remains separate
and unchanged for its coordinator tests. This branch does not include that fix.
Engine stays pinned at `ecca8094a2d2cdb8a11e018a085487288b26e88d`; Catalog stays
pinned at `a18cb48928da25d40d057a182c69f71ef149ce80`.

Preview source assessment is complete; preview implementation is held behind this
characterization. The exact selected Engine world_draft.preview_initialization
DTO is `irgs-world-initialization-preview-1`: preview_only, committed false,
requires_explicit_acceptance true, preview_identities_reusable false, with an
actor_view derived by Engine shared_runtime.actor_view from its disposable
candidate's actual controlled actor. Do not substitute App playthrough in Creator
mode, which intentionally exposes inspection records, or guess an actor mapping.
Any future preview route must use the existing Host/Origin/session and explicit
Creator guard, bounded exact draft fields and Engine source/classification
validation. Browser text must remain separate from Story drafts; edit, cancel,
navigation and mode changes must fence late responses. Preview identities confer
no campaign/action authority. Add authenticated-host, nested privacy and exact
no-campaign-write tests before claiming that route.

Durable creation remains held: local-owner binding, immutable original initial
receipts, reservations/tombstones, cross-process serialization and atomic
campaign/restore-guard recovery are not provided by these storage tests. Engine's
documentation revision `7d17ec6212f283df88f49c6ffc993b77df5a6e45` reflects the
inspected local-owner model and public save/branch ID; it is reviewed design,
not an adopted runtime pin or implemented durable creation contract. All twelve requested 5.0 gates remain open;
the pinned target guide is in joined WorldWard at
`3f174ffad14e2219c483dd5366bb56254e08a401/TARGET_5_0.md`.
Published edition remains 3.4.8; joined integration/publication belongs solely to
the existing coordinator.

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
