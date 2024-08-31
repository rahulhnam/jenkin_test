from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import datetime
import data_push
from itertools import islice
import os


api_url = "http://ec2-54-254-162-245.ap-southeast-1.compute.amazonaws.com:9000/items/"

def launch_browser_and_click_link(link_text):
    """
    Launches a browser, opens IndianExpress.com, and clicks on the specified link.

    Args:
    link_text (str): The text of the link to click ("India," "Sports," "Business," or "Politics").
    """
    # Choose your preferred browser driver (e.g., Chrome, Firefox)
    driver_r = "D:\FYERS\chromedriver-win64\chromedriver-win64\chromedriver.exe"  # Replace with 'webdriver.Firefox()' for Firefox
    driver = webdriver.Chrome(executable_path=driver_r)
    driver.get("https://indianexpress.com/")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "slick-track"))
    )
    print("Page loaded successfully.")
    j_data = {"name": "string",  "description": "string",  "price": 0,  "item_type": "string"}
    data_arr = []
    try:
        # Use a more robust approach to find the link by its text content within a specific element
        link = driver.find_element(By.XPATH, "/html/body/main/header/nav/div/ul/li[8]/a")
        link.click()
        # print(f"Clicked on the '{link_text}' link.")
        wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed
        wait.until(EC.number_of_windows_to_be(2))

        new_window = driver.window_handles[-1]
        driver.switch_to.window(new_window)
        time.sleep(4)
       
        ul_element = driver.find_element(By.CLASS_NAME, "slick-dots")
        # Find all <li> elements inside the <ul>
        li_elements = ul_element.find_elements(By.TAG_NAME, "li")
        count = 0
        # Loop through each <li> element
        for li in li_elements:
            try:
                # Find the <button> tag within the <li> and click it
                if count >= 3:
                    break
                time.sleep(3)
                button = li.find_element(By.TAG_NAME, "button")
                button_id = button.get_attribute('id')
                button.click()
                #print("clicked", li._id)

                target_li = driver.find_element(By.XPATH, f"//li[@aria-describedby='{button_id}']")
                anchor_element = target_li.find_element(By.TAG_NAME, 'a')
                href_link = anchor_element.get_attribute('href')
                j_data["description"] = href_link
                driver.execute_script(f"window.open('{href_link}');")
                # a_tag.send_keys(Keys.COMMAND + Keys.RETURN)  # For macOS
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(1)

                element = driver.find_element(By.XPATH, '//h1[@itemprop="headline" and @class="native_story_title"]')
                text = element.text
                j_data["name"] = text

                element = driver.find_element(By.XPATH, '//h1[@itemprop="headline" and @class="native_story_title"]')
                text = element.text
                j_data["name"] = text

                element = driver.find_element(By.XPATH, '//span[@itemprop="dateModified"]')
                content_value = element.get_attribute('content')

                datetime_string = content_value

                # Parse the datetime string into a datetime object
                datetime_object = datetime.datetime.fromisoformat(datetime_string)

                # Extract the date components from the datetime object
                day = datetime_object.day
                month = datetime_object.month
                year = datetime_object.year

                # Format the date in DDMMYYYY format
                date_string = f"{day:02d}{month:02d}{year}"

                j_data["price"] = float(date_string)
                j_data["item_type"] = "Alstom"

                driver.close()

                driver.switch_to.window(driver.window_handles[-1])

                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/main/div[5]/div/div/div[3]/div[1]/div/div/div[1]/ul/div"))
                    )
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "slick-dots"))
                    )
                time.sleep(3)
                ul_element = driver.find_element(By.CLASS_NAME, "slick-dots")
                # Find all <li> elements inside the <ul>
                li_elements = ul_element.find_elements(By.TAG_NAME, "li")
                count += 1
                
            except Exception as e:
                print(f"An error occurred: {e}")
                continue
            data_arr.append(j_data)
        print(data_arr)
    except Exception as e:
        print(f"An error occurred: {e}")

    # Close the browser after the action
    driver.quit()
    return data_arr
# Example usage
link_to_click = "Politics"  # Replace with "Sports", "Business", or "Politics"
dat_arr = launch_browser_and_click_link(link_to_click)
cropped_array = list(islice(dat_arr, 3))
item_id = data_push.push_data_to_api(api_url, cropped_array)
Pass_Fail = data_push.validate_data_to_api(api_url, cropped_array, item_id)

folder_path = os.path.dirname(os.path.realpath(__file__))
os.startfile(folder_path)