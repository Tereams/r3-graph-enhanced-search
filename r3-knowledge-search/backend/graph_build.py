import json
import networkx as nx
import matplotlib.pyplot as plt

# 文件路径
file_path = 'result_id.jsonl'

titles = []           # 用于存储文章标题
keywords_set = set()  # 用于存储所有不重复的关键词
edges = []            # 用于存储文章标题和关键词之间的关系
ids=[]

# 读取 JSONL 文件数据
with open(file_path, 'r', encoding='utf-8') as f:
    for line in f:
        if line.strip():  # 忽略空行
            data = json.loads(line)
            id = data.get('id', '').strip()
            if id:
                ids.append(id)
            title = data.get('title', '').strip()
            if title:
                titles.append(title)
            # 读取关键词列表
            for kw in data.get('keywds', []):
                kw = kw.strip().lower()
                if kw:
                    keywords_set.add(kw)
                    # 添加文章标题与关键词之间的边
                    edges.append((title, kw))

# 为文章标题和关键词生成唯一索引
# 假设文章标题在文件中是唯一的
title_index = {title: idx for idx, title in zip(ids,titles)}
keyword_index = {kw: str(idx) for idx, kw in enumerate(keywords_set)}
index_title = {idx:title for idx, title in zip(ids,titles)}
index_keyword = {idx:kw for idx, kw in enumerate(keywords_set)}

# 构建图
G = nx.Graph()

# 添加文章标题节点（设置属性 type 为 'title' 和对应的 index）
for title in titles:
    G.add_node(title_index[title], type='title', name=title)

# 添加关键词节点（设置属性 type 为 'keyword' 和对应的 index）
for kw in keywords_set:
    G.add_node(keyword_index[kw], type='keyword', name=kw)

# 添加边：每条边表示文章标题与关键词之间的关联
for title, kw in edges:
    G.add_edge(title_index[title], keyword_index[kw])

nx.write_gml(G, 'graph3.gml')

with open('title_index.json', 'w', encoding='utf-8') as f:
    json.dump(title_index, f, ensure_ascii=False, indent=2)

with open('keyword_index.json', 'w', encoding='utf-8') as f:
    json.dump(keyword_index, f, ensure_ascii=False, indent=2)

# 输出节点信息（可选）
# print("文章标题节点及索引：", title_index)
# print("关键词节点及索引：", keyword_index)

# 绘制图（简单示例）
# pos = nx.spring_layout(G)  # 使用弹簧布局
# # 根据节点类型设置不同的颜色（文章标题红色，关键词蓝色）
# node_colors = ['red' if G.nodes[node]['type'] == 'title' else 'blue' for node in G.nodes()]
# nx.draw(G, pos, with_labels=False, node_color=node_colors, node_size=2)
# plt.title("文章标题与关键词关系图")
# plt.show()

# from collections import deque

# def find_nodes_within_distance(G, start_node, max_distance=5):
#     """
#     使用 BFS 从 start_node 开始遍历，返回距离小于或等于 max_distance 的所有节点及其距离。

#     参数：
#       G: NetworkX 图
#       start_node: 起始节点
#       max_distance: 最大距离（包含此距离）的节点将被返回

#     返回：
#       一个列表，列表中的每个元素是 (节点, 距离) 元组
#     """
#     visited = set()
#     queue = deque([(start_node, 0)])
#     result = []
    
#     while queue:
#         node, dist = queue.popleft()
#         if node in visited:
#             continue
#         visited.add(node)
        
#         # 只保存距离在 max_distance 以内的节点
#         if dist <= max_distance:
#             result.append((node, dist))
#         else:
#             # 如果当前节点距离已超过 max_distance，就无需扩展其邻居
#             continue

#         # 如果当前距离还未达到最大值，则将其邻居加入队列
#         if dist < max_distance:
#             for neighbor in G.neighbors(node):
#                 if neighbor not in visited:
#                     queue.append((neighbor, dist + 1))
    
#     return result

# # 示例：假设图 G 已经构建，并且存在关键词节点 "fading channels"
# start_keyword = "words"
# nodes_within_5 = find_nodes_within_distance(G, start_keyword, max_distance=5)

# print("距离节点 '{}' 5以内的所有节点:".format(start_keyword))
# for node, distance in nodes_within_5:
#     print(f"节点: {node}, 距离: {distance}")

