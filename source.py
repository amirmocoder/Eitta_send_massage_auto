# stable version for Eitta Web 4.6.10

# import required libraries
import time
import re
import csv
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from chromedriver_py import binary_path

# create class of program
class Eitaa:
    def __init__(self, csv_path, init_chat_id, prefix, chrome_profile_path, dev_chat_id, message):
        # initialize the webdriver and chrome profile and other variables
        self.driver_path = binary_path
        self.options = Options()
        self.options.add_argument(chrome_profile_path)
        self.options.add_argument("--start-minimized")
        self.svc = webdriver.ChromeService(executable_path=self.driver_path)
        self.driver = webdriver.Chrome(service=self.svc, options=self.options)
        self.contact_prefix = prefix
        self.inti_chat_id = init_chat_id
        self.support_chat_id = dev_chat_id
        self.message_pattern = message
        self.file_dir = csv_path
        self.count_error = 0
        self.count_timeout = 0

    # to open given url
    def get_url(self, url):
        self.driver.get(url)
        time.sleep(0.5)
        self.driver.refresh()
        time.sleep(0.5)

    # to read data the csv file of program work with it (input and output are same file) as csv_data array
    def read_csv(self):
        with open(self.file_dir, mode='r', newline='', encoding='utf-8-sig') as f:
            self.csv_data = list(csv.reader(f))

    # to get a record of table and assign it to item
    def get_item(self, item_index):
        self.item= self.csv_data[item_index]
    
    # some actions to save item in contact
    def save_contact(self):
        # press the pencel icon
        clickable = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/div/div/div[2]/div[3]/div[1]")
        ActionChains(self.driver)\
            .click(clickable)\
            .perform()
        time.sleep(0.25)

        # press the new message icon
        clickable = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/div/div/div[2]/div[3]/div[3]/div[3]")
        ActionChains(self.driver)\
            .click(clickable)\
            .perform()
        time.sleep(0.25)
        
        # press the + icon
        clickable = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/div/div[2]/div[2]/button/div")
        ActionChains(self.driver)\
            .click(clickable)\
            .perform()
        time.sleep(0.25)

        # fill name and prefix and phone number of item as creating contact
        self.driver.execute_script(f"arguments[0].textContent = 'کد {self.item[0]}';", self.driver.find_element(By.XPATH,"/html/body/div[5]/div/div[2]/div[1]/div[1]"))
        self.driver.execute_script(f"arguments[0].textContent = '{self.contact_prefix}';", self.driver.find_element(By.XPATH,"/html/body/div[5]/div/div[2]/div[2]/div[1]"))
        clickable = self.driver.find_element(By.XPATH,"/html/body/div[5]/div/div[3]/div[1]")
        clickable.click()
        time.sleep(0.25)

        # fill phone number digit by digit for sensitive inputs like that
        for digit in self.item[3]:
            clickable.send_keys(digit)
            time.sleep(0.0625)

        # press the add to contact button
        clickable = self.driver.find_element(By.XPATH, "/html/body/div[5]/div/div[1]/button/div")
        ActionChains(self.driver)\
            .click(clickable)\
            .perform()
        time.sleep(0.25)

        # refresh twice to update contact list
        self.driver.refresh()
        time.sleep(0.25)
        self.driver.refresh()
        time.sleep(0.5)

    # find and bring chat-screen of added contact if founded returns 1 else returns 0
    def get_contact(self, content):
        # press the search-bar
        clickable = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/div/div/div[1]/div[2]")
        ActionChains(self.driver)\
            .click(clickable)\
            .perform()
        time.sleep(0.25)

        # insert the contact info to search added contact
        clickable = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/div/div/div[1]/div[2]/input")
        ActionChains(self.driver)\
            .click(clickable)\
            .perform()
        clickable.send_keys(content)
        time.sleep(0.25)

        try:
            # press the first result from search result as founded contact to froward chat-screen if exists
            clickable = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/div/div/div[2]/div[2]/div[3]/div/div/div[1]/div/div/ul/li[1]")
            ActionChains(self.driver)\
                .click(clickable)\
                .perform()
            time.sleep(0.25)

            # checks if search result is empty or not
            if self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div/span").text == content:
                return 1
            else:
                return 0
        # try and exception "NoSuchElementException" error to handel missed element caused by empty result searching
        except NoSuchElementException:
            return 0
    
    # get and adds the chat-id current contact by fetching it from chat-page url
    def get_chat_id(self):
        self.item[8] = re.search(r"#\d+",self.driver.current_url).group()

    # to send a given massage on current chat, checks if succeed returns 1 else returns 0
    def send_message(self, message):
        try:
            # press the chat-bar to make text-cursor appear
            clickable = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/div/div/div[4]/div/div[1]/div[7]/div[1]")
            ActionChains(self.driver)\
                .click(clickable)\
                .perform()
            time.sleep(0.25)

            # insert the massage to chat-bar
            self.driver.execute_script(f"arguments[0].innerText = arguments[1];", self.driver.find_element(By.XPATH,"/html/body/div[2]/div[1]/div[2]/div/div/div[4]/div/div[1]/div[7]/div[1]/div[1]"), message)
            time.sleep(0.0625)
            
            # press the send icon
            clickable = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/div/div/div[4]/div/div[4]/button/div")
            ActionChains(self.driver)\
                .click(clickable)\
                .perform()
            time.sleep(0.25)
            
            # checks massage sent and returns 1 if the chat-bar was empty else returns 0
            if self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/div/div/div[4]/div/div[1]/div[7]/div[1]/div[1]").text == "":
                return 1
            else:
                return 0
        # try and exception "NoSuchElementException" error to handel missed elements
        except NoSuchElementException:
            return 0
    
    # to update current item information on csv file used for live updating item by item
    def update_csv(self, row):
        self.csv_data[row] = self.item
        with open(self.file_dir, mode='w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerows(self.csv_data)

    # to drop current contact prevents fulling contact list and search contact problem for next items
    def remove_contact(self):
        
        # press contact name to open current contact profile
        clickable = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/div/div/div[2]/div[1]/div")
        ActionChains(self.driver)\
            .click(clickable)\
            .perform()
        time.sleep(0.25)
        
        # press more option icon
        clickable = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[3]/div/div/div[1]/div/div[1]/button")
        ActionChains(self.driver)\
            .click(clickable)\
            .perform()
        time.sleep(0.25)

        # press drop contact
        clickable = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[3]/div/div[2]/div[2]/div/div[2]/div/div")
        ActionChains(self.driver)\
            .click(clickable)\
            .perform()
        time.sleep(0.25)
        
        # press to agree to drop current contact
        clickable = self.driver.find_element(By.XPATH, "/html/body/div[5]/div/div[2]/button[1]")
        ActionChains(self.driver)\
            .click(clickable)\
            .perform()
        time.sleep(0.25)

        # refresh twice to update contact list
        self.driver.refresh()
        time.sleep(0.25)
        self.driver.refresh()
        time.sleep(0.5)
    
    # to report bugs or logs of running process using a third-party messenger
    def report_logs(self, exp):
        parse_url = "https://tapi.bale.ai/406394701:1qgLsOLSAqoswcdmLvfTOPpQA6glRlrfEvM5il9O/sendMessage"
        return requests.post(parse_url, json= {'chat_id':f'{self.support_chat_id}', 'text': f'{exp}'})

    # main function executed to auto send patterned message
    def execution(self):
        # count checked record for reporting
        count_break_point = [0,1]
        # iteration on each records as row index i
        for i in range(len(self.csv_data)):
            try:
                self.get_item(item_index=i)
                # checks if current item as a contact has "Eitaa" acount or not if has not account, the remained process will skipped for this record
                if self.item[6]:
                    self.save_contact()
                else:
                    continue

                # gets chat-screen of current item as a contact, if could not gets which mean the contact has not "Eitaa" acount so changes the related column amount to 0 and updates the record with,the remained process will skipped for this record
                if not self.get_contact(f"کد {self.item[0]} {self.contact_prefix}"):
                    self.item[6]= 0
                    self.update_csv(row= i)
                    continue
                # checks if the massage sent before for current item as a contact, the remained process will skipped for this record else sends the message to current user and changes the related column amount to 1, if was not successful the "NoMessageSendError" will be raised
                if not self.item[7]:
                    self.remove_contact()
                    continue
                else:
                    if self.send_message(self.message_pattern  % (self.item[1], self.item[2])):
                        self.item[7]= 1
                    else:
                        raise TypeError("NoMessageSendError")

                self.get_chat_id()
                self.remove_contact()

                # reset the error counter if the process for this record was successfully done then updates file
                self.count_error = 0
                self.update_csv(row= i)
                
                # this gonna report every 1000 record was processed
                count_break_point[0] = i
                if count_break_point[0] >= 1000:
                    try:
                        self.report_logs(f"done for {count_break_point[1]}th, {count_break_point[0]} group of people!")
                    except:
                        pass
                    count_break_point[0] = 0
                    count_break_point[1] += 1

            # try and exception "NoSuchElementException" to handel missed element, the program will be start again recursively, if this error happens for several times the program will be stopped and reported
            except NoSuchElementException as exp:
                self.count_error += 1
                if self.count_error >= 10:
                    self.report_logs(f"running process stopped during gotten several {exp} error!")
                    break
                
                self.driver.refresh()
                time.sleep(0.25)
                self.driver.refresh()
                time.sleep(0.5)

                self.read_csv()
                self.get_url(f"https://web.eitaa.com/#{application.inti_chat_id}")
                self.execution()
            
            # try and exception "TimeoutError" to handel poor or lose connection, the program will be interrupt for minutes, if this error happens for several times the program will be stopped and reported
            except TimeoutError as exp:
                self.count_timeout += 1
                self.update_csv(row= i)
            
                if self.count_error >= 5:
                    self.report_logs(f"running process stopped during gotten several {exp} error!")
                    break

                time.sleep(600)

                self.read_csv()
                self.get_url(f"https://web.eitaa.com/#{application.inti_chat_id}")
                self.execution()
            
            # try and exception "NoMessageSendError" to handel missed sending, this will be reported and skipped for current record
            except "NoMessageSendError" as exp:
                try:
                    self.report_logs(f"{exp} for record {self.item[0]}")
                except:
                    pass
                continue
    
    # to close driver
    def close(self):
        self.driver.quit()

# initialize program
if __name__ == "__main__":
    # use program call the parameters are file_path, initialize chat-id to start, prefix for make contact saving regular, a chrome profile path to save login credentials, report user chat_id on third-party platform, patterned message
    application = Eitaa(csv_path="data_csv.csv", init_chat_id="333000", prefix= "اطلاع رسانی بیمه", chrome_profile_path= "user-data-dir=C:\\Users\\amira\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1", dev_chat_id= "431600925", message="همکار محترم دانشگاه علوم پزشکی تبریز %s %s؛\n به استحضار می رساند آخرین مهلت ثبت نام بیمه درمان تکمیلی و عمر و حوادث کارکنان دانشگاه تا پایان وقت اداری مورخ 1403/11/15 می باشد. جهت ثبت نام به رابطین رفاهی مرکز خود مراجعه فرمایید؛ همچنین جهت کسب اطلاعات بیشتر می توانید از نشانی www.bimeh197.ir بازدید فرمایید.")

    application.read_csv()
    application.get_url(f"https://web.eitaa.com/#{application.inti_chat_id}")

    application.execution()
    
    application.close()