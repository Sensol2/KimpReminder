# import time
# from selenium import webdriver

# global driver
# #초기화
# def Initialize():
#     global driver

#     options = webdriver.ChromeOptions()

#     options.add_argument("headless")
#     # 필요없고 해결방법도 없는 에러로그들 제거 옵션 추가
#     options.add_experimental_option('excludeSwitches', ['enable-logging'])
#     options.add_experimental_option("detach", True)
#     driver = webdriver.Chrome('.\chromedriver\chromedriver.exe', options=options)

# #링크 받아오기
# def GetLink():
#     url = "http://121.161.125.62/coin/rate.php"
#     driver.get(url)

# #김프 지수 가져오기
# def GetKimchiRate():
#     rateList = []
#     bitbank_to_bithumb = (float)(driver.find_element_by_id('XRPbanktoth').text)
#     bitbank_to_coinone = (float)(driver.find_element_by_id('XRPbanktoone').text)
#     bitbank_to_upbit = (float)(driver.find_element_by_id('XRPbanktoup').text)

#     rateList.append(bitbank_to_bithumb)
#     rateList.append(bitbank_to_coinone)
#     rateList.append(bitbank_to_upbit)
#     # 0:비트뱅크->빗썸, 1:비트뱅크->코인원 2:비트뱅크->업비트

#     return rateList


