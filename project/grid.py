import heapq

class Grid:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.static_no_fly_zones = set()
        self.reservation_table = {} 
        self.edge_reservation = {}

    def register_no_fly_zones(self, cells):
        """إضافة العوائق مع التأكد أنها داخل حدود الخريطة"""
        for cell in cells:
            if 0 <= cell[0] < self.width and 0 <= cell[1] < self.height:
                self.static_no_fly_zones.add(cell)

    def find_path_time_aware(self, start, goal, start_time=0):
        if start == goal: return [(start, start_time)], 0
        MAX_TIME = start_time + (self.width * self.height * 2)
        frontier = [(0, start, start_time)]
        came_from, cost_so_far = {(start, start_time): None}, {(start, start_time): 0}

        while frontier:
            _, current, t = heapq.heappop(frontier)
            if current == goal:
                path = []
                state = (current, t)
                while state:
                    path.append(state); state = came_from[state]
                return path[::-1], cost_so_far[(current, t)]
            
            if t > MAX_TIME: continue

            for nxt in [(current[0]+dx, current[1]+dy) for dx, dy in [(1,0), (-1,0), (0,1), (0,-1), (0,0)]]:
                if not (0 <= nxt[0] < self.width and 0 <= nxt[1] < self.height) or nxt in self.static_no_fly_zones: continue
                nt = t + 1
                if nt in self.reservation_table and nxt in self.reservation_table[nt]: continue
                if nt in self.edge_reservation and (nxt, current) in self.edge_reservation[nt]: continue

                new_cost = cost_so_far[(current, t)] + (1.2 if nxt == current else 1)
                if (nxt, nt) not in cost_so_far or new_cost < cost_so_far[(nxt, nt)]:
                    cost_so_far[(nxt, nt)] = new_cost
                    priority = new_cost + (abs(goal[0]-nxt[0]) + abs(goal[1]-nxt[1]))
                    heapq.heappush(frontier, (priority, nxt, nt))
                    came_from[(nxt, nt)] = (current, t)
        return None, None

    def reserve_path(self, path):
        for i, (node, t) in enumerate(path):
            if t not in self.reservation_table: self.reservation_table[t] = set()
            self.reservation_table[t].add(node)
            if i > 0:
                if t not in self.edge_reservation: self.edge_reservation[t] = set()
                self.edge_reservation[t].add((path[i-1][0], node))

    def cancel_reservation(self, path, from_time):
        for i, (node, t) in enumerate(path):
            if t >= from_time:
                if t in self.reservation_table and node in self.reservation_table[t]: self.reservation_table[t].remove(node)
                if i > 0:
                    prev = path[i-1][0]
                    if t in self.edge_reservation and (prev, node) in self.edge_reservation[t]: self.edge_reservation[t].remove((prev, node))