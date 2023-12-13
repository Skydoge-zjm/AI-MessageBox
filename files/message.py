"""
time.sleep()中的时间可以根据网速、电脑性能等因素调整
原程序中的停顿时间较长，是因为作者的电脑比较fw

程序需要安装selenium库，以及浏览器对应驱动

输入账号密码阶段就交给前端和整合了:)
只要替换掉input区域的相关代码
"""

import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
flag = 1
date = ''
title = ''
content = ''


def get_message():
    driver = webdriver.Firefox()
    driver.get("https://xxcapp.xidian.edu.cn/site/xidianPage/newsPage")
    time.sleep(2)
    page_url = driver.current_url
    print(page_url[:42])
    while page_url[:42] == 'https://ids.xidian.edu.cn/authserver/login':
        time.sleep(2)
        page_url = driver.current_url
    cnt = 0
    personal_json = []
    for i in range(1, 6):  # 表示最近x条消息

        special_value = '/html/body/div[1]/div[1]/section/div[2]/div/div[' + str(i) + ']/div[2]'
        special = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, special_value))).text
        if '流程' in special:
            continue
        if '提醒' in special:
            continue

        title_value = '/ html/body/div[1]/div[1]/section/div[2]/div/div[' + str(i) + ']/div[1]'
        item_value = '/html/body/div[1]/div[1]/section/div[2]/div/div[' + str(i) + ']'
        date_value = '/html/body/div[1]/div[1]/section/div[2]/div/div[' + str(i) + ']/div[2]'
        need_back = 1
        try:
            title = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, title_value)))
            title = driver.find_element(By.XPATH, value=title_value).text
            date = driver.find_element(By.XPATH, value=date_value).text
            item = driver.find_element(By.XPATH, value=item_value)
            item.click()
            time.sleep(0.5)
            try:
                error_page_value = '/html/body/div[6]/p'
                error_page = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, error_page_value))).text
                if '内容不存在或已删除' in error_page:
                    driver.back()
                    continue
            except:
                pass

            time.sleep(0.5)
            try:
                content = driver.find_element(By.XPATH, value='/html/body/div[1]/div[2]').text
                if content == '加载中':
                    continue
                elif content == '' and len(title) > 30:
                    need_back = 0

                if need_back == 1:
                    driver.back()
                    time.sleep(0.1)
            except:
                pass
        except:
            cnt += 1
            content = driver.find_element(By.XPATH, value=title_value).text
            title = "none"
        if content == '' and title != '':
            content = title
            title = "none"
        try:
            data_json = {
                "title": title,
                "time": date,
                "content": content
            }
            personal_json.append(data_json)
        except:
            flag = -2
    return personal_json
