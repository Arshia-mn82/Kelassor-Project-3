import csv
import json
import heapq

class Graph:
    def __init__(self):
        self.adj_matrix = []
        self.edges = []
        self.vertices = set()
    
    def load_from_csv(self, filename):
        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                self.adj_matrix = [list(map(int, row)) for row in reader]
                self.vertices = set(range(len(self.adj_matrix)))
        except FileNotFoundError:
            print(f"Error loading CSV file: {filename} not found.")
        except Exception as e:
            print(f"Error loading CSV file: {str(e)}")

    def load_from_json(self, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.edges = [(edge['src'], edge['dest'], edge['weight']) for edge in data['edges']]
                self.vertices = set(v for edge in self.edges for v in (edge[0], edge[1]))
                self.adj_matrix = self._edges_to_matrix(self.edges)
        except FileNotFoundError:
            print(f"Error loading JSON file: {filename} not found.")
        except json.JSONDecodeError:
            print(f"Error loading JSON file: {filename} is not a valid JSON.")
        except Exception as e:
            print(f"Error loading JSON file: {str(e)}")

    def to_csv(self, filename):
        try:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(self.adj_matrix)
        except Exception as e:
            print(f"Error exporting to CSV: {str(e)}")

    def to_json(self, filename):
        try:
            data = {
                'edges': [{'src': src, 'dest': dest, 'weight': weight} for src, dest, weight in self.edges]
            }
            with open(filename, 'w') as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"Error exporting to JSON: {str(e)}")

    def bfs(self, start_vertex):
        visited = set()
        queue = [start_vertex]
        result = []

        while queue:
            vertex = queue.pop(0)
            if vertex not in visited:
                visited.add(vertex)
                result.append(vertex)
                queue.extend(neighbor for neighbor in self._get_neighbors(vertex) if neighbor not in visited)
        
        return result

    def dfs(self, start_vertex):
        visited = set()
        result = []

        def dfs_recursive(v):
            visited.add(v)
            result.append(v)
            for neighbor in self._get_neighbors(v):
                if neighbor not in visited:
                    dfs_recursive(neighbor)

        dfs_recursive(start_vertex)
        return result

    def dijkstra(self, start_vertex):
        distances = {vertex: float('inf') for vertex in self.vertices}
        distances[start_vertex] = 0
        priority_queue = [(0, start_vertex)]

        while priority_queue:
            current_distance, vertex = heapq.heappop(priority_queue)

            if current_distance > distances[vertex]:
                continue

            for neighbor, weight in self._get_neighbors_with_weights(vertex):
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))
        
        return distances

    def find_shortest_path(self, start_vertex, end_vertex):
        distances = self.dijkstra(start_vertex)
        path = []
        current_vertex = end_vertex

        while current_vertex != start_vertex:
            path.append(current_vertex)
            for neighbor, weight in self._get_neighbors_with_weights(current_vertex):
                if distances[current_vertex] - weight == distances[neighbor]:
                    current_vertex = neighbor
                    break
            else:
                return []  # No path found

        path.append(start_vertex)
        path.reverse()
        return path

    def detect_cycles(self):
        def visit(vertex):
            stack = [vertex]
            visited = set()
            rec_stack = set()

            while stack:
                v = stack.pop()
                if v in rec_stack:
                    return True
                if v not in visited:
                    visited.add(v)
                    rec_stack.add(v)
                    stack.extend(self._get_neighbors(v))
                rec_stack.remove(v)
            return False

        return any(visit(v) for v in self.vertices)

    def _edges_to_matrix(self, edges):
        n = len(self.vertices)
        matrix = [[0] * n for _ in range(n)]
        for src, dest, weight in edges:
            matrix[src][dest] = weight
        return matrix

    def _get_neighbors(self, vertex):
        return [i for i, val in enumerate(self.adj_matrix[vertex]) if val > 0]

    def _get_neighbors_with_weights(self, vertex):
        return [(i, self.adj_matrix[vertex][i]) for i, val in enumerate(self.adj_matrix[vertex]) if val > 0]

    def number_of_vertices(self):
        return len(self.vertices)

    def number_of_edges(self):
        return len(self.edges)
