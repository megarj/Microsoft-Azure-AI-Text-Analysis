import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define the path to the Chrome driver
chrome_driver_path = r"C:\Users\Laus\Documents\chromedriver-win64\chromedriver.exe"

# Define the path to the Chrome user data directory
chrome_user_data_path = r"C:\Users\Laus\AppData\Local\Google\Chrome\User Data\Profile 2"

# Create a new Chrome browser instance with the specified user data directory
service = Service(executable_path=chrome_driver_path)
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=" + chrome_user_data_path)
driver = webdriver.Chrome(service=service, options=options)

# Get a list of company names from the user
companies = input("Enter a list of companies to search, separated by commas: ").split(',')

# Iterate through the list of companies
for company in companies:
    # Remove any leading or trailing whitespace from the company name
    company = company.strip()

    # Navigate to the Google Search page
    driver.get(f"https://www.google.com/search?q={company}")

    # Wait for the page to load
    time.sleep(5)

    # Click the "Ver todos os comentários do Google" button
    button = driver.find_element(By.CSS_SELECTOR, 'a[data-async-trigger="reviewDialog"]')
    button.click()

    # Wait for the reviews to load
    wait = WebDriverWait(driver, 10)

    # Find all the "Mais" buttons and click them
    more_buttons = driver.find_elements(By.CSS_SELECTOR, '.review-more-link')
    for button in more_buttons:
        button.click()

    # Wait for the review items to load
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.jxjCjc')))

    # Get the full review text for each review and print it to a text file
    reviews = driver.find_elements(By.CSS_SELECTOR, '.jxjCjc')
    with open(f"{company}_reviews.txt", "w", encoding="utf8") as f:
        for review in reviews:
            full_text = None
            text = None
            try:
                # Get the full review element
                review_element = review.find_element(By.CSS_SELECTOR, '.jxjCjc')
                # Try to get the full review text by clicking the "Mais" button if it exists
                more_button = review_element.find_element(By.CSS_SELECTOR, '.review-more-link')
                more_button.click()
                # Wait for the full review text to load
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.review-full-text')))
                full_text = driver.find_element(By.CSS_SELECTOR, '.review-full-text').get_attribute("innerText")
                f.write(full_text + "\n\n")
                # Wait for the next review to load
                wait.until(EC.staleness_of(more_button))
            except:
                # If the "Mais" button does not exist, get the review text as is
                text = review.get_attribute("innerText")
                if text:
                    f.write(text + "\n\n")

# Close the browser
driver.quit()