"""Validated 3D zone map and safest-path routing prototype."""

from __future__ import annotations

import heapq
from typing import Iterable


class NeuroMapper:
    """Classify voxels and find a low-risk path through a 3D grid.

    This remains a spatial simulation prototype. It does not validate clinical
    anatomy, surgical safety or physical robot motion.
    """

    def __init__(self, grid_size: tuple[int, int, int] = (10, 10, 10)):
        self.grid_size = self._validate_grid_size(grid_size)
        self.zones: dict[tuple[int, int, int], int] = {}

    @staticmethod
    def _validate_grid_size(grid_size: Iterable[int]) -> tuple[int, int, int]:
        try:
            values = tuple(grid_size)
        except TypeError as exc:
            raise ValueError("grid_size must contain three positive integers") from exc
        if (
            len(values) != 3
            or any(isinstance(value, bool) or not isinstance(value, int) or value < 1 for value in values)
        ):
            raise ValueError("grid_size must contain three positive integers")
        return values

    def _valid_coordinate(self, coord: object) -> bool:
        if not isinstance(coord, (tuple, list)) or len(coord) != 3:
            return False
        if any(isinstance(value, bool) or not isinstance(value, int) for value in coord):
            return False
        return all(0 <= coord[index] < self.grid_size[index] for index in range(3))

    def classify_region(self, coord: tuple[int, int, int], classification: int) -> None:
        """Classify a voxel: 0=safe, 1=warning, 2=critical."""
        if not self._valid_coordinate(coord):
            raise ValueError("coord must be an in-bounds integer 3D coordinate")
        if isinstance(classification, bool) or classification not in (0, 1, 2):
            raise ValueError("classification must be 0 (safe), 1 (warning), or 2 (critical)")
        self.zones[tuple(coord)] = classification

    def is_valid(self, coord: tuple[int, int, int]) -> bool:
        """Return whether a coordinate is in bounds and not critically classified."""
        if not self._valid_coordinate(coord):
            return False
        return self.zones.get(tuple(coord), 0) != 2

    def get_neighbors(self, coord: tuple[int, int, int]) -> list[tuple[int, int, int]]:
        """Return valid 6-connected neighbours for one valid coordinate."""
        if not self._valid_coordinate(coord):
            return []
        directions = (
            (1, 0, 0), (-1, 0, 0),
            (0, 1, 0), (0, -1, 0),
            (0, 0, 1), (0, 0, -1),
        )
        neighbours = []
        for dx, dy, dz in directions:
            neighbour = (coord[0] + dx, coord[1] + dy, coord[2] + dz)
            if self.is_valid(neighbour):
                neighbours.append(neighbour)
        return neighbours

    def find_safest_path(
        self,
        start: tuple[int, int, int],
        end: tuple[int, int, int],
    ) -> list[tuple[int, int, int]] | None:
        """Run Dijkstra search with a penalty for warning voxels."""
        if not self.is_valid(start) or not self.is_valid(end):
            return None

        start = tuple(start)
        end = tuple(end)
        queue = [(0, start, [start])]
        best_cost = {start: 0}

        while queue:
            cost, current, path = heapq.heappop(queue)
            if cost != best_cost.get(current):
                continue
            if current == end:
                return path

            for neighbour in self.get_neighbors(current):
                step_cost = 10 if self.zones.get(neighbour, 0) == 1 else 1
                new_cost = cost + step_cost
                if new_cost < best_cost.get(neighbour, float("inf")):
                    best_cost[neighbour] = new_cost
                    heapq.heappush(
                        queue, (new_cost, neighbour, path + [neighbour])
                    )
        return None
