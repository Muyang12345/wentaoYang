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
    #index取1-25随机整数
    index = random.randint(1, 25)
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
file_path = 'C:\\Users\\13377\\PycharmProjects\\pythonProject\\1.xlsx' # Change this to your actual file path
products = read_excel_file(file_path)
print_product_details(products, 100)  # Replace 1 with any other product index to get its details
print(print_product_details(products, 100) )