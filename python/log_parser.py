import re
from datetime import datetime, date
import time



def getTodayUrl():
    # 获取当前日期
    target_date = date.today()

    # 创建一个空字典
    addr_url_map = {}
    # 打开文件
    with open('path', 'r') as file:
        # 逐行读取文件内容
        for line in file:
            # 使用正则表达式匹配行数据
            match = re.search(r't=(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{4}) lvl=info msg="started tunnel" obj=tunnels name=[a-zA-Z]+ addr=([^ ]+) url=([^ ]+)', line)
            if match:
                # 提取地址和URL属性
                date_str = match.group(1)
                addr = match.group(2)
                url = match.group(3)
                # 将日期字符串转换为日期对象
                cur_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S%z').date()
                if cur_date != target_date:
                    continue
                # 将地址和URL存储到字典中
                addr_url_map[addr] = url
    return addr_url_map

def getUrl():
    retryCount = 0;
    maxRetryCount = 20;
    url = ''
    while True:
        url = getTodayUrl()
        if(not url):
            retryCount += 1
        if(url or retryCount == maxRetryCount):
            break
        time.sleep(1)
    return str(url) if url else "未获取到数据";    