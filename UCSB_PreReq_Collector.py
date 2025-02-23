# !pip install selenium

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

driver = webdriver.Chrome()
base_url = "https://catalog.ucsb.edu/courses?sortBy=code&cq="
driver.get(base_url)
time.sleep(1)

dropdown_button = driver.find_element(By.XPATH, "//div[@class='vs__actions']")
dropdown_button.click()

time.sleep(0.5)

input_major = driver.find_element(By.XPATH, "//input[@id='departments']")
text_input = "Computer Science"
input_major.send_keys(text_input)

try:
    # Adjust the locator to match your dropdown options
    options = WebDriverWait(driver, 2).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, "vs__dropdown-menu"))  # Replace with the actual class for suggestions
    )

    # Loop through the options and select the desired one
    for option in options:
        print(option.text)
        if text_input in option.text:  # Replace with the desired option text
            print("found")
            option.click()  # Click on the option to select it
            break
except Exception as e:
    print("No options found or an error occurred:", e)

time.sleep(3)

while True:
    try:
        elements = WebDriverWait(driver, 1).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[@aria-posinset]"))  # Replace with the actual class name or locator
        )

        print(len(elements))
        # Iterate through the elements and click each one
        for element in elements:

            # open sidetab with course info
            course_link = element.find_element(By.XPATH, ".//a")
            driver.execute_script("arguments[0].click();", course_link)

            addi_course_info = driver.find_element(By.XPATH, "//aside[@aria-label='Additional Course Information']")
            try:
                prereq_found = WebDriverWait(addi_course_info, 3).until(
                    EC.presence_of_element_located((By.XPATH, "//section"))
                )  # Adjust the locator accordingly

                pre_req = prereq_found.find_element(By.XPATH, ".//section")
                print(pre_req.text)

            except (TimeoutException, NoSuchElementException):
                print("Section not found, skipping to next item.")
                continue

            html = driver.page_source
            with open('course_page.html', 'w', encoding='utf-8') as file:
                file.write(html)

            # Open the file in read mode
            with open('course_page.html', 'r', encoding='utf-8') as file:
                content = file.read()
            #print(content)
            #print(len(pre_req))
            time.sleep(0.1)

    except Exception as e:
        print("An error occurred:", e)

    next_page = driver.find_element(By.XPATH, "//button[@aria-label='Next page']")
    if next_page.get_attribute("disabled") == None:
        driver.execute_script("arguments[0].click();", next_page)
    else:
        break
    """
    try:
        next_page = driver.find_element(By.XPATH, "//button[@aria-label='Next page']")
        driver.execute_script("arguments[0].scrollIntoView(true);", next_page)
        time.sleep(1)
        next_page.click()
        time.sleep(3)
    except:
        print("No more pages or button not clickable.")
        break
    """

time.sleep(5)
driver.quit()
