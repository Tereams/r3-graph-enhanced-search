from neo4j import GraphDatabase
import json

# 定义 Neo4j 驱动类
class Neo4jHandler:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self.driver.close()
    
    def create_graph(self, data):
        with self.driver.session() as session:
            for record in data:
                # 使用 execute_write 替换 write_transaction
                session.execute_write(self._create_title_and_keywords, record)
    
    @staticmethod
    def _create_title_and_keywords(tx, record):
        title = record['title']
        keywords = record['keywords']
        
        # 创建 Title 节点
        tx.run("MERGE (t:Title {name: $title})", title=title)
        
        for keyword in keywords:
            # 创建 Keyword 节点
            tx.run("MERGE (k:Keyword {name: $keyword})", keyword=keyword)
            
            # 创建关系
            tx.run("""
                MATCH (t:Title {name: $title})
                MATCH (k:Keyword {name: $keyword})
                MERGE (t)-[:HAS_KEYWORD]->(k)
            """, title=title, keyword=keyword)

# 从 JSONL 文件读取数据
def load_jsonl(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data.append(json.loads(line))
    return data

# 主函数
def main():
    # 设置你的 Neo4j 数据库连接信息
    uri = "bolt://localhost:7687"  # 替换为你的 Neo4j 地址
    user = "neo4j"                 # 替换为你的用户名
    password = "FFR3"          # 替换为你的密码
    
    # JSONL 文件路径
    file_path = "output.jsonl"
    
    # 加载 JSONL 数据
    data = load_jsonl(file_path)
    
    # 初始化 Neo4j 处理器
    neo4j_handler = Neo4jHandler(uri, user, password)
    
    # 将数据导入 Neo4j
    neo4j_handler.create_graph(data)
    
    # 关闭连接
    neo4j_handler.close()
    print("数据已成功导入 Neo4j 数据库！")

if __name__ == "__main__":
    main()
