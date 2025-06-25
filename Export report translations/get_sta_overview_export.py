import requests
import json
import os
from login import login
from config import BASE_URL, LANGUAGE_LIST, TRANSLATION_DIR, DEFAULT_HEADERS, LOGIN_CONFIG

def get_sta_overview_export(accept_language='',url='', params=None, method="post"):
    """
    调用获取统计概览导出接口，支持多语言导出Excel文件
    
    Args:
        accept_language (str): 接受的语言代码，如'en'、'zh-CN'等
        url (str): API的完整URL地址
        params (dict): 请求参数字典
        method (str): 请求方法，默认为"post"，支持"get"和"post"
    
    Returns:
        str: 保存的文件路径，如果发生错误则返回None
    """
    # 设置请求头信息
    headers = {
        'Token': login(accept_language=accept_language),  # 认证Token
        'Accept-Language': accept_language,  # 设置接受的语言
        'User-Agent': DEFAULT_HEADERS['User-Agent']  # 设置User-Agent
    }

    try:
        # 根据指定的方法发送请求
        if "post" == method.lower():
            # 尝试使用JSON格式发送POST请求
            response = requests.post(url, headers=headers, json=params)
            try:
                # 如果JSON请求成功且返回JSON响应，则尝试使用form-data格式重新发送
                if response.ok and response.json():
                    response = requests.post(url, headers=headers, data=params)
            except Exception as e:
                pass
        elif "get" == method.lower():
            # 发送GET请求
            response = requests.get(url, headers=headers, params=params)

        # 如果请求不成功，打印详细的请求信息用于调试
        if not response.ok:
            print(f"完整URL: {response.url}")
            print(f"请求方法: POST")
            print(f"请求头: {json.dumps(headers, indent=2, ensure_ascii=False)}")
            print(f"请求参数: {json.dumps(params, indent=2, ensure_ascii=False)}")
            print(f"状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
        
        # 按语言创建子目录
        lang_dir = os.path.join(TRANSLATION_DIR, f"导出端-{accept_language}")
        
        # 创建保存文件的目录（如果不存在）
        os.makedirs(lang_dir, exist_ok=True)
        
        # 从URL中提取文件名并构建完整的文件路径
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
    # 开始测试API调用
    print("开始测试API调用...")
    
    # 定义API端点和参数列表
    url_list = [
        # 统计报表-运行统计
        # 运行总览
        (f"{BASE_URL}/location-service/position/getStaOverviewExport", 
         {"endTime": "2025-06-07 16:00:00", "entId": "1925747610618953728", "startTime": "2025-06-06 16:00:00"}),
         #里程统计1
         (f"{BASE_URL}/location-service/position/mileageStaByDayExport", 
         {"carId":"1881317797200396288", "endTime": "2025-06-07 16:00:00", "entId": "1925747610618953728", "startTime": "2025-06-06 16:00:00"}),
         #超速详单2
         (f"{BASE_URL}/location-service/position/getOverSpeedDetailExport", 
         {"carId":"1881317797200396288", "endTime": "2025-06-07 16:00:00", "entId": "1925747610618953728", "startTime": "2025-06-06 16:00:00"}),
         #停留详单3
         (f"{BASE_URL}/location-service/position/getStopDetailExport",
         {"carId":"1881317797200396288", "mapType":"1", "endTime": "2025-06-07 16:00:00", "entId": "1925747610618953728", "startTime": "2025-06-06 16:00:00"},
          "GET"),
         #ACC统计4
         (f"{BASE_URL}/device-service/accSta/queryDetailWithUserOrCarIdExport", 
         {"carId":"1881317797200396288", "mapType":"1", "endTime": "2025-06-07 16:00:00", "entId": "1925747610618953728", "startTime": "2025-06-06 16:00:00"},
          "GET"),
         #行程统计5
         (f"{BASE_URL}/location-service/position/distanceStaExport", 
         {"carId":"1881317797200396288", "intervalTime":"180", "selectKey":"mileage", "mapType":"1", "endTime": "2025-06-07 16:00:00", "entId": "1925747610618953728", "startTime": "2025-06-06 16:00:00"}),
         #离线统计6
         (f"{BASE_URL}/device-service/car/queryOffineCarExport", 
         {"entId": "1881159263183699968","duration":"7","prependFilterType":"2","apppendFilterType":"2","recursion":"false","mapType":"1","minInterval":"600","maxInterval":"604800","endTime": "2025-06-07 16:00:00",  "startTime": "2025-06-06 16:00:00"}),
         #怠速统计7
        (f"{BASE_URL}/location-service/position/getIdlingDetailExport", 
         {"carId":"1881317797200396288", "mapType":"1", "endTime": "2025-06-10 15:59:59", "entId": "1881159263183699968", "startTime": "2025-06-05 16:00:00"}),
         #静止统计8
        (f"{BASE_URL}/device-service/structure/getStaticStatisticsExport", 
         {"entId":"1881159263183699968","subFlag":False,"flag":5,"timeInterval":-1,"mapType":1,"startTime":"2025-06-08 16:00:00","endTime":"2025-06-09 15:59:59"}),
         #统计报表-报警统计
         #报警总览9
        (f"{BASE_URL}/alarm-service/alarmSta/queryGroupByCarExport", 
         {"entId":"1881159263183699968","groupId":0,"alarmTypes":"1,2,3,4,5,6,7,10,21,25","startTime":"2025-06-08 16:00:00","endTime":"2025-06-09 15:59:59"},
         "GET"),
        #报警统计10
        (f"{BASE_URL}/alarm-service/alarmSta/queryGroupByDayExport", 
         {"carId":"1881317797200396288","entId":"1881159263183699968","mapType":1,"alarmTypes":"1,2,3,4,5,6,7,10,21,25","startTime":"2025-06-08 16:00:00","endTime":"2025-06-09 15:59:59"},
         "GET"),
        #报警详单11
         (f"{BASE_URL}/alarm-service/alarmSta/queryDetailExport", 
         {"carId":"1881317797200396288","alarmTypes":"1,2,3,4,5,7,8,10,11,13,21,25,26,27,30,31,32,33,34,35,40,45,50,55,60,70,71,72,73,74,75,76,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,107,108,109,101,111,122,123,124,127,128","mapType":1,"entId":"1881159263183699968","startTime":"2025-06-08 16:00:00","endTime":"2025-06-09 15:59:59"}),
        #温湿度报警汇总12
        (f"{BASE_URL}/alarm-service/alarmLabel/queryTempAndHumidAlarmExport", 
        {"entId":"1881159263183699968","groupId":"0","startTime":"2024-07-31 16:00:00","endTime":"2024-08-31 15:59:59"}),
        #温湿度报警详单13
        (f"{BASE_URL}/alarm-service/alarmLabel/queryAlarmDetailExport", 
        {"entId":"1881159263183699968","deviceId":"10338","deviceType":0,"mapType":1,"startTime":"2024-08-31 16:00:00","endTime":"2024-09-30 15:59:59"}),
        #统计报表-行业统计
        #油量总览14
        (f"{BASE_URL}/location-service/position/getOilOverViewExport", 
         {"entId":"1881159263183699968","groupId":"0","filter":"true","mapType":"1","startTime":"2025-06-08 16:00:00","endTime":"2025-06-09 15:59:59"},
         "GET"),
        #油量统计15
        (f"{BASE_URL}/location-service/position/getStaOilExport", 
         {"mapType":"1","minRate":"0.25","maxRate":"5.00","startTime":"2025-04-30 16:00:00","endTime":"2025-05-31 15:59:59","carId":"1881317797200396288"},
         "GET"),
        #条码统计16
        (f"{BASE_URL}/user-service/barCode/queryBarCodeExport", 
        {"carId":"1384502","mapType":"1","entId":"1405","startTime":"2025-05-31 16:00:00","endTime":"2025-06-09 15:59:59"}),
        #驾驶行为17
        (f"{BASE_URL}/alarm-service/alarmSta/getDriveStaExport", 
        {"carId":"1881515872997081088","endTime":"2025-01-31 15:59:59","entId":"1881159263183699968","groupId":"0","mapType":1,"startTime":"2024-12-31 16:00:00"}),
        #驾驶分析18
        (f"{BASE_URL}/location-service/position/drivingAnalysisExport", 
        {"carId":"1881317797200396288","entId":"1881159263183699968","groupId":"0","mapType":1,"startTime":"2025-05-31 16:00:00","endTime":"2025-06-09 15:59:59"}),
        #充电统计19
        (f"{BASE_URL}/alarm-service/position/getChargingStaExport", 
        {"carId":"1881332707842064384","entId":"1881159263183699968","subFlag":1,"mapType":1,"startTime":"2024-11-30 16:00:00","endTime":"2024-12-31 15:59:59"},
        "GET"),
        #统计报表-区域统计
        #出入围栏统计20
        (f"{BASE_URL}/alarm-service/carFenceAlarm/statisticExport", 
        {"offset":0,"mapType":1,"startTime":"2025-06-08 16:00:00","endTime":"2025-06-09 15:59:59"}),
        #出入围栏详单21
        (f"{BASE_URL}/alarm-service/carFenceAlarm/inOutFenceDetailExport", 
        {"offset":0,"mapType":1,"startTime":"2025-06-08 16:00:00","endTime":"2025-06-09 15:59:59"}),
        #围栏报警详单22
        (f"{BASE_URL}/alarm-service/carFenceAlarm/fenceAlarmDetailExport", 
        {"offset":0,"mapType":1,"startTime":"2025-06-08 16:00:00","endTime":"2025-06-09 15:59:59"}),
        #线路报警详单23

        #统计报表-打卡统计
        #人员打卡23
        (f"{BASE_URL}/user-service/punchrecord/listExport", 
        {"entId":"17099","type":"1","subFlag":True,"addressFlag":True,"mapType":1,"startTime":"2024-11-30 16:00:00","endTime":"2024-12-31 15:59:59"}),
        #司机打卡明细24
        (f"{BASE_URL}/user-service/driverPunch/punchDetailExport", 
        {"isChild":1,"mapType":1,"startTime":"2025-06-08 16:00:00","endTime":"2025-06-09 15:59:59"},
        "GET"),
        #司机打卡汇总25
        (f"{BASE_URL}/user-service/driverPunch/punchStaExport", 
        {"isChild":1,"mapType":1,"startTime":"2025-06-08 16:00:00","endTime":"2025-06-09 15:59:59"},
        "GET"),
        #司机管理26
        (f"{BASE_URL}/user-service/driver/getListExport", 
        {"isChild":1,"mapType":1},
        "GET"),
        #财务中心-资产管理
        #点卡管理27
        (f"{BASE_URL}/user-service/pointCard/exportLog", 
        {"belongEntId":"1","targetEntId":None,"pointCardType":None,"operaType":None,"type":None,"pageIndex":1,"pageSize":15,"startTime":"2025-05-09 16:00:00","endTime":"2025-06-09 15:59:59"}),
        #订单管理28
        (f"{BASE_URL}/function-package-service/saas/order/exportList", 
        {"entId":"1","tradeNo":""})
    ] 

    # 遍历每种语言和每个API端点进行导出
    # for language in LANGUAGE_LIST:
    #     for request_data in url_list:
    #         result = get_sta_overview_export(language, *request_data)
    
    result = get_sta_overview_export(LANGUAGE_LIST[0], *url_list[23])
    
    # 检查最终结果
    if result:
        print("\n接口调用成功，文件保存在:")
        print(result)
    else:
        print("\n接口调用失败")
