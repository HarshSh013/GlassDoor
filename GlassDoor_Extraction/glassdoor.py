from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
feedback = []
overall_rating = []
position = []
location = []
service_time = []
pros = []
cons = []
date=[]


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
driver = webdriver.Chrome()


your_email = 'youremail'
your_password = 'yourpassword'

login_url = "https://www.glassdoor.co.in/index.htm"
driver.get(login_url)
driver.maximize_window()
email_input = driver.find_element("id", "inlineUserEmail")
email_input.send_keys(your_email)
email_input.submit()
time.sleep(2)
email_input = driver.find_element("id", "inlineUserPassword")
email_input.send_keys(your_password)
email_input.submit()
resp = driver.page_source
time.sleep(5)

target_url = "https://www.glassdoor.co.in/Reviews/Blackcoffer-Reviews-E2260916.htm"
# driver.get("https://hq.ssrn.com/login/pubsigninjoin.cfm")

# driver=webdriver.Chrome(PATH)
driver.get(target_url)
driver.maximize_window()
time.sleep(2)
resp = driver.page_source



# soup=BeautifulSoup(resp,'html.parser')
# for x in soup.find_all('a', {'class':'review-details__review-details-module__detailsLink review-details__review-details-module__title'}):
#     feedback.append(x.text)

filter_button = driver.find_element(By.XPATH, "//button[@class='css-1o3mc0h']")
filter_button.click()
time.sleep(2)

while True:
    # Extract data from the current page
    resp = driver.page_source
    soup = BeautifulSoup(resp, 'html.parser')
    #Feedback
    for review_box in soup.find_all('div', {'class': 'review-details__review-details-module__topReview'}):
        # Feedback
        feedback_box = review_box.find('a', {'class': 'review-details__review-details-module__detailsLink review-details__review-details-module__title'})
        feedback.append(feedback_box.get_text(strip=True) if feedback_box else None)

        # Overall Rating
        overall_rating_box = review_box.find('span', {'class': 'review-details__review-details-module__overallRating'})
        overall_rating.append(overall_rating_box.get_text(strip=True) if overall_rating_box else None)

        # Position
        position_box = review_box.find('span', {'class': 'review-details__review-details-module__employee'})
        position.append(position_box.get_text(strip=True) if position_box else None)

        # Location
        location_box = review_box.find('span', {'class': 'review-details__review-details-module__location'})
        location.append(location_box.get_text(strip=True) if location_box else None)

        # Service Time
        service_time_box = review_box.find('div', {'class': 'review-details__review-details-module__employeeDetails'})
        service_time.append(service_time_box.get_text(strip=True) if service_time_box else None)

        # Pros
        pros_box = review_box.find('span', {'data-test': 'pros'})
        pros.append(pros_box.get_text(strip=True) if pros_box else None)

        # Cons
        cons_box = review_box.find('span', {'data-test': 'cons'})
        cons.append(cons_box.get_text(strip=True) if cons_box else None)

        datebox = review_box.find('span', {'class': 'review-details__review-details-module__reviewDate'})
        date.append(datebox.get_text(strip=True) if datebox else None)




        
    # for x in soup.find_all('span', {'class': 'review-details__review-details-module__reviewDate'}):
    #     date.append(x.get_text(strip=True))






    
    # Click the "Next" button to go to the next page
    try:
        next_button = driver.find_element(By.XPATH, "//button[@data-test='pagination-next']")
        next_button.click()
        
        # Wait for the next page to load before proceeding
        WebDriverWait(driver, 10).until(
            EC.staleness_of(next_button)
        )
        
        time.sleep(3) 
    except:
        # If there is no "Next" button or an error occurs, break the loop
        break


driver.close()
import csv
from dateutil import parser

# Assuming your lists are already populated with data

# Combine your lists into a list of rows
rows = list(zip(feedback, overall_rating, position, location, service_time, pros, cons, date))

# Convert date to the desired format
formatted_date = [parser.parse(d).strftime("%d-%m-%y") for d in date]

# Combine the formatted date with other data
rows = list(zip(feedback, overall_rating, position, location, service_time, pros, cons, formatted_date))

# Specify the CSV file path
csv_file_path = 'output.csv'

# Write to CSV file
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    # Create a CSV writer object
    csv_writer = csv.writer(csvfile)

    # Write header
    header = ["feedback", "overall_rating", "position", "location", "service_time", "pros", "cons", "date"]
    csv_writer.writerow(header)

    # Write rows
    csv_writer.writerows(rows)

print(f"CSV file '{csv_file_path}' created successfully.")
