import pandas as pd

# 读取csv文件
df = pd.read_csv("huoyue42.csv")

# 清洗Username列，去掉时间
df['Username'] = df['Username'].str.split(' ').str[0].replace(r'(未关注|新客|老客)\s*', '', regex=True)

# 清洗label列，只保留括号内的内容
df['label'] = df['label']

# 清洗action列，只保留如“从推荐来了”
df['action'] = df['action']

# 保存到新的Excel文件
df.to_excel('cleaned_data_huoyue.xlsx', index=False)