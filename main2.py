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
    time.sleep(5)

    # Find all the "Mais" buttons and click them
    more_buttons = driver.find_elements(By.CSS_SELECTOR, '.review-more-link')
    for button in more_buttons:
        try:
            # Wait until the button is clickable
            WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.review-more-link')))
            button.click()
        except:
            # If the button is not clickable, try to click it using JavaScript
            driver.execute_script("arguments[0].click();", button)

    # Get the reviews
    reviews = driver.find_elements(By.CSS_SELECTOR, '.jxjCjc')
    with open(f"inputs/{company}_reviews.txt", "w", encoding="utf8") as f:
        for review in reviews:
            full_text = None
            text = None
            try:
                
                # Wait for the full review text to load
                #wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.review-full-text')))
                
                # Get the full review text
                full_text = review.get_attribute("innerText")
                f.write(full_text + "\n\n")
                
            except:
                # If the full review text does not exist, get the review text as is
                text = review.get_attribute("innerText")
                if text:
                    f.write(text + "\n\n")
            
            # Write the separator to the file
            f.write('---\n')
            
# Close the browser
driver.quit()