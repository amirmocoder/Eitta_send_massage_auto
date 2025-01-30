# import selenium, regex
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException, WebDriverException
# call installed chromedriver drive from from the lib
from chromedriver_py import binary_path

svc = webdriver.ChromeService(executable_path=binary_path)
driver = webdriver.Chrome(service=svc)

def sleep(t):
    global wait

    wait = WebDriverWait(driver, t)
    wait.until(EC.visibility_of_element_located((By.TAG_NAME, "html")))
