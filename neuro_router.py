import heapq

class NeuroMapper:
    def __init__(self, grid_size=(10, 10, 10)):
        self.grid_size = grid_size
        # Classifier dictionary: 0=Safe, 1=Warning, 2=Critical
        self.zones = {} 

    def classify_region(self, coord, classification):
        """
        Classify a voxel: 
        0 = Safe (Green), 1 = Warning (Yellow), 2 = Critical (Red)
        """
        self.zones[coord] = classification

    def is_valid(self, coord):
        x, y, z = coord
        if not (0 <= x < self.grid_size[0] and 0 <= y < self.grid_size[1] and 0 <= z < self.grid_size[2]):
            return False
        # If the zone is Critical (2), it's impassable
        if self.zones.get(coord, 0) == 2:
            return False
        return True

    def get_neighbors(self, coord):
        directions = [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]
        neighbors = []
        for dx, dy, dz in directions:
            neighbor = (coord[0]+dx, coord[1]+dy, coord[2]+dz)
            if self.is_valid(neighbor):
                neighbors.append(neighbor)
        return neighbors

    def find_safest_path(self, start, end):
        if not self.is_valid(start) or not self.is_valid(end):
            return None

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
                    # If it's a Warning zone (1), add a heavy penalty to the cost
                    penalty = 10 if self.zones.get(neighbor, 0) == 1 else 1
                    new_cost = cost + penalty
                    heapq.heappush(queue, (new_cost, neighbor, path + [neighbor]))
        return None
