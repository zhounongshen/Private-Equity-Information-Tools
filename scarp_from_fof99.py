from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd 
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# 由于存在一定反爬取的设置，所以使用selenium模拟用户登录操作从而进入私募基金数据页面
def login_function():
    # 配置选项
    options = webdriver.ChromeOptions()
    # 忽略证书错误
    options.add_argument('--ignore-certificate-errors')
    # 忽略 Bluetooth: bluetooth_adapter_winrt.cc:1075 Getting Default Adapter failed. 错误
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 忽略 DevTools listening on ws://127.0.0.1... 提示
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(options=options)
    #未登录情况下进入基金搜索页面会自动跳转到登录页面
    login_url = 'https://mp.fof99.com/fund/all/?key=黑翼CTA-T1'
    driver.get(login_url)
    #寻找登录元素
    username_input = driver.find_element(By.ID,'username')
    password_input = driver.find_element(By.ID,'password')
    # 注册fof99的账户获得账户和密码
    username_input.send_keys('YOUR_USER_NAME')
    password_input.send_keys('YOU_PASSWORD')
    #寻找登录按钮登录
    login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
    login_button.click()
    #等待页面加载js 返回基金信息
    wait = WebDriverWait(driver, 10)
    time.sleep(5)
    return driver
    # html_content = driver.page_source
    # print(html_content)

# 获取所需数据
def get_product_name(driver,new_data):
    #html元素寻找还不是很熟悉，目前存在一定的冗余，待后续更改
    content = driver.find_element(By.CLASS_NAME,'layout-content')
    right_content = content.find_elements(By.XPATH,"./*")[1]  # 这里使用 XPath 查找所有子元素
    right_content_1 = right_content.find_elements(By.XPATH,"./*")[0]  # 这里使用 XPath 查找所有子元素
    data_3 = right_content_1.find_elements(By.XPATH,"./*")[2]
    data_3_2 = data_3.find_elements(By.XPATH,"./*")[1]

    # Tag Name: fund-table min-table-height
    data_3_2_1 = data_3_2.find_elements(By.XPATH,"./*")[0]
    data_3_2_2 = data_3_2_1.find_elements(By.XPATH,"./*")[0]
    data_3_2_3 = data_3_2_2.find_elements(By.XPATH,"./*")[0]
    data_3_2_4 = data_3_2_3.find_elements(By.XPATH,"./*")[0]
    data_3_2_5 = data_3_2_4.find_elements(By.XPATH,"./*")[0]
    # fixed left
    fixeed_left = data_3_2_5.find_elements(By.XPATH,"./*")[1]
    fixeed_left_1 = fixeed_left.find_elements(By.XPATH,"./*")[0]
    fixeed_left_2 = fixeed_left_1.find_elements(By.XPATH,"./*")[0]
    fixeed_left_3 = fixeed_left_2.find_elements(By.XPATH,"./*")[0]
    fixeed_left_4 = fixeed_left_3.find_elements(By.XPATH,"./*")[2]
    tr = fixeed_left_4.find_elements(By.XPATH,"./*")[0]

    product_name_td = tr.find_elements(By.XPATH,"./*")[2]
    product_name_span = product_name_td.find_elements(By.XPATH,"./*")[0]
    product_name_a = product_name_span.find_elements(By.XPATH,"./*")[0]

    product_name = product_name_a.text
    product_link = product_name_a.get_attribute('href')

    data = driver.find_elements(By.CLASS_NAME,'ant-table-row-cell-break-word')
    code = data[18].text
    date = data[20].text
    net = data[21].find_elements(By.XPATH,"./*")[0]
    net1 = net.find_elements(By.XPATH,"./*")[0].text
    week = data[22].text
    month = data[23].text
    month3 = data[24].text
    month6 = data[25].text
    year = data[26].text
    sharp_year = data[27].text
    karma_year = data[28].text
    new_row = {'name':product_name,'code':code,'date':date,'net':net1,'week':week,'month':month,'month3':month3,'month6':month6,'year':year,'sharp':sharp_year,'karma':karma_year}
    new_data = new_data.append(new_row,ignore_index=True)
    #获取产品名称，产品代码，创建日期，净值，周，月，三月，半年，年度收益率，年化夏普，年化卡玛
    print(product_name,code,date,net1,week,month,month3,month6,year,sharp_year,karma_year)

    # tr = fixeed_left_4.find_elements(By.XPATH,"./*")[0]
    # td = tr.find_elements(By.XPATH,"./*")
    # for child in data:
    #     print("Tag Name:",a, child.text)
    return new_data

# 搜索下一个基金
def next_product(driver,name):
    search_field = driver.find_element(By.CLASS_NAME,'ant-select-search__field')
    search_name = search_field.find_elements(By.XPATH,"./*")[0]
    search_name.send_keys(name)
    time.sleep(1)

    search_button = search_field.find_elements(By.XPATH,"./*")[1]
    search_button1 = search_button.find_elements(By.XPATH,"./*")[0]
    # svg
    search_button2 = search_button1.find_elements(By.XPATH,"./*")[0]

    ActionChains(driver).move_to_element(search_button2).click().perform()
    return 0

# 清除搜索框中上一个基金的名称
def clear(driver):
    search_field = driver.find_element(By.CLASS_NAME,'ant-select-search__field')
    search_name = search_field.find_elements(By.XPATH,"./*")[0]
    search_name.send_keys(Keys.CONTROL + "a")  # 选中全部文本
    search_name.send_keys(Keys.BACKSPACE)      # 使用BACKSPACE键清除选中的文本    
    time.sleep(1)
    return 0


if __name__ == '__main__':
    driver = login_function()
    # get_product_name(driver)
    # 中长CTA.xlsx中存放着一列想要查找的基金名称
    df = pd.read_excel('D:/causis/中长CTA.xlsx')
    column_list = df.values.tolist()

    new_columns = ['name','code','date','net','week','month','month3','month6','year','sharp','karma']
    new_data = pd.DataFrame(columns=new_columns)
    #循环查找产品信息
    for i in column_list:
        next_product(driver,i)
        wait = WebDriverWait(driver, 10)
        time.sleep(2)
        new_data = get_product_name(driver,new_data)
        time.sleep(2)
        clear(driver)
        time.sleep(2)
    #将获取信息存入csv文件中
    new_data.to_csv('data.csv', index=False)
