from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time


# Credentials Entry (Temporary credential to scrape the data)
Celeb_name = ''
email = ''
user_name = ''
password_twitter = ''

# Keep the webdriver in full screen

# Load the web driver
driver = webdriver.Chrome()
driver.get('https://twitter.com/i/flow/login')

time.sleep(3)

# Login using credential
email_input = driver.find_element("xpath", '//div/input')
time.sleep(2)

email_input.click()
time.sleep(2)

email_input.send_keys(email)
button = driver.find_element("xpath", '//div/button[2]')
time.sleep(2)
button.click()

time.sleep(3)


# Logging and dealing with error of asking username while logging
try:
    username_input = driver.find_element("xpath", '//div/input')
    username_input.click()
    time.sleep(2)
    username_input.send_keys(user_name)
    button = driver.find_element("xpath", '//div[@role="button"]/div/span/span')
    time.sleep(2)
    button.click()
except NoSuchElementException:
    username_input = driver.find_element("xpath", '//div/input')
    username_input.click()
    button = driver.find_element("xpath", '//div[2]/div/div/div/button')
    button.click()

time.sleep(10)

password_input = driver.find_element("xpath", '//div/input[@autocomplete="current-password"]')
time.sleep(2)
password_input.click()
password_input.send_keys(password_twitter)
button = driver.find_element("xpath", '//div[2]/div/div[1]/div/div/button')
button.click()

time.sleep(10)

# Searching the name of the celeb
search = driver.find_element('xpath', '//div/div[2]/div/input')
time.sleep(3)
search.click()
search.send_keys(Celeb_name)
search.send_keys(Keys.ENTER)

time.sleep(3)

# Select the people tab and select the profile of the celeb
select_people = driver.find_element('xpath', "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[3]/a")
select_people.click()

time.sleep(3)

select_profile = driver.find_element('xpath', '//div/div[1]/div/div/button/div/div[2]/div[1]/div[1]/div/div[1]/a/div/div[1]/span/span[1]')
select_profile.click()

time.sleep(10)


# Load the data for the first set of loaded tweets
soup = BeautifulSoup(driver.page_source, 'lxml')
posting = soup.find_all("div", {"class": "css-146c3p1 r-8akbws r-krxsd3 r-dnmrzs r-1udh08x r-bcqeeo r-1ttztb7 r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41 r-bnwqim"})

# Scrolling and Saving to get new tweets
tweets = []
i = 0

# Appending the data while scrolling to feed new tweets
while True:
    for post in posting:
        tweets.append((i, post.text))
        i += 1
    time.sleep(5)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    posting = soup.find_all("div", {"class": "css-146c3p1 r-8akbws r-krxsd3 r-dnmrzs r-1udh08x r-bcqeeo r-1ttztb7 r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41 r-bnwqim"})
    tweets2 = list(set(tweets))

    i += 1
    if len(tweets2) > 25:
        break

# List to store DataFrame for each row
rows_to_append = []

# Create a DataFrame for each row and add it to the list
for i in tweets2:
    new_row = {'Index': i[0], 'Tweet': i[1]}
    row_df = pd.DataFrame([new_row], index=[0])  # Add index=[0]
    rows_to_append.append(row_df)

# Concatenate all DataFrames in the list
tweets_df = pd.concat(rows_to_append, ignore_index=True)

# Saving the data into an Excel file through pandas
tweets_df.to_excel('Tweets_scraping.xlsx', index=False)