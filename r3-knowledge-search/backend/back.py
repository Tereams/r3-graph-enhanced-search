import pandas as pd
import networkx as nx
from fastapi import FastAPI
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from neo4j import GraphDatabase

from apr import find_all_frequent_itemsets
from bm25 import query_bm25
from graph_retrieve import find_nodes_within_distance
from initializer import initialize_data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化所有缓存数据
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

paperID_to_keyIDs={}

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "FFR3"

neo4j_driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

@app.get("/neo4j/default", response_model=dict)
async def get_default_neo4j_graph():
    with neo4j_driver.session() as session:
        result = session.run("""
            MATCH (n)-[r]-(m)
            WITH n, r, m LIMIT 50
            RETURN id(n) AS source_id, properties(n) AS source_props, labels(n) AS source_labels,
                   id(m) AS target_id, properties(m) AS target_props, labels(m) AS target_labels,
                   type(r) AS rel_type
        """)

        nodes = {}
        links = []
        for record in result:
            for prefix in ['source', 'target']:
                node_id = record[f"{prefix}_id"]
                if node_id not in nodes:
                    nodes[node_id] = {
                        "id": node_id,
                        "name": record[f"{prefix}_props"].get("name", f"{prefix}_{node_id}"),
                        "labels": record[f"{prefix}_labels"],
                        "properties": record[f"{prefix}_props"]
                    }
            links.append({
                "source": record["source_id"],
                "target": record["target_id"],
                "type": record["rel_type"]
            })

        return {"nodes": list(nodes.values()), "links": links}

@app.get("/neo4j/search", response_model=dict)
async def search_subgraph(query: str = Query(..., min_length=1)):
    with neo4j_driver.session() as session:
        result = session.run("""
            MATCH path = (n)-[*..1]-(m)
            WHERE toLower(n.name) CONTAINS toLower($query)
            RETURN nodes(path) AS ns, relationships(path) AS rs
        """, parameters={"query": query})

        nodes = {}
        links = []

        for record in result:
            for node in record["ns"]:
                nid = node.id
                if nid not in nodes:
                    nodes[nid] = {
                        "id": nid,
                        "name": node.get("name", f"node_{nid}"),
                        "labels": list(node.labels),
                        "properties": dict(node)
                    }

            for rel in record["rs"]:
                links.append({
                    "source": rel.start_node.id,
                    "target": rel.end_node.id,
                    "type": rel.type
                })

        return {
            "nodes": list(nodes.values()),
            "links": links
        }

def get_frequent_pattern():
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

@app.get("/search", response_model=dict)
async def search(query: str):
    if not query:
        return []

    keywords = query_bm25(query, candidate_keywords, tokenized_keywords, df_dict, N, avgdl)

    # 基于关键词节点在图中搜索
    raw_result = {}
    for kw in keywords:
        if kw not in keyword_index:
            continue  # 忽略图中不存在的关键词节点
        # id_k = G.nodes[kw].get('index')
        id_k = keyword_index[kw]
        nodes_within_5 = find_nodes_within_distance(G, id_k, max_distance=3)
        raw_result[id_k] = nodes_within_5

    # 收集所有节点 id
    all_ids = set()
    for lst in raw_result.values():
        for id_, dis in lst:
            all_ids.add(id_)

    # 计算总距离
    sum_result = {}
    for id_ in all_ids:
        total_distance = 0
        for lst in raw_result.values():
            total_distance += next((dis for cur_id, dis in lst if cur_id == id_), 7)
        sum_result[id_] = total_distance

    sorted_result = sorted(sum_result.items(), key=lambda x: x[1])
    id_list = [i[0] for i in sorted_result]

    qresult = [record for record in cached_data if record['id'] in id_list]

    global paperID_to_keyIDs
    paperID_to_keyIDs = {}
    for key, lst in raw_result.items():
        for id_, dis in lst:
            if id_ in paperID_to_keyIDs:
                paperID_to_keyIDs[id_].append(key)
            else:
                paperID_to_keyIDs[id_] = [key]

    freq_graph=get_frequent_pattern()

    return {
        'list': qresult,
        'freq_graph': freq_graph
    }

@app.get("/path/{paper_id}", response_model=dict)
async def get_paths_from_node(paper_id: str):
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

