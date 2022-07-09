import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException


options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument('--headless')
options.headless = True
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)


def isFoundLink(term):
    urls = getUrls()

    print(urls)
    print(term)
    print('==============')

    for url in urls:
        if (re.search(term, url) != None):
            return True

    return False


def getUrls():
    urls = driver.find_elements(By.XPATH, "//div//cite[@role='text']")

    return list(filter(bool, map(lambda x: x.text, urls)))


def searchInBrowser(term):
    search_query = "https://www.google.com/search?q={q}".format(q=term)
    driver.get(search_query)


def nextPage():
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'Next')))

        driver.find_element(By.LINK_TEXT, 'Next').click()
        print("next page")
        return True
    except (TimeoutException, WebDriverException) as e:
        print(e)
        print("Last page reached")
        return False


def bootstrap(site, term):
    searchInBrowser(term)

    PAGE_LIMIT = 10
    for i in range(PAGE_LIMIT):
        if (isFoundLink(site)):
            print("Found it")
            return True

        if (not nextPage()):
            break

    print("Not found")


bootstrap('cromg.org', 'jeash')
