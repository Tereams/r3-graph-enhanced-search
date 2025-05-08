
import networkx as nx
from collections import deque

def find_nodes_within_distance(G, start_node_id, max_distance=5):
    """
    使用 BFS 从 start_node 开始遍历，返回距离小于或等于 max_distance 的所有节点及其距离。

    参数：
      G: NetworkX 图
      start_node: 起始节点
      max_distance: 最大距离（包含此距离）的节点将被返回

    返回：
      一个列表，列表中的每个元素是 (节点, 距离) 元组
    """
    visited = set()
    queue = deque([(start_node_id, 0)])
    result = []
    
    while queue:
        node_id, dist = queue.popleft()
        if node_id in visited:
            continue
        visited.add(node_id)
        
        # 只保存距离在 max_distance 以内的节点
        if dist <= max_distance and G.nodes[node_id].get('type') == 'title':
            result.append((node_id, dist))
        elif dist > max_distance:
            # 如果当前节点距离已超过 max_distance，就无需扩展其邻居
            continue

        # 如果当前距离还未达到最大值，则将其邻居加入队列
        if dist < max_distance:
            for neighbor in G.neighbors(node_id):
                if neighbor not in visited:
                    queue.append((neighbor, dist + 1))
    return result


if __name__ =='__main__':
    G = nx.read_gml('graph1.gml')
    # 示例：假设图 G 已经构建，并且存在关键词节点 "fading channels"
    start_keyword = "fluorescence"  
    nodes_within_5 = find_nodes_within_distance(G, start_keyword, max_distance=3)
    print(nodes_within_5)
# print("距离节点 '{}' 5以内的所有节点:".format(start_keyword))
# for node, distance in nodes_within_5:
#     print(f"节点: {node}, 距离: {distance}")