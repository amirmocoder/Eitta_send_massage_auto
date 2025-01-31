import time
import re
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from chromedriver_py import binary_path

class Eitaa:
    def __init__(self, csv_path, init_chat_id, prefix, chrome_profile_path, dev_chat_id, dev_name, message):
        # Initialize the WebDriver
        self.driver_path = binary_path
        self.options = Options()
        self.options.add_argument(chrome_profile_path)
        self.options.add_argument("--start-minimized")
        self.svc = webdriver.ChromeService(executable_path=self.driver_path)
        self.driver = webdriver.Chrome(service=self.svc, options=self.options)
        self.contact_prefix = prefix
        self.inti_chat_id = init_chat_id
        self.support_chat_id = dev_chat_id
        self.support_contact_name= dev_name
        self.message_pattern = message
        self.file_dir = csv_path

    def get_url(self, url):
        self.driver.get(url)
        time.sleep(0.5)
        self.driver.refresh()
        time.sleep(0.5)

    def read_csv(self):
        with open(self.file_dir, mode='r', newline='', encoding='utf-8-sig') as f:
            self.csv_data = list(csv.reader(f))

    def get_item(self, item_index):
        self.item = [item_index]
        self.item.extend(self.csv_data[item_index])
    
    def save_contact(self):

        clickable = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/div/div/div[2]/div[3]/div[1]")
        ActionChains(self.driver)\
            .click(clickable)\
            .perform()
        time.sleep(0.25)
        
        clickable = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/div/div/div[2]/div[3]/div[3]/div[3]")
        ActionChains(self.driver)\
            .click(clickable)\
            .perform()
        time.sleep(0.25)
        
        clickable = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/div/div[2]/div[2]/button/div")
        ActionChains(self.driver)\
            .click(clickable)\
            .perform()
        time.sleep(0.25)

        self.driver.execute_script(f"arguments[0].textContent = 'کد {self.item[0]}';", self.driver.find_element(By.XPATH,"/html/body/div[5]/div/div[2]/div[1]/div[1]"))
        self.driver.execute_script(f"arguments[0].textContent = '{self.contact_prefix}';", self.driver.find_element(By.XPATH,"/html/body/div[5]/div/div[2]/div[2]/div[1]"))
        clickable = self.driver.find_element(By.XPATH,"/html/body/div[5]/div/div[3]/div[1]")
        clickable.click()
        time.sleep(0.25)

        for digit in self.item[3]:
            clickable.send_keys(digit)
            time.sleep(0.0625)

        clickable = self.driver.find_element(By.XPATH, "/html/body/div[5]/div/div[1]/button/div")
        ActionChains(self.driver)\
            .click(clickable)\
            .perform()
        time.sleep(0.25)

        self.driver.refresh()
        time.sleep(0.25)
        self.driver.refresh()
        time.sleep(0.5)

    def get_contact(self, content):
        clickable = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/div/div/div[1]/div[2]")
        ActionChains(self.driver)\
            .click(clickable)\
            .perform()
        time.sleep(0.25)

        clickable = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/div/div/div[1]/div[2]/input")
        ActionChains(self.driver)\
            .click(clickable)\
            .perform()
        clickable.send_keys(content)
        time.sleep(0.25)
        try:
            clickable = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/div/div/div[2]/div[2]/div[3]/div/div/div[1]/div/div/ul/li[1]")
            ActionChains(self.driver)\
                .click(clickable)\
                .perform()
            time.sleep(0.25)

            if self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div/span").text == f"کد {self.item[0]} {self.contact_prefix}":
                self.item[6]= 1
                return 1
            else:
                self.item[6]= 0
                return 0
        except NoSuchElementException:
            self.item[6]= 0
            return 0
        
    def get_chat_id(self):
        self.item.append(re.search(r"#\d+",self.driver.current_url).group())

    def send_message(self, message):
        try:
            clickable = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/div/div/div[4]/div/div[1]/div[7]/div[1]")
            ActionChains(self.driver)\
                .click(clickable)\
                .perform()
            time.sleep(0.25)

            self.driver.execute_script(f"arguments[0].innerText = arguments[1];", self.driver.find_element(By.XPATH,"/html/body/div[2]/div[1]/div[2]/div/div/div[4]/div/div[1]/div[7]/div[1]/div[1]"), message % (self.item[1], self.item[2]))
            time.sleep(0.0625)

            clickable = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/div/div/div[4]/div/div[4]/button/div")
            ActionChains(self.driver)\
                .click(clickable)\
                .perform()
            
            time.sleep(0.25)
            if self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/div/div/div[4]/div/div[1]/div[7]/div[1]/div[1]").text == "":
                self.item[7]= 1
                return 1
            else:
                self.item[7]= 0
                return 0
        except NoSuchElementException:
            self.item[7]= 0
            return 0

    def update_csv(self, row):
        self.csv_data[row] = self.item
        with open(self.file_dir, mode='w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerows(self.csv_data)

    def remove_contact(self):
        clickable = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/div/div/div[2]/div[1]/div")
        ActionChains(self.driver)\
            .click(clickable)\
            .perform()
        time.sleep(0.25)
        
        clickable = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[3]/div/div/div[1]/div/div[1]/button")
        ActionChains(self.driver)\
            .click(clickable)\
            .perform()
        time.sleep(0.25)

        clickable = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[3]/div/div[2]/div[2]/div/div[2]/div/div")
        ActionChains(self.driver)\
            .click(clickable)\
            .perform()
        time.sleep(0.25)
        
        clickable = self.driver.find_element(By.XPATH, "/html/body/div[5]/div/div[2]/button[1]")
        ActionChains(self.driver)\
            .click(clickable)\
            .perform()
        time.sleep(0.25)

        self.driver.refresh()
        time.sleep(0.25)
        self.driver.refresh()
        time.sleep(0.5)
    
    def report_logs(self, exp):
        self.get_contact(self.support_contact_name)
        self.send_message(exp)

    def execution(self):
        for i in range(len(self.csv_data)):
            self.get_item(item_index=i)
            if self.item[6]:
                self.save_contact()
            else:
                continue
            if not self.get_contact(f"کد {self.item[0]} {self.contact_prefix}"):
                self.update_csv(self.file_dir, i)
                continue
            if not self.item[7]:
                continue
            else:
                self.send_message(self.message_pattern)
            self.get_chat_id()
            self.remove_contact()
            self.update_csv(self.file_dir, i)

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    application = Eitaa(csv_path="data_csv.csv", init_chat_id="333000", prefix= "اطلاع رسانی بیمه", chrome_profile_path= "user-data-dir=C:\\Users\\amira\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1", dev_chat_id="", dev_name="", message="همکار محترم دانشگاه علوم پزشکی تبریز %s %s؛\n به استحضار می رساند آخرین مهلت ثبت نام بیمه درمان تکمیلی و عمر و حوادث کارکنان دانشگاه تا پایان وقت اداری مورخ 1403/11/15 می باشد. جهت ثبت نام به رابطین رفاهی مرکز خود مراجعه فرمایید؛ همچنین جهت کسب اطلاعات بیشتر می توانید از نشانی www.bimeh197.ir بازدید فرمایید.")

    application.read_csv()
    application.get_url(f"https://web.eitaa.com/#{application.inti_chat_id}")

    application.execution()
    
    application.close()