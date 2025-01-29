from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import csv

def scrape(URL):
    # Set Chrome options to run headless (optional)
    chrome_options = Options()
    # chrome_options.add_argument("--headless")

    # Path to your ChromeDriver
    service = Service('/Users/mollytaylor/Downloads/chromedriver-mac-x64/chromedriver')  # Adjust the path

    # Initialize the WebDriver with the service
    driver = None
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Open the website
        driver.get(URL)

        # Wait for the page to load completely
        time.sleep(1)  # Adjust sleep if necessary for the challenge to pass

        # Once the page is loaded, get the page source
        html = driver.page_source

        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Extract all text from the page
        all_text = soup.get_text()

        # Print all the text found on the page
        print(all_text)

        # Extract the title and handle potential issues with missing title
        title_tag = soup.title
        title = title_tag.string.split("|")[0].strip() if title_tag else "No Title"
        print("Title: ", title)

        # Now you can scrape the content
        bio_div = soup.find('div', class_='col-sm-8')

        bio_text = "Bio not found"
        if bio_div:
            bio_paragraph = bio_div.find('p')
            if bio_paragraph:
                bio_text = bio_paragraph.get_text()
                # print("Bio text: ", bio_text)
            else:
                print("Bio paragraph not found")
        else:
            print("Bio div not found")

        return title, bio_text
    except Exception as e:
        print(f"Error during scraping {URL}: {e}")
        return None, None  # Return None in case of errors
    finally:
        # Ensure that the browser is closed properly
        if driver:
            driver.quit()

# NEED TO RE-SCRAPE 921
# Example loop to scrape narrators from 1 to 10
for i in range(1000, 1050):
    url = f'https://ddr.densho.org/narrators/{i}/'
    title, bio = scrape(url)

    if title and bio:
        # Write the data only if scraping was successful
        with open('bios.csv', 'a', newline='') as file:
            if bio != "Bio not found":
                writer = csv.writer(file, delimiter=',')
                writer.writerow([i,title,bio])
        print(f"narrator with id {i} scraped")
    else:
        print(f"Failed to scrape narrator with id {i}")
