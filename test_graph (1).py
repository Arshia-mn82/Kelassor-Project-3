from graph import Graph  # Assuming the class is saved in graph.py

def test_graph():
    g = Graph()

    # Test loading from CSV
    try:
        g.load_from_csv('graph_matrix.csv')
        print("Graph loaded from CSV:")
        print("Vertices:", g.vertex_names())
        print("Number of vertices:", g.number_of_vertices())
        print("Number of edges:", g.number_of_edges())
        print("Adjacency Matrix (CSV):", g.to_list())
    except FileNotFoundError as e:
        print(f"Error loading CSV file: {e}")

    # Test BFS and DFS
    print("BFS starting from vertex 0:", g.bfs(0))
    print("DFS starting from vertex 0:", g.dfs(0))
    
    # Test Dijkstra's algorithm
    print("Dijkstra's algorithm starting from vertex 0:", g.dijkstra(0))

    # Test exporting to CSV
    try:
        g.to_csv('exported_matrix.csv')
        print("Graph exported to CSV.")
    except Exception as e:
        print(f"Error exporting CSV file: {e}")

    # Test loading from JSON
    try:
        g.load_from_json('graph_edges.json')
        print("\nGraph loaded from JSON:")
        print("Vertices:", g.vertex_names())
        print("Number of vertices:", g.number_of_vertices())
        print("Number of edges:", g.number_of_edges())
        print("Adjacency Matrix (JSON):", g.to_list())
    except FileNotFoundError as e:
        print(f"Error loading JSON file: {e}")

    # Test exporting to JSON
    try:
        g.to_json('exported_edges.json')
        print("Graph exported to JSON.")
    except Exception as e:
        print(f"Error exporting JSON file: {e}")

if __name__ == "__main__":
    test_graph()
