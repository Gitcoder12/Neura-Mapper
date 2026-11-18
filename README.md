# Neura-Mapper
3D Spatial Optimization and Diagnostic Routing Engine for Computer Assisted Neurosurgery. 


---

## AI-maintained project notes (secondary — 2026-11-13)

This section supplements the maintainer-authored README above; it does not replace or certify the original claims.

- The current source tree, actual data and executed tests are the implementation source of truth. Roadmap items and draft PRs are not shipped capabilities.
- Preserve real/user-provided data and source provenance. Never replace it with fabricated or synthetic runtime records; isolate and label fixtures.
- Document units, coordinate frames, source, licence, collection date, assumptions, seeds and validation methods where applicable.
- Mark unverifiable fields and metrics as unknown/unverified. Do not invent clinical, scientific or official claims.
- Verify installation, execution and tests against the exact current commit before public use.
- See [MODEL_AUDIT_ROUTER.md](MODEL_AUDIT_ROUTER.md) for independent review instructions.

---

## Engineering Audit & Handover — 2026-11-17

**Reviewed commit:** `53a270b8edf10dad77f2d5b8327e36462778772b` (`main`). Static inspection covered `neuro_router.py` and `pathfinder.py`; tests were not executed.

### Confirmed findings
- `NeuroMapper.find_safest_path()` validates start/end coordinates against grid bounds and treats classification value 2 as impassable.
- The separate `AStarRouter.find_path()` in `pathfinder.py` does not validate the start or goal before search. An out-of-bounds start can therefore be expanded into the grid rather than being rejected at the API boundary.
- `classify_region()` stores the supplied coordinate/classification without validating tuple shape, bounds, or the allowed values 0/1/2.
- The “surgical robots” description is not evidence of clinical or physical-robot validation; the inspected code is a grid pathfinding prototype.

### Next actions
1. Share one validated coordinate/classification schema between both pathfinders.
2. Add tests for out-of-bounds start/goal, malformed coordinates, invalid classification values, unreachable goals, and warning-cost optimality.
3. Keep the project labelled as a simulation/prototype until independently validated in a controlled robotics environment.

**Verification status:** static source inspection only; pathfinding tests and physical-system integration remain unverified.

---

## Examples Used
- Finding a low-cost path through a 3D anatomical grid
- Routing around regions marked as obstacles
- Comparing alternative paths in a simulated surgical-planning environment
