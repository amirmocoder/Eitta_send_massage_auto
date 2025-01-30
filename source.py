import time
import re
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from chromedriver_py import binary_path

class Eitta:
    def __init__(self):
        # Initialize the WebDriver
        self.driver_path = binary_path
        self.options = Options()
        self.options.add_argument("user-data-dir=C:\\Users\\amira\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
        self.options.add_argument("--start-minimized")
        self.svc = webdriver.ChromeService(executable_path=self.driver_path)
        self.driver = webdriver.Chrome(service=self.svc, options=self.options)
        self.contact_prefix = "بیمه گزار علوم پزشکی تبریز"
        self.output_csv = []
        
    def get_url(self, url):
        self.driver.get(url)
        time.sleep(5)

    def read_csv(self, file_path):
        with open(file_path, mode='r', newline='', encoding='utf-8-sig') as f:
            self.csv_file = list(csv.reader(f))

    def get_item(self, item_index):
        self.item = [item_index]
        self.item.extend(self.csv_file[item_index])
        self.item.append(0)
    
    def create_contact(self):

        clickable = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/div/div/div[2]/div[3]")
        ActionChains(self.driver)\
            .click(clickable)\
            .perform()
        time.sleep(1)
        
        clickable = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/div/div/div[2]/div[3]/div[3]/div[3]/div")
        ActionChains(self.driver)\
            .click(clickable)\
            .perform()
        time.sleep(1)
        
        clickable = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/div/div[2]/div[2]/button/div")
        ActionChains(self.driver)\
            .click(clickable)\
            .perform()
        time.sleep(1)

        self.driver.execute_script(f"arguments[0].textContent = '{self.item[2]}';", self.driver.find_element(By.XPATH,"/html/body/div[5]/div/div[2]/div[1]/div[1]"))
        self.driver.execute_script(f"arguments[0].textContent = '{self.contact_prefix}';", self.driver.find_element(By.XPATH,"/html/body/div[5]/div/div[2]/div[2]/div[1]"))
        clickable = self.driver.find_element(By.XPATH,"/html/body/div[5]/div/div[3]/div[1]")
        clickable.click()

        for digit in self.item[3]:
            clickable.send_keys(digit)
            time.sleep(0.1)

        time.sleep(5)

        clickable = self.driver.find_element(By.XPATH, "/html/body/div[5]/div/div[1]/button/div")
        ActionChains(self.driver)\
            .click(clickable)\
            .perform()
        time.sleep(1)

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    application = Eitta()

    application.read_csv('data_csv.csv')
    application.get_item(item_index=2)
    
    application.get_url("https://web.eitaa.com/")

    application.create_contact()

    input("Press Enter to close...")

    # application.close()