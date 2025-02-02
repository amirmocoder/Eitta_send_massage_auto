# MIT License

# Copyright (c) 2025 Amirali Mohammadi

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# stable version for Eitaa Web 4.6.10

# Import required libraries
import time
import csv
import re
import requests
from chromedriver_py import binary_path
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Define global configuration variables
IMPLICIT_WAIT_TIME = 0.25
SHORT_WAIT_TIME = 0.0625
REFRESH_WAIT_TIME = 0.5
TIMEOUT_WAIT_TIME = 600
ERROR_THRESHOLD = 10
TIMEOUT_THRESHOLD = 5
REPORT_FREQUENCY = 50
MAIN_EITAA_URL = "https://web.eitaa.com/"
INDEX_CONTACT_LABEL = "Num. "
THIRD_PARTY_API_URL = "https://tapi.bale.ai/YfBRDpAxWQDtZKrcD7AbByScCIsK4Bip38Ff3qAg/sendMessage"

# Create a class for the Eitaa automation
class Eitaa:
    def __init__(
        self, csv_path, init_chat_id, prefix, chrome_profile_path, dev_chat_id, message
    ):
        # Initialize the webdriver, Chrome profile, and other variables
        self.driver_path = binary_path
        self.options = Options()
        self.options.add_argument(chrome_profile_path)
        self.options.add_argument("--headless")
        self.svc = webdriver.ChromeService(executable_path=self.driver_path)
        self.driver = webdriver.Chrome(service=self.svc, options=self.options)
        self.contact_prefix = prefix
        self.inti_chat_id = init_chat_id
        self.support_chat_id = dev_chat_id
        self.message_pattern = message
        self.file_dir = csv_path
        self.count_error = 0
        self.count_timeout = 0

    # Opens the given URL in the browser
    def get_url(self, url):
        self.driver.get(url)
        time.sleep(REFRESH_WAIT_TIME)
        self.driver.refresh()
        time.sleep(REFRESH_WAIT_TIME)

    # Reads data from the CSV file. Input and output are the same file, stored as csv_data array.
    def read_csv(self):
        with open(self.file_dir, mode="r", newline="", encoding="utf-8-sig") as f:
            self.csv_data = list(csv.reader(f))

    # Gets a record from the table and assigns it to 'item'
    def get_item(self, item_index):
        self.item = self.csv_data[item_index]

    # Actions to save the item as a contact
    def save_contact(self):
        # Click the pencil icon
        clickable = self.driver.find_element(
            By.XPATH, "/html/body/div[2]/div[1]/div[1]/div/div/div[2]/div[3]/div[1]"
        )
        ActionChains(self.driver).click(clickable).perform()
        time.sleep(IMPLICIT_WAIT_TIME)

        # Click the new message icon
        clickable = self.driver.find_element(
            By.XPATH,
            "/html/body/div[2]/div[1]/div[1]/div/div/div[2]/div[3]/div[3]/div[3]",
        )
        ActionChains(self.driver).click(clickable).perform()
        time.sleep(IMPLICIT_WAIT_TIME)

        # Click the + icon
        clickable = self.driver.find_element(
            By.XPATH, "/html/body/div[2]/div[1]/div[1]/div/div[2]/div[2]/button/div"
        )
        ActionChains(self.driver).click(clickable).perform()
        time.sleep(IMPLICIT_WAIT_TIME)

        # Fill in the name, prefix, and phone number of the item to create a new contact
        self.driver.execute_script(
            f"arguments[0].textContent = '{INDEX_CONTACT_LABEL} {self.item[0]}';",
            self.driver.find_element(
                By.XPATH, "/html/body/div[5]/div/div[2]/div[1]/div[1]"
            ),
        )
        self.driver.execute_script(
            f"arguments[0].textContent = '{self.contact_prefix}';",
            self.driver.find_element(
                By.XPATH, "/html/body/div[5]/div/div[2]/div[2]/div[1]"
            ),
        )
        clickable = self.driver.find_element(
            By.XPATH, "/html/body/div[5]/div/div[3]/div[1]"
        )
        clickable.click()
        time.sleep(IMPLICIT_WAIT_TIME)

        # Fill in the phone number digit by digit for sensitive inputs
        for digit in self.item[3]:
            clickable.send_keys(digit)
            time.sleep(SHORT_WAIT_TIME)

        # Click the add to contact button
        clickable = self.driver.find_element(
            By.XPATH, "/html/body/div[5]/div/div[1]/button/div"
        )
        ActionChains(self.driver).click(clickable).perform()
        time.sleep(IMPLICIT_WAIT_TIME)

        # Refresh the page twice to update the contact list
        self.driver.refresh()
        time.sleep(IMPLICIT_WAIT_TIME)
        self.driver.refresh()
        time.sleep(REFRESH_WAIT_TIME)

    # Finds and returns the chat screen of the added contact. Returns 1 if found, 0 otherwise.
    def get_contact(self, content):
        # Click the search bar
        clickable = self.driver.find_element(
            By.XPATH, "/html/body/div[2]/div[1]/div[1]/div/div/div[1]/div[2]"
        )
        ActionChains(self.driver).click(clickable).perform()
        time.sleep(IMPLICIT_WAIT_TIME)

        # Insert the contact info to search
        clickable = self.driver.find_element(
            By.XPATH, "/html/body/div[2]/div[1]/div[1]/div/div/div[1]/div[2]/input"
        )
        ActionChains(self.driver).click(clickable).perform()
        clickable.send_keys(content)
        time.sleep(IMPLICIT_WAIT_TIME)

        try:
            # Click the first search result (the contact) to forward to their chat screen
            clickable = self.driver.find_element(
                By.XPATH,
                "/html/body/div[2]/div[1]/div[1]/div/div/div[2]/div[2]/div[3]/div/div/div[1]/div/div/ul/li[1]",
            )
            ActionChains(self.driver).click(clickable).perform()
            time.sleep(IMPLICIT_WAIT_TIME)

            # Checks if search result is empty or not
            if (
                self.driver.find_element(
                    By.XPATH,
                    "/html/body/div[2]/div[1]/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div/span",
                ).text
                == content
            ):
                return 1
            else:
                return 0
        # Handles "NoSuchElementException" if the search result is empty
        except NoSuchElementException:
            return 0

    # Gets the chat ID of the current contact by fetching it from the chat page URL
    def get_chat_id(self):
        self.item[8] = re.search(r"#\w+", self.driver.current_url).group()

    # Sends a given message in the current chat. Returns 1 if successful, 0 otherwise.
    def send_message(self, message):
        try:
            # Click the chat bar to make the text cursor appear
            clickable = self.driver.find_element(
                By.XPATH,
                "/html/body/div[2]/div[1]/div[2]/div/div/div[4]/div/div[1]/div[7]/div[1]",
            )
            ActionChains(self.driver).click(clickable).perform()
            time.sleep(IMPLICIT_WAIT_TIME)

            # Insert the message into the chat bar
            self.driver.execute_script(
                f"arguments[0].innerText = arguments[1];",
                self.driver.find_element(
                    By.XPATH,
                    "/html/body/div[2]/div[1]/div[2]/div/div/div[4]/div/div[1]/div[7]/div[1]/div[1]",
                ),
                message,
            )
            time.sleep(SHORT_WAIT_TIME)

            # Click the send icon
            clickable = self.driver.find_element(
                By.XPATH,
                "/html/body/div[2]/div[1]/div[2]/div/div/div[4]/div/div[4]/button/div",
            )
            ActionChains(self.driver).click(clickable).perform()
            time.sleep(IMPLICIT_WAIT_TIME)

            # Checks if the message was sent and returns 1 if the chat bar is empty, 0 otherwise.
            if (
                self.driver.find_element(
                    By.XPATH,
                    "/html/body/div[2]/div[1]/div[2]/div/div/div[4]/div/div[1]/div[7]/div[1]/div[1]",
                ).text
                == ""
            ):
                return 1
            else:
                return 0
        # Handles "NoSuchElementException" if elements are missing
        except NoSuchElementException:
            return 0

    # Updates the current item information in the CSV file. Used for live updating.
    def update_csv(self, row):
        self.csv_data[row] = self.item
        with open(self.file_dir, mode="w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerows(self.csv_data)

    # Removes the current contact to avoid filling the contact list and causing search problems.
    def remove_contact(self):

        # Click on the contact name to open the contact profile
        clickable = self.driver.find_element(
            By.XPATH, "/html/body/div[2]/div[1]/div[2]/div/div/div[2]/div[1]/div"
        )
        ActionChains(self.driver).click(clickable).perform()
        time.sleep(IMPLICIT_WAIT_TIME)

        # Click the more options icon
        clickable = self.driver.find_element(
            By.XPATH, "/html/body/div[2]/div[1]/div[3]/div/div/div[1]/div/div[1]/button"
        )
        ActionChains(self.driver).click(clickable).perform()
        time.sleep(IMPLICIT_WAIT_TIME)

        # Click drop contact
        clickable = self.driver.find_element(
            By.XPATH,
            "/html/body/div[2]/div[1]/div[3]/div/div[2]/div[2]/div/div[2]/div/div",
        )
        ActionChains(self.driver).click(clickable).perform()
        time.sleep(IMPLICIT_WAIT_TIME)

        # Click to confirm dropping the contact
        clickable = self.driver.find_element(
            By.XPATH, "/html/body/div[5]/div/div[2]/button[1]"
        )
        ActionChains(self.driver).click(clickable).perform()
        time.sleep(IMPLICIT_WAIT_TIME)

        # Refresh the page twice to update the contact list
        self.driver.refresh()
        time.sleep(IMPLICIT_WAIT_TIME)
        self.driver.refresh()
        time.sleep(REFRESH_WAIT_TIME)

    # Reports bugs or logs of the running process using a third-party messenger.
    def report_logs(self, exp):
        return requests.post(
            THIRD_PARTY_API_URL, json={"chat_id": f"{self.support_chat_id}", "text": f"{exp}"}
        )

    # Main function to auto-send patterned messages
    def execution(self):
        # Count checked records for reporting
        count_break_point = [0, 1]
        # Iterate over each record (row) in the CSV data
        for i in range(len(self.csv_data)):
            try:
                self.get_item(item_index=i)
                # Check if the current item (contact) has an Eitaa account. If not, skip to the next record.
                if self.item[6]:
                    self.save_contact()
                else:
                    continue

                # Get the chat screen of the current contact. If not found (meaning the contact does not have an Eitaa account), update the related column and skip to the next record.
                if not self.get_contact(
                    f"{INDEX_CONTACT_LABEL} {self.item[0]} {self.contact_prefix}"
                ):
                    self.item[6] = 0
                    self.update_csv(row=i)
                    continue
                # Checks if a message has already been sent to the current contact. If so, skip this record. Otherwise, sends the message, updates the corresponding column, and raises "NoMessageSendError" if unsuccessful.
                if not self.item[7]:
                    self.remove_contact()
                    continue
                else:
                    if self.send_message(
                        self.message_pattern % (self.item[1], self.item[2])
                    ):
                        self.item[7] = 1
                    else:
                        raise TypeError("NoMessageSendError")

                self.get_chat_id()
                self.remove_contact()

                # Reset the error counter if the process for this record was successful, then update the CSV
                self.count_error = 0
                self.update_csv(row=i)

                # Reports progress every REPORT_FREQUENCY records
                count_break_point[0] = i
                if count_break_point[0] >= REPORT_FREQUENCY:
                    try:
                        self.report_logs(
                            f"done for {count_break_point[1]}th, {count_break_point[0]} group of people!"
                        )
                    except:
                        pass
                    count_break_point[0] = 0
                    count_break_point[1] += 1

            # Handles "NoSuchElementException" for missing elements. The program will restart recursively. If this error happens several times, the program will stop and report the error.
            except NoSuchElementException as exp:
                self.count_error += 1
                if self.count_error >= ERROR_THRESHOLD:
                    self.report_logs(
                        f"running process stopped during gotten several {exp} error!"
                    )
                    break

                self.driver.refresh()
                time.sleep(IMPLICIT_WAIT_TIME)
                self.driver.refresh()
                time.sleep(REFRESH_WAIT_TIME)

                self.read_csv()
                self.get_url(f"{MAIN_EITAA_URL}#{application.inti_chat_id}")
                self.execution()

            # Handles "TimeoutError" for poor connection. The program will pause. If this error happens several times, the program will stop and report the error.
            except TimeoutError as exp:
                self.count_timeout += 1
                self.update_csv(row=i)

                if self.count_error >= TIMEOUT_THRESHOLD:
                    self.report_logs(
                        f"running process stopped during gotten several {exp} error!"
                    )
                    break

                time.sleep(TIMEOUT_WAIT_TIME)

                self.read_csv()
                self.get_url(f"{MAIN_EITAA_URL}#{application.inti_chat_id}")
                self.execution()

            # Handles "NoMessageSendError" for missed sending. This will be reported and the record will be skipped.
            except TypeError as exp:
                try:
                    self.report_logs(f"{exp} for record {self.item[0]}")
                except:
                    pass
                continue

    # Closes the webdriver
    def close(self):
        self.driver.quit()


# Initialize the program
if __name__ == "__main__":
    # Program call parameters are: file_path, initial chat ID, prefix for saving contacts, Chrome profile path, reporting user chat ID, and patterned message.
    application = Eitaa(
        csv_path="data_csv.csv",
        init_chat_id="333000",
        prefix="the Client",
        chrome_profile_path="user-data-dir=C:\\Users\\amira\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1",
        dev_chat_id="000000000",
        message="%s %s,\nIn today's fast-paced business environment, optimizing your supply chain is crucial, and I understand how valuable your time is. Introducing ChainLink Pro, a cutting-edge solution designed to streamline your operations with real-time tracking, AI-powered analytics, and automated workflows. This tool offers unparalleled efficiency, providing clear visibility across your entire supply chain while reducing manual errors and saving you valuable time.",
    )

    application.read_csv()
    application.get_url(f"{MAIN_EITAA_URL}#{application.inti_chat_id}")

    application.execution()

    application.close()