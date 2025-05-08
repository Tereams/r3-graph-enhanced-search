import itertools

def apriori(transactions, min_support=1):
    """
    使用 Apriori 算法挖掘所有频繁项集。
    transactions: 事务列表，每个事务是一个集合，例如：[{40}, {40, 356}, ...]
    min_support: 最小支持度（这里设置为1，即只要出现过就算频繁）
    返回值: 一个列表，每个元素是一个字典，存储该层频繁项集及其支持度。
    """
    # 生成1-项集候选集
    C1 = {}
    for t in transactions:
        for item in t:
            itemset = frozenset([item])
            C1[itemset] = C1.get(itemset, 0) + 1
    # 过滤掉支持度低于阈值的1-项集
    L1 = {itemset: count for itemset, count in C1.items() if count >= min_support}
    frequent_itemsets = [L1]
    k = 2  # 接下来生成2-项集、3-项集……
    
    while True:
        prev_freq_itemsets = list(frequent_itemsets[-1].keys())
        candidate_set = set()
        # 自连接：生成大小为 k 的候选项集
        for i in range(len(prev_freq_itemsets)):
            for j in range(i + 1, len(prev_freq_itemsets)):
                union_set = prev_freq_itemsets[i] | prev_freq_itemsets[j]
                if len(union_set) == k:
                    candidate_set.add(union_set)
        # 剪枝：如果候选项集的任一 (k-1) 子集不在上层频繁项集中，则剪去
        candidate_set = {candidate for candidate in candidate_set 
                         if all(frozenset(subset) in frequent_itemsets[-1] 
                                for subset in itertools.combinations(candidate, k - 1))}
        # 统计候选项集的支持度
        current_level = {}
        for candidate in candidate_set:
            support = sum(1 for t in transactions if candidate.issubset(t))
            if support >= min_support:
                current_level[candidate] = support
        # 如果当前层没有候选项集，则退出循环
        if not current_level:
            break
        frequent_itemsets.append(current_level)
        k += 1

    return frequent_itemsets

def find_all_frequent_itemsets(transactions):
    """
    返回所有满足以下条件的频繁项集：
      - 项集长度大于 1
      - 支持度大于 1
    返回值为一个列表，每个元素为 (项集, 支持度) 的元组
    """
    freq_itemsets = apriori(transactions, min_support=1)
    result = []
    for level in freq_itemsets:
        for itemset, support in level.items():
            if len(itemset) > 1 and support > 1:
                result.append((itemset, support))
    return result

if __name__ == "__main__":
    # 输入字典：键不重要，值为事务的列表
    input_dict = {
        21: [40],
        89: [40],
        338: [40],
        544: [40, 356],
        548: [40],
        1110: [40, 356],
        138: [40],
        80: [40],
        422: [40],
        738: [40],
        991: [40],
        691: [40],
        771: [40],
        794: [40],
        721: [40],
        101: [40, 356],
        784: [40, 356],
        838: [40, 356],
        878: [40, 356],
        38: [40],
        191: [40],
        202: [40],
        274: [40],
        651: [40],
        797: [40],
        195: [40, 356],
        1220: [40],
        139: [40],
        1095: [3815],
        204: [3815],
        823: [3815],
        496: [795],
        610: [795],
        1345: [795],
        169: [795],
        871: [795],
        1190: [795]
    }
    
    # 将字典的 value 转换为集合列表，作为事务数据
    transactions = [set(v) for v in input_dict.values()]
    
    results = find_all_frequent_itemsets(transactions)
    if results:
        for itemset, support in results:
            print("频繁项集:", set(itemset), "支持度:", support)
    else:
        print("没有找到满足条件的频繁项集。")
