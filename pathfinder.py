"""A* routing on a validated 3D zone grid."""

from __future__ import annotations

import heapq
import logging
from typing import Iterable

logger = logging.getLogger("NeuraMapper.AStar")


class AStarRouter:
    """3D A* with critical obstacles and weighted warning zones.

    This is a grid simulation, not a certified surgical or robotic planner.
    """

    def __init__(self, grid_size: tuple[int, int, int]):
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
            raise ValueError("classification must be 0, 1 or 2")
        self.zones[tuple(coord)] = classification

    def _heuristic(self, first: tuple[int, int, int], second: tuple[int, int, int]) -> int:
        """Admissible Manhattan heuristic because every step costs at least one."""
        return (
            abs(first[0] - second[0])
            + abs(first[1] - second[1])
            + abs(first[2] - second[2])
        )

    def find_path(
        self,
        start: tuple[int, int, int],
        goal: tuple[int, int, int],
    ) -> list[tuple[int, int, int]]:
        """Find a least-cost path; return an empty list for invalid or unreachable endpoints."""
        if not self._valid_coordinate(start) or not self._valid_coordinate(goal):
            return []
        start = tuple(start)
        goal = tuple(goal)
        if self.zones.get(start, 0) == 2 or self.zones.get(goal, 0) == 2:
            return []

        open_list = [(self._heuristic(start, goal), 0, start, [start])]
        best_cost = {start: 0}
        closed_set: set[tuple[int, int, int]] = set()
        directions = (
            (1, 0, 0), (-1, 0, 0),
            (0, 1, 0), (0, -1, 0),
            (0, 0, 1), (0, 0, -1),
        )

        while open_list:
            _, cost, current, path = heapq.heappop(open_list)
            if cost != best_cost.get(current):
                continue
            if current == goal:
                return path
            if current in closed_set:
                continue
            closed_set.add(current)

            for dx, dy, dz in directions:
                neighbour = (current[0] + dx, current[1] + dy, current[2] + dz)
                if not self._valid_coordinate(neighbour):
                    continue
                zone = self.zones.get(neighbour, 0)
                if zone == 2:
                    continue
                step_cost = 10 if zone == 1 else 1
                new_cost = cost + step_cost
                if new_cost < best_cost.get(neighbour, float("inf")):
                    best_cost[neighbour] = new_cost
                    f_score = new_cost + self._heuristic(neighbour, goal)
                    heapq.heappush(
                        open_list, (f_score, new_cost, neighbour, path + [neighbour])
                    )

        logger.warning("No path found to target.")
        return []
