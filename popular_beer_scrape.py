import os
from os.path import join, dirname
from dotenv import load_dotenv
from gazpacho import Soup
import time
import csv
from tqdm import tqdm
from selenium.webdriver import Firefox
from selenium.common import exceptions
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login_dialog(css_selector, message=""):
    """ get the login dialog elements by css and send message once they are visible """
    try:
        elem = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector))
        )
        if message:
            elem.clear()
            elem.send_keys(message)
        else:
            elem.click()

    except exceptions.NoSuchElementException:
        print(f"Element not found {css_selector}")
    except exceptions.TimeoutException:
        print(f"Timeout waiting for {css_selector}")


# read the environment file to get my username and password
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)
username = os.getenv("BA_USERNAME")
password = os.getenv("BA_PASSWORD")
if not username or not password:
    print(f"username or password not provided in {dotenv_path}")
    exit(1)
print(username)
print(password)

# login to site
url = "https://www.beeradvocate.com"
popular_url = f"{url}/beer/popular"
options = Options()
options.headless = False
browser = Firefox(options=options)
browser.get(popular_url)
# open the login dialog
browser.find_element_by_class_name("loginText").click()
# enter username
username_css = "#pageLogin > dl:nth-child(3) > dd:nth-child(2) > input:nth-child(1)"
login_dialog(username_css, username)
# enter password
password_css = "#ctrl_pageLogin_registered_Disabler > input:nth-child(1)"
login_dialog(password_css, password)
# click login button
button_css = "dl.ctrlUnit:nth-child(5) > dd:nth-child(2) > input:nth-child(1)"
login_dialog(button_css)

# now check for my username to make sure I'm logged in
html = browser.page_source
soup = Soup(html)
my_user_name = soup.find("strong", {"class": "accountUsername"})
if not my_user_name:
    print("Not logged in!")
    exit()

# open a csv file for writing
with open("popular_beer_ratings.csv", "a") as f:
    csv_writer = csv.writer(f)
    # write the header row
    csv_writer.writerow(["brewery", "item", "user", "review"])
    # get each of the popular beers
    rows = soup.find("tr", mode="all")
    for row in tqdm(rows):
        beer = row.find("a", mode="first")
        if beer:
            brewer = row.find("span", {"class": "muted"})
            beer_url = f"{url}{beer.attrs['href']}/?sort=top"
            browser.get(beer_url)
            # get the first few pages
            for i in range(2):
                soup = Soup(browser.page_source)
                users = soup.find(
                    "div", {"id": "rating_fullview_content_2"}, mode="all"
                )
                for user in users:
                    name = user.find("a", {"class": "username"}).text
                    rating = user.find("span", {"class": "BAscore_norm"}).text
                    csv_writer.writerow([brewer.text, beer.text, name, rating])
                # flush the file and sleep for a couple of seconds
                f.flush()
                time.sleep(3)
                # get next set of reviews by clicking next
                login_dialog(
                    "#ba-content > div:nth-child(12) > span:nth-child(1) > a:nth-child(5)"
                )
