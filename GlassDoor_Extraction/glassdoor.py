from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.action_chains import ActionChains
import csv
from dateutil import parser
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

your_email = 'youremail'
your_password = 'yourpassword'

def convert_date_format_without_datetime(date):
    # Dictionary to map month abbreviations to numeric values
    month_mapping = {
        'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
        'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
        'Sept': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
    }

    try:
        # Split the date into day, month, and year
        day, month, year = date.split()
        
        # Convert the month abbreviation to numeric value
        month_numeric = month_mapping.get(month)
        
        # Create the formatted date
        formatted_date = f"{day}/{month_numeric}/{year}"
        
        return formatted_date
    except ValueError:
        # Handle the case where the date format is not as expected
        print(f"Error converting date: {date}")
        return None


feedback = []
overall_rating = []
position = []
location = []
service_time = []
pros = []
cons = []
date=[]
recommend=[]	
ceoapproval=[]	
business_outlook=[]	
subrating_counts = {
    "Work/Life Balance": [],
    "Culture and Values": [],
    "Diversity and Inclusion": [],
    "Career Opportunities": [],
    "Compensation and Benefits": [],
    "Senior Management": []
}



driver = webdriver.Chrome()

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
driver.get(target_url)
driver.maximize_window()
time.sleep(2)
resp = driver.page_source



filter_button = driver.find_element(By.XPATH, "//button[@class='css-1o3mc0h']")
filter_button.click()
time.sleep(2)

while True:
    resp = driver.page_source
    soup = BeautifulSoup(resp, 'html.parser')
    sub_rating_containers = driver.find_elements(By.CLASS_NAME, "review-details__review-details-module__subRatingContainer")

    # Iterate over each subRatingContainer
    for ind, sub_rating_container in enumerate(sub_rating_containers, start=1):
        # Check if the ratingCaret element is available
        rating_caret = sub_rating_container.find_elements(By.CLASS_NAME, "review-details__review-details-module__ratingCaret")
        
        if rating_caret:
            # Hover over the element
            ActionChains(driver).move_to_element(rating_caret[0]).perform()

            # Get the page source after the hover
            page_source = driver.page_source

            # Parse the page source with BeautifulSoup
            soup = BeautifulSoup(page_source, 'html.parser')

            # Iterate over each review box
            sub_ratings = sub_rating_container.find_elements(By.CLASS_NAME, "review-details__review-details-module__subRating")

            # Initialize a dictionary to store counts for the current subrating container
            current_subrating_counts = {key: None for key in subrating_counts}

            for sub_rating in sub_ratings:
                subr = sub_rating.text
                stars = sub_rating.find_elements(By.CLASS_NAME, "rating-star__rating-star-module__RatingStarContainer")
                count = 0
                
                for star in stars:
                    style_attribute = star.get_attribute("style")
                    if "--outline-percentage: 0%" in style_attribute:
                        count += 1

                # Assign count to corresponding subrating in the current_subrating_counts dictionary
                current_subrating_counts[subr] = count

            # Append the counts for the current subrating container to the main dictionary
            for key, value in current_subrating_counts.items():
                subrating_counts[key].append(value)

        else:
            # If no hover is available, append None for all subratings in the main dictionary
            for key in subrating_counts:
                subrating_counts[key].append(None)
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


        context_boxes = review_box.find_all('div', {'class': 'review-details__review-details-module__ratingDetail'})
        for context_box in context_boxes:
            context_name_box = context_box.find('span', {'class': 'review-details__review-details-module__ratingTitle'})
            # print(context_name_box)
            context_name = context_name_box.get_text(strip=True) if context_name_box else None
            # print(context_name)

            if context_name=="Recommend":
                if context_box.find('span', {'class': 'review-details__review-details-module__positiveStyles'}):
                    recommend.append("Yes")
                else:
                    recommend.append("No")
            if context_name=="CEO Approval":
                if context_box.find('span', {'class': 'review-details__review-details-module__positiveStyles'}):
                    ceoapproval.append("Yes")
                else:
                    ceoapproval.append("No")
            if context_name=="Business Outlook":
                if context_box.find('span', {'class': 'review-details__review-details-module__positiveStyles'}):
                    business_outlook.append("Yes")
                else:
                    business_outlook.append("No")


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




# Assuming your lists are already populated with data

# Combine your lists into a list of rows
rows = list(zip(feedback, overall_rating, position, location, service_time, pros, cons, date, recommend, ceoapproval, business_outlook,subrating_counts["Work/Life Balance"],subrating_counts["Culture and Values"],subrating_counts["Diversity and Inclusion"],subrating_counts["Career Opportunities"],subrating_counts["Compensation and Benefits"],subrating_counts["Senior Management"]))

formatted_dates = [convert_date_format_without_datetime(d) for d in date]

# Combine the formatted date with other data
rows = list(zip(feedback, overall_rating, position, location, service_time, pros, cons, formatted_dates, recommend, ceoapproval, business_outlook,subrating_counts["Work/Life Balance"],subrating_counts["Culture and Values"],subrating_counts["Diversity and Inclusion"],subrating_counts["Career Opportunities"],subrating_counts["Compensation and Benefits"],subrating_counts["Senior Management"]))
# Specify the CSV file path
csv_file_path = 'final_output.csv'

# Write to CSV file
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    # Create a CSV writer object
    csv_writer = csv.writer(csvfile)

    # Write header
    header = ["feedback", "overall_rating", "position", "location", "service_time", "pros", "cons", "date", "recommend", "ceoapproval", "business_outlook","Work/Life Balance","Culture and Values","Diversity and Inclusion","Career Opportunities","Compensation and Benefits","Senior Management"]
    csv_writer.writerow(header)

    # Write rows
    csv_writer.writerows(rows)

print(f"CSV file '{csv_file_path}' created successfully.")

