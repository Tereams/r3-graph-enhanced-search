import json
import pandas as pd
import networkx as nx
from bm25 import tokenize

def initialize_data():
    try:
        # 读取 CSV 数据
        df = pd.read_csv("filtered_data.csv")
        cached_data = df.to_dict(orient="records")

        # 读取关键词文件
        candidate_keywords = []
        with open('new_kwds1.txt', 'r', encoding='utf-8') as f:
            for line in f:
                l = line.strip()
                if l:
                    candidate_keywords.append(l)

        # 关键词分词
        tokenized_keywords = [tokenize(keyword) for keyword in candidate_keywords]
        N = len(tokenized_keywords)
        avgdl = sum(len(doc) for doc in tokenized_keywords) / N if N > 0 else 0

        # 文档频率字典
        df_dict = {}
        for doc in tokenized_keywords:
            seen = set()
            for token in doc:
                if token not in seen:
                    df_dict[token] = df_dict.get(token, 0) + 1
                    seen.add(token)

        
        with open('title_index.json', 'r', encoding='utf-8') as f:
            title_index = json.load(f)

        # 读取 index_keyword.json
        with open('keyword_index.json', 'r', encoding='utf-8') as f:
            keyword_index = json.load(f)

        # 缓存图结构
        G = nx.read_gml('graph3.gml')

        return {
            "cached_data": cached_data,
            "candidate_keywords": candidate_keywords,
            "tokenized_keywords": tokenized_keywords,
            "df_dict": df_dict,
            "N": N,
            "avgdl": avgdl,
            "graph": G,
            "title_index":title_index,
            "keyword_index":keyword_index
        }

    except Exception as e:
        print(f"[Init Error] {e}")
        return {
            "cached_data": [],
            "candidate_keywords": [],
            "tokenized_keywords": [],
            "df_dict": {},
            "N": 0,
            "avgdl": 0,
            "graph": nx.Graph(),  # 返回空图
            "title_index":{},
            "keyword_index":{}
        }
