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


---

## Comparison with Existing Open-Source Projects

Neura-Mapper is described as a 3D spatial pathfinding/diagnostic-routing prototype in an anatomical grid. The following projects are established medical-imaging and image-computing platforms; they are relevant technical references, not proof of clinical equivalence.

| Project | Established focus | Relationship to Neura-Mapper |
|---|---|---|
| [3D Slicer](https://github.com/Slicer/Slicer) | Medical-image visualization, segmentation and research workflows | A mature medical-imaging platform; Neura-Mapper's documented focus is a narrower grid-based pathfinding experiment. |
| [MONAI](https://github.com/Project-MONAI/MONAI) | Deep-learning framework and tools for healthcare imaging | A broad AI medical-imaging ecosystem; Neura-Mapper currently describes algorithmic routing, not a validated imaging/AI pipeline. |
| [SimpleITK](https://github.com/SimpleITK/SimpleITK) | Medical-image processing and registration toolkit | Provides mature image-processing primitives; Neura-Mapper's current grid representation is a simplified abstraction rather than a complete medical-image workflow. |

### Where Neura-Mapper is different
- **Path-planning emphasis:** the documented prototype searches for routes through a spatial grid with blocked regions and warning costs.
- **Diagnostic-planning framing:** the concept applies spatial routing to a neurosurgical planning context rather than general-purpose image processing.
- **Inspectable algorithms:** separate pathfinding implementations make algorithmic assumptions and route costs easier to examine.

### Where established projects are stronger
3D Slicer, MONAI and SimpleITK have much broader imaging, data-handling and research ecosystems. Neura-Mapper's current code audit identifies grid/pathfinding validation gaps and does not establish clinical, anatomical or physical-robot validation.

### Medical safety and evidence requirements
Keep all outputs clearly labelled as simulation/research prototypes. Validate coordinate frames, units, image registration, anatomical segmentation and obstacle definitions before any clinical interpretation. Add independent expert review and rigorous testing; never use the current tool for patient care or surgical guidance. This is a scope comparison, not a clinical-safety assessment.
