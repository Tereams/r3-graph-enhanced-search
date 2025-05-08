import networkx as nx
from apr import find_all_frequent_itemsets
from bm25 import query_bm25
from graph_retrieve import find_nodes_within_distance
from initializer import initialize_data

# 初始化数据
data = initialize_data()
cached_data = data["cached_data"]
candidate_keywords = data["candidate_keywords"]
tokenized_keywords = data["tokenized_keywords"]
df_dict = data["df_dict"]
N = data["N"]
avgdl = data["avgdl"]
G = data["graph"]
title_index=data["title_index"]
keyword_index=data["keyword_index"]

# 输入查询
query = "machine learning"
keywords = query_bm25(query, candidate_keywords, tokenized_keywords, df_dict, N, avgdl)

# 基于关键词节点在图中搜索
res = {}
for kw in keywords:
    if kw not in keyword_index:
        continue  # 忽略图中不存在的关键词节点
    # id_k = G.nodes[kw].get('index')
    id_k = keyword_index[kw]
    nodes_within_5 = find_nodes_within_distance(G, id_k, max_distance=3)
    res[id_k] = nodes_within_5

# 收集所有节点 id
all_ids = set()
for lst in res.values():
    for id_, dis in lst:
        all_ids.add(id_)

# 计算总距离
result = {}
for id_ in all_ids:
    total_distance = 0
    for lst in res.values():
        total_distance += next((dis for cur_id, dis in lst if cur_id == id_), 7)
    result[id_] = total_distance

# # 排序输出
# sorted_result = sorted(result.items(), key=lambda x: x[1])
# print("Sorted node IDs by total distance:")
# for id_, dist in sorted_result:
#     print(f"ID: {id_}, Total Distance: {dist}")

# 映射：节点 ID -> 命中关键词索引
paperID_to_keyIDs = {}
for key, lst in res.items():
    for id_, dis in lst:
        if id_ in paperID_to_keyIDs:
            paperID_to_keyIDs[id_].append(key)
        else:
            paperID_to_keyIDs[id_] = [key]

# print("\nID to Keyword Index Mapping:")
# for id_, keys in paperID_to_keyIDs.items():
#     print(f"ID: {id_}, Related Keyword Node Indices: {keys}")


def get_paths_from_node(paper_id: int):
    if paper_id not in paperID_to_keyIDs:
        return {"error": "This node was not part of the last search results."}

    keyword_indices = paperID_to_keyIDs[paper_id]
    paths = []
    query_name = G.nodes[paper_id].get("name", "")
    query_uri = ""
    for row in cached_data:
        if row.get("id") == paper_id:
            query_uri = row.get("dc.identifier.uri[en_US]", "")

    for kwd_id in keyword_indices:
        try:
            path_nodes = nx.shortest_path(G, source=paper_id, target=kwd_id)
            path_info = []
            for id in path_nodes[1:]:
                name = G.nodes[id].get("name", "")
                type = G.nodes[id].get("type", "")

                # 查找cached_data中该节点对应的URI
                uri = ""
                if type == "title":
                    for row in cached_data:
                        if row.get("id") == id:
                            uri = row.get("dc.identifier.uri[en_US]", "")
                            break

                path_info.append({
                    "name": name,
                    "label": type,
                    "uri": uri if type == "title" else None
                })

            paths.append(path_info) 
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            paths.append([]) 

    return {
        "query_name": query_name,
        "query_uri": query_uri,
        "paths": paths
    }

# ress=get_paths_from_node("147d07ef-fe0f-4054-8592-a5f9ea552109")
# print(ress)
def get_frequent_pattern_with_details() -> dict:
    """
    找到最大频繁 keyID 集合及对应的 paperID 集合，并返回详细的节点信息（含日期排序）。

    返回：
        {
            "key_nodes": List[{"id", "name", "type"}],
            "paper_nodes": List[{"id", "name", "type", "date"}]
        }
    """
    transactions = [set(keyIDs) for keyIDs in paperID_to_keyIDs.values()]
    frequent_itemsets = find_all_frequent_itemsets(transactions)

    if not frequent_itemsets:
        return {"key_nodes": [], "paper_nodes": []}

    max_itemset, _ = max(frequent_itemsets, key=lambda x: (len(x[0]), x[1]))
    keyID_set = set(max_itemset)
    matching_paperIDs = [pid for pid, keyIDs in paperID_to_keyIDs.items() if keyID_set.issubset(set(keyIDs))]

    def get_node_info(node_id):
        return {
            "name": G.nodes[node_id].get("name", ""),
            "type": G.nodes[node_id].get("type", "")
        }

    def get_paper_info(paper_id):
        name = G.nodes[paper_id].get("name", "")
        type_ = G.nodes[paper_id].get("type", "")
        date = ""
        for row in cached_data:
            if row.get("id") == paper_id:
                date = row.get("dc.date.issued[en_US]", "")
                break
        return {
            "name": name,
            "type": type_,
            "date": date
        }

    key_nodes = [get_node_info(kid) for kid in keyID_set if kid in G]
    paper_nodes = [get_paper_info(pid) for pid in matching_paperIDs if pid in G]

    # 根据日期排序（默认升序）
    paper_nodes.sort(key=lambda x: x["date"])

    return {
        "key_nodes": key_nodes,
        "paper_nodes": paper_nodes
    }

print(get_frequent_pattern_with_details())