import csv
from datetime import datetime
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")
driver = webdriver.Chrome(options=chrome_options)

# chrome.exe --remote-debugging-port=9223 --user-data-dir="D:\selenum\AutomationProfile"
# 导航到目标页面
driver.get('https://liveplatform.taobao.com/restful/index/live/control?liveId=455518116401')
# 获取当前时间
current_time = datetime.now()
formatted_time = current_time.strftime('%Y%m%d%H%M')
# 修改CSV文件名以包含当前日期和时间
csv_path = f'huoyue{formatted_time}.csv'
csv_headers = ['Username', 'label', 'Time', 'action']
with open(csv_path, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(csv_headers)
# 初始化用户数据映射
users_data = {}
try:
    seen_comments = set()  # 存储已经看到的评论的标识符，以避免重复

    while True:  # 持续监控直到手动停止
        # 假设 html_content 是您提供的 HTML 字符串
        sleep(1)
        try:
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            users = soup.find_all(class_="UserItem--container--3i5QlMh")
            print(len(users))
            for user in users:
                user_name = user.find(class_="UserItem--userName--3zArOw2").text.strip()
                labels = [label.span.text for label in user.find_all(class_="UserItem--label--2gf-Y3-")]
                message_time = user_name.split()[-1]
                messages = user.find_all(class_="UserItem--message--3i_wZS_")
                message_texts = [message.div.text for message in messages if message.div]

                print(f"用户名: {user_name}")
                print(f"标签: {labels}")
                print(f"消息时间: {message_time}")
                for message_text in message_texts:
                    print(f"消息内容: {message_text}")
                print("-" * 20)

                comment_id = f"{user_name}_{message_texts}_{message_time}"
                if comment_id not in seen_comments:
                    seen_comments.add(comment_id)
                    # 将当前日期添加到评论时间中
                    full_comment_time = f"{current_time.strftime('%Y-%m-%d')} {message_time}"

                    # 将评论信息保存到CSV文件
                    with open(csv_path, 'a', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow([user_name, labels, full_comment_time, message_texts])
                    print(f"Added: {user_name}, {labels}, {full_comment_time}, {message_texts[0]}")
        except:
            print("Error extracting comment details")
finally:
    driver.quit()
#
# sleep(5)
# users = driver.find_elements(By.CLASS_NAME, "UserItem--container--3i5QlMh")
# for user in users:
#     # 使用ActionChains模拟鼠标移动到容器上
#     print(1)
#     ActionChains(driver).move_to_element(user).click().perform()
#     sleep(1)
#     # 等待“显示详情”按钮出现并点击
#
#     # details_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "UserItem--mask--1W2p1Wf")))
#     # details_button.click()
#     # details_button = EC.element_to_be_clickable((By.CSS_SELECTOR, "UserItem--mask--1W2p1Wf"))
#     # details_button.click()
#
#     # 等待详情信息加载
#     # details_loaded = (EC.presence_of_element_located((By.CSS_SELECTOR, ".tbla-tual-drawer-body")))
#
#     # 使用BeautifulSoup提取详情内容
#     html_content = driver.page_source
#
#     soup = BeautifulSoup(html_content, 'html.parser')
#     # 选择器针对消息容器进行了调整
#     details_content = soup.select(".tbla-tual-timeline-item")
#     print(2)
#     name = soup.find(class_="UserDrawer--title--2TDtUth").text
#     print(f"用户: {name}")
#     for detail in details_content:
#         # 提取并打印消息时间和消息文本
#         time = detail.find("span").text
#         text = detail.find(class_="UserItem--text--JV5ApC2").text
#         print(f"时间: {time}, 消息: {text}")
#
#     close = driver.find_elements(By.CLASS_NAME, "tbla-tual-drawer-close")
#
#     print(3)
#
#     ActionChains(driver).move_to_element(close[0]).click().perform()
#     sleep(1)
