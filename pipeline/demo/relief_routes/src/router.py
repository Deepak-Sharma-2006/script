def shortest_distance(edge_map: dict, node_a: str, node_b: str) -> int:
    return edge_map.get((node_a, node_b), edge_map.get((node_b, node_a), -1))
