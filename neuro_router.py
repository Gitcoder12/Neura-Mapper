import heapq
import math

class NeuroMapper:
    def __init__(self, grid_size=(10, 10, 10)):
        self.grid = {}
        self.grid_size = grid_size
        self.critical_regions = set()

    def add_critical_region(self, coord):
        """Marks a voxel as high-risk (e.g., a tumor or vital area)."""
        self.critical_regions.add(coord)

    def is_valid(self, coord):
        x, y, z = coord
        if not (0 <= x < self.grid_size[0] and 0 <= y < self.grid_size[1] and 0 <= z < self.grid_size[2]):
            return False
        if coord in self.critical_regions:
            return False
        return True

    def get_neighbors(self, coord):
        """Gets 6-directional neighbors in 3D space."""
        directions = [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]
        neighbors = []
        for dx, dy, dz in directions:
            neighbor = (coord[0]+dx, coord[1]+dy, coord[2]+dz)
            if self.is_valid(neighbor):
                neighbors.append(neighbor)
        return neighbors

    def find_safest_path(self, start, end):
        """Dijkstra's algorithm to find the safest (shortest) path."""
        if start in self.critical_regions or end in self.critical_regions:
            return None

        # Priority queue: (cost, current_coord, path)
        queue = [(0, start, [start])]
        visited = set()

        while queue:
            cost, current, path = heapq.heappop(queue)
            if current == end:
                return path
            if current in visited:
                continue
            visited.add(current)

            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    new_cost = cost + 1  # Uniform cost for simplicity
                    heapq.heappush(queue, (new_cost, neighbor, path + [neighbor]))
        return None

# --- Example Usage ---
if __name__ == "__main__":
    mapper = NeuroMapper(grid_size=(5, 5, 5))
    
    # Add some critical (high-risk) regions in the middle
    for x in range(1, 4):
        for y in range(1, 4):
            mapper.add_critical_region((x, y, 2))

    start = (0, 0, 0)
    end = (4, 4, 4)
    
    safest_path = mapper.find_safest_path(start, end)
    print(f"Start: {start}, End: {end}")
    print(f"Critical Regions Blocked (Layer Z=2): {(1,1,2), (2,2,2), (3,3,2)}")
    print(f"Path found: {safest_path}")
