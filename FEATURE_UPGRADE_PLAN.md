# Neura-Mapper — Feature Upgrade Plan

## Objective

A simple 3D grid pathfinder that finds a route through cells labelled as open, risky or blocked.

## P0 — prototype boundaries and correctness

- [ ] Validate grid dimensions, coordinate shapes/ranges and classification values before pathfinding.
- [ ] Remove clinical-navigation implications until there is independent medical validation, regulatory review and an appropriate safety case.

## P1 — deterministic pathfinding

- [ ] Add deterministic tests for blocked paths, unreachable targets, invalid coordinates and path costs.
- [ ] Document neighborhood connectivity, movement cost, tie-breaking and no-path behavior.

## P2 — research evaluation

- [ ] Add synthetic anatomical-like volumes only with explicit non-clinical labelling and provenance.
- [ ] Compare pathfinding baselines and quantify sensitivity to voxel size and risk penalties.

## Contributor work packages

1. Input validation for grid and coordinates.
2. Path algorithm tests with known optimal solutions.
3. Cost/connectivity documentation and reproducible examples.
4. Synthetic-volume evaluation with non-clinical scope statement.

## Definition of done

- [ ] Invalid grid/coordinate inputs fail safely.
- [ ] Tests cover reachable, blocked and unreachable paths.
- [ ] Path costs and connectivity are documented.
- [ ] README does not imply clinical use or safety certification.
