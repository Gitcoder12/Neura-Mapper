# Neura-Mapper
3D Spatial Optimization and Diagnostic Routing Engine for Computer Assisted Neurosurgery.

---

## Project handbook

- [Activity log](ACTIVITY_LOG.md) · [Feature upgrade plan](FEATURE_UPGRADE_PLAN.md)
- [Company and team fit](COMPANY_FIT.md) · [README explanation draft](README_ADDENDUM_DRAFT.md)
- [README quality checklist](README_QUALITY_CHECKLIST.md)
- [Contributing](CONTRIBUTING.md) · [Agent instructions](AGENTS.md) · [Agent skills](SKILLS.md)

## Understanding the project

### In plain language

A simple 3D grid pathfinder that finds a route through cells labelled as open, risky or blocked.

### Technical and research view

Current implementation is a small in-memory 3D grid pathfinder with manually assigned safe/warning/critical voxels. It has no medical-image ingestion, anatomical registration, clinical validation, uncertainty model or clinical workflow integration. The repository must be described as an educational/research prototype, not a neurosurgical navigation system.

Document grid indexing, dimensions, neighborhood connectivity, cost model, path search algorithm, validation and output structure. Include a small example with a known expected route.

For future work, see [FEATURE_UPGRADE_PLAN.md](FEATURE_UPGRADE_PLAN.md), [ACTIVITY_LOG.md](ACTIVITY_LOG.md), [COMPANY_FIT.md](COMPANY_FIT.md) and [CONTRIBUTING.md](CONTRIBUTING.md).
