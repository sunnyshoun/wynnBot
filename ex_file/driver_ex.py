# from threading import Thread
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
#import bs4

# def open_chrome():
#     chrome_options = Options()
#     chrome_options.add_argument('--headless')
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-dev-shm-usage')
#     user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/91.0.4472.124 Safari/537.36"
#     chrome_options.add_argument('--user-agent=%s' % user_agent)
#     global chrome
#     chrome = webdriver.Chrome(chrome_options=chrome_options,port=8080)
#     chrome.get("https://safeweb.norton.com/")

# def check_url_theard(result_list,url):
#     chrome.find_element_by_id("appendedInputButton").send_keys(url)
#     chrome.find_element_by_id("homeSearchImg").click()
#     source = chrome.page_source
#     root = bs4.BeautifulSoup(source, 'html.parser')
#     result=root.find('div',class_='paddingTop30 tAlignCr').select("b")
#     chrome.get("https://safeweb.norton.com/")
#     result_list.append(result)

# def check_url(url):
    # result_list=[]
    # t = Thread(target=check_url_theard, args=(result_list, url))
    # t.start()
    # t.join()
    # result = result_list[0]
    # return result[0].getText().lower()

# open_webdriver = Thread(target=open_chrome)
# open_webdriver.start()