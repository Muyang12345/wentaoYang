from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import MessageGraph, END

# 扩展问题
# 直播间交互{输入 输出}
# 问题：

cm_info = '''
    女士尺寸	XS	S	M	L	XL
身高	155-160	158-168	160-168	160-170	160-170
体重	85-95	110-120	120-130	130以上	140以上
'''
import random
import pandas as pd


# Function to read the Excel file
def read_excel_file(filepath):
    # Read the Excel file
    df = pd.read_excel(filepath)

    # Create a dictionary to hold the product data
    products = {}

    # Temporary variables to hold the current main product data
    current_index = None
    current_product = {}

    # Iterate through the dataframe rows
    for idx, row in df.iterrows():
        if pd.notna(row['序号']):  # This is a new main product
            if current_index is not None:
                products[current_index] = current_product  # Store the completed product

            # Start a new main product
            current_index = int(row['序号'])
            current_product = {
                '商品id': row['商品id'],
                '标题': row['标题'],
                '商品链接': row['商品链接'],
                'skus': []
            }

        # Append SKU data to the current main product
        if pd.notna(row['SKUID']):
            sku_data = {
                'SKUID': row['SKUID'],
                'sku名称': row['sku名称'],
                '价格': row.get('价格', 'N/A'),  # Add price information
                '库存': row.get('库存', 'N/A')  # Add inventory information
            }
            current_product['skus'].append(sku_data)

    # Add the last product to the dictionary
    if current_index is not None:
        products[current_index] = current_product

    return products


# Function to print product details by index
def print_product_details(products, index):
    # index取1-25随机整数
    # index = random.randint(1, 25)
    index = 24
    product = products.get(index)
    if product:
        print("Main Product Details:")
        print(f"商品id: {product['商品id']}")
        print(f"标题: {product['标题']}")
        print(f"商品链接: {product['商品链接']}")
        for sku in product['skus']:
            print("SKU Details:")
            print(f"SKUID: {sku['SKUID']}")
            print(f"sku名称: {sku['sku名称']}")
            print(f"价格: {sku['价格']}")  # Print price information
            print(f"库存: {sku['库存']}")  # Print inventory information
    else:
        print("Product not found.")
    output = []
    product = products.get(index)
    if product:
        output.append("Main Product Details:")
        output.append(f"商品id: {product['商品id']}")
        output.append(f"标题: {product['标题']}")
        output.append(f"商品链接: {product['商品链接']}")
        for sku in product['skus']:
            output.append("SKU Details:")
            output.append(f"SKUID: {sku['SKUID']}")
            output.append(f"sku名称: {sku['sku名称']}")
            output.append(f"价格: {sku['价格']}")  # Print price information
            output.append(f"库存: {sku['库存']}")  # Print inventory information
    else:
        output.append("not found")

    return "\n".join(output)


# Usage
file_path = 'C:\\Users\\13377\\PycharmProjects\\pythonProject\\1.xlsx'  # Change this to your actual file path
products_all = read_excel_file(file_path)
print_product_details(products_all, 100)  # Replace 1 with any other product index to get its details
print(print_product_details(products_all, 100))

# 读取 Excel 文件
df = pd.read_excel(file_path, engine='openpyxl')

# 打印原始数据框架以理解其结构
print(df)

# 根据需要处理数据
# 假设每个序号对应多行，并且这些行具有相同的商品 ID 和标题，但具有不同的 SKUID 和 sku 名称

# 创建一个字典来存储每个序号的所有信息
products = {}

# 遍历数据框架的每一行
for index, row in df.iterrows():
    item_number = row['序号']
    if item_number not in products:
        products[item_number] = {
            '商品id': row['商品id'],
            '标题': row['标题'],
            '商品链接': row['商品链接'],
            'SKUs': []
        }

    # 添加 SKU 信息
    products[item_number]['SKUs'].append({
        'SKUID': row['SKUID'],
        'sku名称': row['sku名称'],
        'sku备注': row['sku备注'] if 'sku备注' in row else None  # 确保列存在
    })

# 输出序号为 1 的产品信息
print(products[1])

# 初始化ChatOpenAI模型
inference_server_url = "http://119.188.113.120:1180/v1"
model = ChatOpenAI(
    model="qwen",
    openai_api_key="none",
    openai_api_base=inference_server_url,
    max_tokens=150,
    temperature=0,
    streaming=True,
    # use_streaming=True,
    # use_stream=True,
    # stream=True
)


def create_message_graph():
    graph = MessageGraph()

    # router 问题分类：1品类相关问题：{衣服{尺码、库存{暂无法回答}，其他（其他品类（颜色标识））} 2。由主播回答 3。暂不回答
    # rag
    def categorize_question(messages):
        # last_user_message = messages[-1].content
        # category_response = model(
        #     [HumanMessage(
        #         content=f"分类这个问题：{last_user_message}，品类有{{衣服，其他}}，请只返回问题对应的品类，只有两个字: ")])
        # category_content = category_response.content if isinstance(category_response,
        #                                                            list) else category_response.content
        # category = "clothing" if "衣服" in category_content else "other"
        # return category

        last_user_message = messages[-1].content
        category_response = model(
            [HumanMessage(
                content=f"你是一个直播ai，代替主播看弹幕，请先分类这个问题：{last_user_message}，分别是"
                        f"1.品类相关问题（衣服、保健品、其他）"
                        f"2.由主播回答的问题(如“你穿的几码;上周你去哪了”)"
                        f"3.询问商品信息的问题(如49号链接胸围多少;54看看;51号链接看看;)，"
                        f"4.其他问题"
                        f"请回答{{"
                        f"品类，主播，其他}}中的一个，尺码问题属于品类，请只返回问题对应的类型，你的回答只有两个字: ")])
        category_content = category_response.content if isinstance(category_response,
                                                                   list) else category_response.content

        if "品类" in category_content:
            return "pinlei"
        elif "主播" in category_content:
            return "host"
        elif "其他" in category_content:
            return "other"
        return "other"

    def item_categorize_question(messages):
        last_user_message = messages[0].content
        category_response = model(
            [HumanMessage(
                content=f"分类这个问题：{last_user_message}，品类有{{衣服，其他}}，请只返回问题对应的品类，只有两个字: ")])
        category_content = category_response.content if isinstance(category_response,
                                                                   list) else category_response.content
        category = "clothing" if "衣服" in category_content else "other"

        print("item_categorize_question", category_content + " " + last_user_message)
        return category

    # 衣服品类问题处理节点
    def clothing_handler(messages):

        last_user_message = messages[0].content
        category_response = model(
            [HumanMessage(
                content=f"分类这个问题：{last_user_message}，类型有询问商品信息(如49号链接胸围多少;54看看;51号链接看看;)、身高体重对应穿衣尺码相关问题，{{尺码，商品信息，其他}}，请只返回列表里的一项: ")])
        category_content = category_response.content if isinstance(category_response,
                                                                   list) else category_response.content
        print("clothing_handler", category_content + " " + last_user_message)
        if "尺码" in category_content:
            return model([HumanMessage(
                content=f"你是一个直播ai客服，根据尺码表{cm_info}礼貌简短回答身高体重的尺码问题，如果无法回答请回答请提供身高和体重: {last_user_message}")])
        elif "信息" in category_content:
            # return [HumanMessage(content="库存问题暂无法回答")]
            # category_response = model(
            #     [HumanMessage(
            #         content=f"提取商品链接：{last_user_message}，商品链接是一个数字，请只回答这个数字：")])
            # category_content = category_response.content if isinstance(category_response,
            #                                                            list) else category_response.content
            # #提取category_content中的数字
            import re
            category_content = re.findall(r"\d+", last_user_message)
            print("category_content", category_content)
            item_info = print_product_details(products_all, 1)
            return model([HumanMessage(
                content=f"你是一个直播ai客服，用户问题是 {last_user_message}，所需要的商品信息提供给你是{item_info}，请礼貌简短回答问题，如果无法回答请礼貌拒绝:")])
        return [HumanMessage(content="衣服品类其他问题暂无法回答")]

    def cloth_other_handler(messages):

        return [HumanMessage(content="该品类类型问题暂无法回答")]

    def other_handler(messages):
        return [HumanMessage(content="暂无法回答类型问题")]

    def host_handler(messages):
        # last_user_message = " ".join([msg.content for msg in messages])
        # print("last_user_message", last_user_message)
        return [HumanMessage(content="请由主播回答问题")]

    def router(messages):
        category = messages[-1].content
        if category == "clothing":
            return "clothing"
        if category == "other":
            return "other"
        return 'END'

    def router1(messages):
        category = messages[-1].content
        if category == "pinlei":
            return "pinlei"
        if category == "host":
            return "host"
        if category == "other":
            return "other"
        return 'END'

    # 添加节点
    graph.add_node("categorizer", categorize_question)
    graph.add_node("clothing", clothing_handler)
    graph.add_node("other", other_handler)
    graph.add_node("host", host_handler)
    graph.add_node("item_categorizer", item_categorize_question)
    graph.add_node("cloth_other", cloth_other_handler)

    # 设定图的入口点
    graph.set_entry_point("categorizer")
    graph.add_conditional_edges("categorizer", router1, {
        "pinlei": "item_categorizer",
        "host": "host",
        "other": "other",
        'END': END
    })
    graph.add_conditional_edges("item_categorizer", router, {
        "clothing": "clothing",
        "other": "cloth_other",
        'END': END
    })
    # 添加边和过渡条件

    graph.add_edge("clothing", END)
    graph.add_edge("other", END)
    graph.add_edge("host", END)
    graph.add_edge("cloth_other", END)

    # 编译图
    return graph.compile()


def process_customer_inquiry(content):
    runnable = create_message_graph()

    return runnable.invoke([HumanMessage(content=content)])


if __name__ == "__main__":
    user_input = "我94，112斤"
    # response = process_customer_inquiry(user_input)
    # print(response)

    # for output in process_customer_inquiry(user_input):
    #     # stream() yields dictionaries with output keyed by node name
    #     for key, value in output.items():
    #         print(f"Output from node '{key}':")
    #         print("---")
    #         if isinstance(value, str):
    #             print(value)
    #         else:
    #             print(value[0].content)
    #         print("\n---\n")
