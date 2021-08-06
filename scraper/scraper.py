from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

url = 'https://bitinfocharts.com/dogecoin/'
browser = webdriver.Chrome()
browser.get(url)

element = browser.find_element_by_xpath('//tr[td[a[contains(text(), "Tweets per day")]]]/td[2]/a')

print(element.text)

browser.close()