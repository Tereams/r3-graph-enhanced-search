import warnings
import pandas as pd
import json

from tqdm import tqdm
from transformers import (
    Text2TextGenerationPipeline,
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
)

# 忽略警告
# warnings.filterwarnings("ignore", message="torch.utils._pytree._register_pytree_node")

# 定义关键词生成管道
class KeyphraseGenerationPipeline(Text2TextGenerationPipeline):
    def __init__(self, model, keyphrase_sep_token=";", *args, **kwargs):
        super().__init__(
            model=AutoModelForSeq2SeqLM.from_pretrained(model),
            tokenizer=AutoTokenizer.from_pretrained(model),
            *args,
            **kwargs
        )
        self.keyphrase_sep_token = keyphrase_sep_token

    def postprocess(self, model_outputs):
        results = super().postprocess(
            model_outputs=model_outputs
        )
        return [[keyphrase.strip() for keyphrase in result.get("generated_text").split(self.keyphrase_sep_token) if keyphrase != ""] for result in results]

# 加载模型
model_name = "pretrained\keyphrase-generation-t5-small-inspec"
generator = KeyphraseGenerationPipeline(model=model_name, max_new_tokens=50)

# 读取 CSV 文件
csv_file = "R3.csv"  # 替换为你的 CSV 文件路径
df = pd.read_csv(csv_file)

# 创建 JSONL 文件
output_file = "output.jsonl"
with open(output_file, "w", encoding="utf-8") as jsonl_file:
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Processing"):
        article_id = row["id"]  # 假设 CSV 文件中有 id 列
        title = row["title"]  # 假设 CSV 文件中有 title 列
        abstract = row["abstract"]  # 假设 CSV 文件中有 abstract 列
        

        if pd.isna(abstract):
            continue

        # 使用模型生成关键词
        keyphrases = generator(abstract)
        
        # 构建 JSON 对象
        output_data = {
            "id": article_id,
            "title": title,
            "keywords": keyphrases[0] if keyphrases else []
        }
        
        # 写入 JSONL 文件
        jsonl_file.write(json.dumps(output_data, ensure_ascii=False) + "\n")

print(f"关键词提取完成，结果已保存到 {output_file}")
