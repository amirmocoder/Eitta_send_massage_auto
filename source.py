import time
import re
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from chromedriver_py import binary_path

class Eitaa:
    def __init__(self, support_chat_id, labeling, profile_path):
        # Initialize the WebDriver
        self.driver_path = binary_path
        self.options = Options()
        self.options.add_argument(profile_path)
        self.options.add_argument("--start-minimized")
        self.svc = webdriver.ChromeService(executable_path=self.driver_path)
        self.driver = webdriver.Chrome(service=self.svc, options=self.options)
        self.contact_prefix = labeling
        self.inti_chat_id = support_chat_id
        self.output_csv = []
        
    def get_url(self, url):
        self.driver.get(url)
        time.sleep(1)
        self.driver.refresh()
        time.sleep(1)

    def read_csv(self, file_path):
        with open(file_path, mode='r', newline='', encoding='utf-8-sig') as f:
            self.csv_file = list(csv.reader(f))

    def get_item(self, item_index):
        self.item = [item_index]
        self.item.extend(self.csv_file[item_index])
        self.item.append(0)
    
    def get_contact(self):

        clickable = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/div/div/div[2]/div[3]/div[1]")
        ActionChains(self.driver)\
            .click(clickable)\
            .perform()
        time.sleep(0.2)
        
        clickable = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/div/div/div[2]/div[3]/div[3]/div[3]")
        ActionChains(self.driver)\
            .click(clickable)\
            .perform()
        time.sleep(0.2)
        
        clickable = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/div/div[2]/div[2]/button/div")
        ActionChains(self.driver)\
            .click(clickable)\
            .perform()
        time.sleep(0.2)

        self.driver.execute_script(f"arguments[0].textContent = 'کد {self.item[0]}';", self.driver.find_element(By.XPATH,"/html/body/div[5]/div/div[2]/div[1]/div[1]"))
        self.driver.execute_script(f"arguments[0].textContent = '{self.contact_prefix}';", self.driver.find_element(By.XPATH,"/html/body/div[5]/div/div[2]/div[2]/div[1]"))
        clickable = self.driver.find_element(By.XPATH,"/html/body/div[5]/div/div[3]/div[1]")
        clickable.click()
        time.sleep(0.2)

        for digit in self.item[3]:
            clickable.send_keys(digit)
            time.sleep(0.05)

        clickable = self.driver.find_element(By.XPATH, "/html/body/div[5]/div/div[1]/button/div")
        ActionChains(self.driver)\
            .click(clickable)\
            .perform()
        time.sleep(0.2)

        self.driver.refresh()
        time.sleep(1)

    def execute(self, message):
        index= 0
        while True:
            try:
                self.get_item(item_index=index)
                self.get_contact()
                index += 1
            except IndexError:
                break

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    application = Eitaa(support_chat_id="333000", labeling= "اطلاع رسانی بیمه", profile_path= "user-data-dir=C:\\Users\\amira\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1")

    application.read_csv('data_csv.csv')
    application.get_url(f"https://web.eitaa.com/#{application.inti_chat_id}")

    application.execute(message= "")

    input("Press Enter to close...")
    # application.close()