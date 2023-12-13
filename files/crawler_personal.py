# -*- coding:utf-8 -*-

import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re
'''
opt = Options()
opt.add_experimental_option('detach', True)
# 通过option参数，设置浏览器不关闭
driver = webdriver.Firefox()
driver.get("https://xxcapp.xidian.edu.cn/site/xidianPage/newsPage")



my_username = ''
my_password = ''
input_username = driver.find_element(By.ID, 'username')
input_username.send_keys(my_username)

input_password = driver.find_element(By.ID, 'password')
input_password.send_keys(my_password)

submit_btn = driver.find_element(By.ID, 'login_submit')
submit_btn.click()

try:
    # 查找username和password元素
    username_element = driver.find_element(By.ID,'username')
    password_element = driver.find_element(By.ID,'password')

    # 如果找到了元素，等待用户输入
    username = input('请输入用户名：')
    password = input('请输入密码：')

    # 输入用户名和密码
    username_element.send_keys(username)
    password_element.send_keys(password)
    submit_btn = driver.find_element(By.ID, 'login_submit')
    submit_btn.click()

except NoSuchElementException:
    # 如果找不到元素，进行自定义操作
    print("未找到用户名和密码元素，进行自定义操作")
'''
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

'''
opt = Options()
opt.add_experimental_option('detach', True)
# 通过option参数，设置浏览器不关闭
'''
driver = webdriver.Firefox()
driver.get("https://xxcapp.xidian.edu.cn/site/xidianPage/newsPage")
time.sleep(3)
my_username = ''
my_password = ''

input_username = driver.find_element(By.ID, 'username')
input_username.send_keys(my_username)

input_password = driver.find_element(By.ID, 'password')
input_password.send_keys(my_password)

submit_btn = driver.find_element(By.ID, 'login_submit')
submit_btn.click()