from selenium import webdriver
import time

class driverCall():
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--incognito")
        options.add_argument("window-size=500,500")
        driver = webdriver.Chrome(chrome_options=options)
        driver.get('https://youtu.be/8rqgGZrsB7g')
        driver.find_element_by_xpath("//button[@class='ytp-play-button ytp-button']").click()
        driver.find_element_by_xpath("//button[@class='ytp-mute-button ytp-button']").click()
        driver.find_element_by_xpath("//button[@class='ytp-button ytp-settings-button']").click()
        driver.find_element_by_xpath("//div[@class='ytp-menuitem-label']").click()
        element = driver.find_element_by_xpath("//div[@class='ytp-menuitem-content']")
        driver.minimize_window()
        time.sleep(601)
        driver.quit()
while(True):
    objs = {}
    for x in range(10) :
        objs[x]= driverCall()

