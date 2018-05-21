from bs4 import BeautifulSoup
from selenium import webdriver
import time

# 使用selenium
# 使用 Selenium 的 webdriver 实例化一个浏览器对象,在这里使用 Phantomjs:
driver = webdriver.PhantomJS(executable_path="D:\\phantomjs.exe")
# 设置 Phantomjs 窗口最大化
driver.mainmize_window()

# 登录QQ空间
def get_shuoshuo(qq):
    # 使用get()方法打开待抓取的URL
    driver.get('http://user.qzone.qq.com/{}/311').format(qq)
    # 等待 5 秒后,判断页面是否需要登录,通过查找页面是否有相应的 DIV 的 id 来判断
    time.sleep(5)
    try:
        driver.find_element_by_id('login_div')
        a = True
    except:
        a = False

    # 如果页面存在登录的 DIV,则模拟登录:
    if a == True:
        driver.switch_to.frame('login_frame')   # 切换到登录ifram
        driver.find_element_by_id('switcher_plogin').click()
        driver.find_element_by_id('u').clear()  # 选择用户名框
        driver.find_element_by_id('u').send_keys('QQ号')
        driver.find_element_by_id('p').clear()
        driver.find_element_by_id('p').send_keys('QQ密码')
        driver.find_element_by_id('login_button').click()
    driver.implicity_wait(3)

    # 接着,判断好友空间是否设置了权限,通过判断是否存在元素 ID
    try:
        driver.find_element_by_id('QM_OwnerInfo_Icon')
        b = True
    except:
        b = False

    # 如果有权限能够访问到说说页面,那么定位元素和数据,并解析:
    if b == True:
        driver.switch_to.frame('app_canvas_frame')
        content = driver.find_element_by_css_selector('content')
        stime = driver.find_element_by_css_selector('.c_tx.c_tx3.goDetail')
        for con, sti in zip(content, stime):
            data = {
                'time': sti.text,
                'shuos': con.text,
            }
            print(data)

        # 除了在 Selenium 中解析数据,我们还可以将当前页面保存为源码,再使用 BeautifulSoup
        # 来解析:
        pages = driver.page_source
        soup = BeautifulSoup(pages, 'lxml')

    # 最后,我们尝试一下获取 Cookie,使用 get_cookies():
    cookie = driver.get_cookies()
    cookie_dict = []
    for c in cookie:
        ck = "{0} = {1};".format(c['name'], c['value'])
        cookie_dict.append(ck)
    i = ''
    for c in cookie_dict:
        i += c
    print('Cookies:', i)
    print("==========完成==============")

    # 另外,再介绍两个 Selenium 的常用方法:
    # driver.save_screenshot('保存的文件路径及文件名') 保存屏幕截图:
    # driver.execute_script("JS 代码")   执行 JS 脚本:
    driver.close()
    driver.quit()

if __name__ == "__main__":
    get_shuoshuo('好友QQ号')
