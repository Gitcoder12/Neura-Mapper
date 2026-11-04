import heapq
import math
import logging
from typing import List, Tuple, Dict

logger = logging.getLogger("NeuraMapper.AStar")

class AStarRouter:
    """3D A* Pathfinding for surgical robots."""
    
    def __init__(self, grid_size: Tuple[int, int, int]):
        self.grid_size = grid_size
        self.zones = {} # 0: Safe, 1: Warning, 2: Critical

    def _heuristic(self, a: Tuple[int, int, int], b: Tuple[int, int, int]) -> float:
        # Manhattan distance in 3D
        return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])

    def find_path(self, start: Tuple[int, int, int], goal: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
        logger.info(f"Calculating A* path from {start} to {goal}")
        
        # Priority queue: (f_score, g_score, current_node, path)
        open_list = [(0, 0, start, [start])]
        closed_set = set()
        
        while open_list:
            _, g_score, current, path = heapq.heappop(open_list)
            
            if current == goal:
                logger.info(f"Path found with {len(path)} steps.")
                return path
                
            if current in closed_set:
                continue
            closed_set.add(current)
            
            # Check 6 directions
            for d in [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]:
                neighbor = (current[0]+d[0], current[1]+d[1], current[2]+d[2])
                
                # Bounds check
                if not all(0 <= neighbor[i] < self.grid_size[i] for i in range(3)):
                    continue
                    
                # Obstacle check (Critical zones)
                if self.zones.get(neighbor, 0) == 2:
                    continue
                    
                # Warning zones add a penalty
                step_cost = 10 if self.zones.get(neighbor, 0) == 1 else 1
                new_g_score = g_score + step_cost
                f_score = new_g_score + self._heuristic(neighbor, goal)
                
                heapq.heappush(open_list, (f_score, new_g_score, neighbor, path + [neighbor]))
                
        logger.warning("No path found to target.")
        return []
