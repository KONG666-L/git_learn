import requests
import json
import os
from login import login
from config import BASE_URL, LANGUAGE_LIST, TRANSLATION_DIR, DEFAULT_HEADERS

def get_sta_overview_export(accept_language='', url='', params=None, method="post"):
    """
    调用获取统计概览导出接口，将数据导出为Excel文件
    
    Args:
        accept_language (str): 接受的语言，用于设置导出文件的语言版本
        url (str): API的完整URL地址
        params (dict): 请求参数，包含查询条件
        method (str): 请求方法，默认为"post"，支持"get"和"post"
    
    Returns:
        str: 保存的文件路径，如果导出失败则返回None
    """

    # 设置请求头信息
    headers = {
        'Token': login("ping-jxs","a12345678.",accept_language=accept_language),  # 调用登录接口获取token
        'Accept-Language': accept_language,  # 设置接受的语言
        'User-Agent': DEFAULT_HEADERS['User-Agent']  # 设置User-Agent
    }

    try:
        # 根据指定的方法发送请求
        if "post" == method.lower():
            # 首先尝试使用json格式发送请求
            response = requests.post(url, headers=headers, json=params)
            try:
                # 如果json格式请求成功，则尝试使用form-data格式重新发送
                if response.ok and response.json():
                    response = requests.post(url, headers=headers, data=params)
            except Exception as e:
                pass
        elif "get" == method.lower():
            # 发送GET请求
            response = requests.get(url, headers=headers, params=params)

        # 如果请求失败，打印详细的请求信息用于调试
        if not response.ok:
            print(f"完整URL: {response.url}")
            print(f"请求方法: POST")
            print(f"请求头: {json.dumps(headers, indent=2, ensure_ascii=False)}")
            print(f"请求参数: {json.dumps(params, indent=2, ensure_ascii=False)}")
            print(f"状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
        
        # 在桌面创建"语言翻译"文件夹，并根据语言创建子文件夹
        lang_dir = os.path.join(TRANSLATION_DIR, f"导出端-{accept_language}")
        
        # 创建保存目录（如果不存在）
        os.makedirs(lang_dir, exist_ok=True)
        
        # 根据URL构建文件名
        file_name = os.path.join(lang_dir, f"{url.split('/')[-1]}_download.xlsx")
        
        # 将响应内容保存为Excel文件
        with open(file_name, "wb") as f:
            f.write(response.content)
        
        # 检查响应状态码，如果不是2xx则抛出异常
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
    
if __name__ == "__main__":
    print("开始测试API调用...")
    
    # 定义需要导出的报表URL和参数列表
    url_list = [
        # 统计报表-区域统计
        # 1. 出入围栏统计
        (f"{BASE_URL}/alarm-service/carFenceAlarm/statisticExport", 
        {"offset":0,"mapType":1,"startTime":"2025-06-08 16:00:00","endTime":"2025-06-09 15:59:59"}),
        
        # 2. 出入围栏详单
        (f"{BASE_URL}/alarm-service/carFenceAlarm/inOutFenceDetailExport", 
        {"offset":0,"mapType":1,"startTime":"2025-06-08 16:00:00","endTime":"2025-06-09 15:59:59"}),
        
        # 3. 围栏报警详单
        (f"{BASE_URL}/alarm-service/carFenceAlarm/fenceAlarmDetailExport", 
        {"offset":0,"mapType":1,"startTime":"2025-06-08 16:00:00","endTime":"2025-06-09 15:59:59"}),
    ] 
    
    # 遍历语言列表和URL列表，导出所有报表
    for language in LANGUAGE_LIST:
        for request_data in url_list:
            result = get_sta_overview_export(language, *request_data)
    
    # 输出最终执行结果
    if result:
        print("\n接口调用成功，文件保存在:")
        print(result)
    else:
        print("\n接口调用失败")
 