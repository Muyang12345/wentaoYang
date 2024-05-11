import pandas as pd

# 读取csv文件
df = pd.read_csv("comments42.csv")
df = df.sort_values(by='Comment Time')


# 保存到新的Excel文件
df.to_excel('cleaned_data_comments.xlsx', index=False)