import requests
from datetime import datetime, timedelta
import json
import os
import time
from get_task_list import get_task_list
from login import login
from config import BASE_URL, LANGUAGE_LIST, TRANSLATION_DIR, DEFAULT_HEADERS, LOGIN_CONFIG

def download_report(accept_language='', base_url='', params=None):
    """
    调用获取统计概览导出接口，并下载生成的报表文件
    
    Args:
        accept_language (str): 接受的语言代码，如'zh-CN', 'en'等
        base_url (str): API的基础URL地址
        params (dict): 请求参数，包含导出配置信息
        method (str): 请求方法，'get'或'post'，默认为'get'
    
    Returns:
        str: 保存的文件路径，如果失败则返回None
    """
    # 获取当前任务列表，用于后续对比找出新建的任务
    old_task_list = get_task_list()

    # 设置请求头信息
    headers = {
        'Token':login(accept_language=accept_language),
        'Accept-Language': accept_language,
        'User-Agent': 'python-requests/2.31.0'
    }

    try:
        # 根据指定的方法发送请求
        response = requests.get(base_url, headers=headers, params=params)
        if not response.ok:
            response = requests.post(base_url, headers=headers, json=params)
      

        # 循环检查任务状态，直到获取到下载URL
        new_task_list = get_task_list()
        latest_task = new_task_list - old_task_list
        while(1):
            new_task_list = get_task_list()
            # 找出新创建的任务
            latest_task = new_task_list - old_task_list
            # 当任务完成且有下载URL时退出循环
            if latest_task and list(latest_task)[0][1] != "":
                url = list(latest_task)[0][1]
                break
            time.sleep(1)  # 等待1秒后再次检查

        # 下载文件
        response = requests.get(url)
        
        # 设置保存文件的路径结构
        base_dir = os.path.join(os.path.expanduser("~"), "Desktop", "语言翻译")
        lang_dir = os.path.join(base_dir, f"导出端-{accept_language}")
        os.makedirs(lang_dir, exist_ok=True)
        
        # 构建文件名并处理特殊字符
        file_name = os.path.join(lang_dir, rf"{url.split('/')[-1]}").replace(" ", "_").replace(":", "_").replace("C_", "C:")
        
        # 保存文件
        with open(file_name, "wb") as f:
            f.write(response.content)
        
        # 检查下载是否成功
        response.raise_for_status()
        
        print(f"文件已成功保存到: {file_name}")
        return file_name

    except requests.exceptions.RequestException as e:
        # 处理请求异常
        print(f"请求发生错误: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"错误响应状态码: {e.response.status_code}")
            print(f"错误响应头: {json.dumps(dict(e.response.headers), indent=2, ensure_ascii=False)}")
            print(f"错误详情: {e.response.text}")
        return None
    except IOError as e:
        # 处理文件操作异常
        print(f"文件操作错误: {str(e)}")
        return None

def get_task_list():
    """
    获取当前任务列表
    
    Returns:
        set: 包含任务ID和下载URL的元组集合
    """
    return_data = set()
    headers = {
        'Token':login(),
        'User-Agent': 'python-requests/2.31.0'
    }
    try:
        response = requests.get(f"{BASE_URL}/device-service/task/list", headers=headers)
        response.raise_for_status()
        result = response.json()
        if result.get('code') == 200:
            for item in result.get('data', []):
                task_id = item.get('id')
                download_url = item.get('downloadUrl', '')
                return_data.add((task_id, download_url))
                print(f"任务ID: {task_id}, 下载URL: {download_url}")  # 添加打印语句
    except Exception as e:
        print(f"获取任务列表失败: {str(e)}")
    return return_data

if __name__ == "__main__":
    print("开始测试API调用...")
    
    # 定义导出参数列表
    para_list = [
        # 导出类型0：
        {"targetEntId":"1881159263183699968","businessType":1,"exportType":2,"active":False,"baseParams":"0,1,2,3,4,5,6,7,8,9,10,12","stateParams":"0,3,4,7,5,6,1","subflag":False,"startTime":"2025-06-08 16:00:00","endTime":"2025-06-09 15:59:59","exportDataType":"0"},
        # 导出类型1：
        {"targetEntId":"1881159263183699968","businessType":1,"exportType":2,"active":False,"baseParams":"0,1,2,3,4,5,6,7,8,9,10,12","stateParams":"9,10,11,12,13,14,15,16,17,18,19","subflag":False,"startTime":"2025-06-08 16:00:00","endTime":"2025-06-09 15:59:59","exportDataType":"1"},
        # 导出类型2：
        {"targetEntId":"1881159263183699968","businessType":1,"exportType":2,"active":False,"baseParams":"0,1,2,3,4,5,6,7,8,9,10,12","stateParams":"0,1,2,3,4,5,6,7,8,9,10,11,12","subflag":False,"startTime":"2025-06-08 16:00:00","endTime":"2025-06-09 15:59:59","exportDataType":"2"},
    ]
    
    base_url = f"{BASE_URL}/device-service/task/save"

    # 遍历所有语言和导出类型进行测试
    for language in LANGUAGE_LIST:
        for request_data in para_list:
            result = download_report(language, base_url, request_data)
            if result:
                print("\n接口调用成功，文件保存在:")
                print(result)
            else:
                print("\n接口调用失败")