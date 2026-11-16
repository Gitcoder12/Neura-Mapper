# Neura-Mapper — README Explanation Draft

## In plain language

A simple 3D grid pathfinder that finds a route through cells labelled as open, risky or blocked.

## What it currently does

It represents a 3D space as a grid of cells and searches for a route between selected coordinates while avoiding cells that the current rules treat as blocked or costly.

## Technical explanation

Current implementation is a small in-memory 3D grid pathfinder with manually assigned safe/warning/critical voxels. It has no medical-image ingestion, anatomical registration, clinical validation, uncertainty model or clinical workflow integration. The repository must be described as an educational/research prototype, not a neurosurgical navigation system.

Document grid indexing, dimensions, neighborhood connectivity, cost model, path search algorithm, validation and output structure. Include a small example with a known expected route.

## Safety and limitations

This code does not read medical scans, identify anatomy, locate surgical structures or validate clinical paths. It is not a medical device or surgical navigation system. Do not use it for patient care.

## Contributing

See FEATURE_UPGRADE_PLAN.md and CONTRIBUTING.md.
