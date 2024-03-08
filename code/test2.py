from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# data List
Title = []
Phone = []
Address = []
Rating = []
Review  = []
Category = []

def scroll(driver):
    try:
            # specific element containing buttons
        container_element = driver.find_element(By.CSS_SELECTOR, '#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd')

            # Scroll down
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', container_element)
        time.sleep(2)  # Add a short delay to allow scrolling to take effect

    except:
            # Handle stale element reference exception by re-finding the container element
            pass


# Collect data function.
def collect_data(driver):
    try:
        # collecting name of the busniess
        title =  driver.find_element(By.CLASS_NAME, 'DUwDvf ')
        Title.append(title.text)

        # collecting category of the business.
        category = driver.find_element(By.CLASS_NAME, 'DkEaL ')
        Category.append(category.text)

        # collecting description (address, phone no)
        desc = driver.find_elements(By.CLASS_NAME, 'Io6YTe')
        Address.append(desc[0].text)
        i =0
        endlist = len(desc)
        for item in desc:
            no  = item.text.replace(" ", "")
            if no.isdigit():
                Phone.append(no)
                break
            if i == endlist-1:
                Phone.append("")
            i=i+1

        # collecting rating and review data
        try:
            rat_rev =  driver.find_elements(By.CLASS_NAME, 'F7nice ')

            open_bracket_index = rat_rev[0].text.find('(')
            close_bracket_index = rat_rev[0].text.find(')')
            rating  = rat_rev[0].text[:open_bracket_index].strip()
            review =  rat_rev[0].text[open_bracket_index + 1:close_bracket_index].strip()
            Rating.append(rating)
            Review.append(review)
        except:
            Rating.append("NA")
            Review.append("NA")
        
    except:
        print(" Internet Connection is slow, adject sleep time...")
    
def write_data(filename):
    data = {'Category': Category, 'Name': Title, 'Address': Address,'Phone No': Phone,'Rating': Rating, 'Review Count': Review}
    df = pd.DataFrame(data)
    excel_file_path = str(filename) +".xlsx"

    df.to_excel(excel_file_path, index=False)

    print(f'Data written to {excel_file_path}')

def main():
    # inputs 
    print("NOTE: If you notice any errors, please increase the sleep time. If you have a good system and internet connection, you can reduce your sleep time.")
    keyword =  input("Enter Busniess name(Example: Hospitals in delhi): ")
    filename =  input("Enter the path and file name (Example: C:/Users/hp/Downloads/output): ")
    # Set up the driver

    driver = webdriver.Chrome()

    # Navigate to the map page
    driver.get('https://www.google.com/maps/search/'+str(keyword))

    # Wait for the map to load
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd')))


# Repeat the process (adjust the number of iterations as needed)
    while True:
        try:
            end = driver.find_element(By.CSS_SELECTOR, "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd.QjC7t > div.m6QErb.tLjsW.eKbjU > div > p > span > span")
            # terminate condition
            if end != "":
                time.sleep(50)
                break
        except:
            pass

        scroll(driver)

        # traversing one by one all business
    buttons = driver.find_elements(By.CLASS_NAME, 'hfpxzc')
    i =1
    for button in buttons:
        try:
            button.click()
            time.sleep(15)
            collect_data(driver)
            print(i,"Row collected")
        except:
            continue
        i=i+1

    print("All data ready wait for just few moments")
    write_data(filename)
    time.sleep(2)
    driver.quit()


# Run main function
main()
