import math
import heapq
import re

# 定义简单的英文分词函数，利用正则表达式提取单词，全部转为小写
def tokenize(text):
    return re.findall(r'\w+', text.lower())

# 定义 BM25 评分函数
def bm25_score(doc, query_tokens, df, N, avgdl, k1=1.5, b=0.75):
    score = 0.0
    doc_len = len(doc)
    for term in query_tokens:
        freq = doc.count(term)
        if freq == 0:
            continue
        term_df = df.get(term, 0)
        idf = math.log((N - term_df + 0.5) / (term_df + 0.5) + 1)
        score += idf * (freq * (k1 + 1)) / (freq + k1 * (1 - b + b * doc_len / avgdl))
    return score

def query_bm25(query, candidate_keywords, tokenized_keywords, df, N, avgdl):
    query_tokens = tokenize(query)
    scores = [
        bm25_score(doc, query_tokens, df, N, avgdl)
        for doc in tokenized_keywords
    ]
    top10_indices = heapq.nlargest(10, range(len(scores)), key=lambda i: scores[i])
    top10_keywords = [candidate_keywords[i] for i in top10_indices if scores[i] > 0]
    return top10_keywords
