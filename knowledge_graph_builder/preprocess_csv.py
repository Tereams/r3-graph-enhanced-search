import pandas as pd

def filter_columns_by_non_empty_ratio(file_path, output_path="filtered_data.csv"):
    """
    过滤 CSV 文件中非空占比大于 0.8 的列，并保存筛选后的数据
    """
    df = pd.read_csv(file_path, dtype=str)  # 以字符串格式读取，避免数据类型问题
    total_counts = len(df)

    # 计算每列非空元素数量
    non_empty_counts = df.apply(lambda col: col.str.strip().replace('', None).dropna().count())

    # 计算占比
    non_empty_ratio = (non_empty_counts / total_counts).round(4)

    # 选取占比 > 0.8 的列
    selected_columns = non_empty_ratio[non_empty_ratio > 0.8].index

    # 仅保留符合条件的列
    filtered_df = df[selected_columns]
    # 将空值（包括空字符串和仅含空格的值）替换为 'not available'
    filtered_df = filtered_df.applymap(lambda x: "not available" if pd.isna(x) or str(x).strip() == "" else x)

    # 保存到新的 CSV 文件
    filtered_df.to_csv(output_path, index=False)
    
    print(f"筛选后的数据已保存至 {output_path}")

    return filtered_df

# 示例调用
if __name__ == "__main__":
    file_path = "R3-Engineering_2025-01-22.csv"  # 替换为你的 CSV 文件路径
    filter_columns_by_non_empty_ratio(file_path)
