import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define the path to the Chrome driver executable
chrome_driver_path = r"C:\Users\Laus\Documents\chromedriver-win64\chromedriver.exe"

# Define the path to the Chrome user data directory
chrome_user_data_path = r"C:\Users\Laus\AppData\Local\Google\Chrome\User Data\Profile 2"

# Create a new Chrome browser instance with the specified user data directory
service = Service(executable_path=chrome_driver_path)
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=" + chrome_user_data_path)
driver = webdriver.Chrome(service=service, options=options)

# Navigate to the Google Maps page for Vilamoura, Portugal
driver.get("https://www.google.com/search?q=vilamore")

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

# Wait for the full review text to load
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.review-full-text')))

# Get the full review text for each review and print it to a text file
reviews = driver.find_elements(By.CSS_SELECTOR, '.review-full-text')
with open("reviews.txt", "w", encoding="utf8") as f:
    for review in reviews:
        text = review.get_attribute("innerText")
        f.write(text + "\n\n")

# Close the browser
driver.quit()