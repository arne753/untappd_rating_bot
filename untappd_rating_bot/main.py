import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

PATH = r"C:\Program Files\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://untappd.com/search?q=")
driver.implicitly_wait(15)
driver.maximize_window()
beer_name = input("enter the name of the beer you want to get the score from: ")


def login():
    with open(
        r"C:\Users\arneb\vscode\python\intermediate_python\untappd_bot\data.json", "r"
    ) as file:
        data = json.load(file)
        email = data.get("username")
        password = data.get("password")

    email_field = driver.find_element(By.ID, "username")
    email_field.send_keys(email)

    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password)

    print("solve the captcha...")
    time.sleep(1)

    # the captcha element is not embedded in the html, its a frame, we need to switch to it
    iframe_elements = driver.find_elements(By.TAG_NAME, "iframe")
    for element in iframe_elements:
        if element.get_attribute("title") == "reCAPTCHA":
            driver.switch_to.frame(element)
            print("switched_frame")
            break

    status = driver.find_element(By.ID, "recaptcha-accessible-status")
    print("element found")

    # look if the captcha is completed
    while True:
        time.sleep(0.5)
        try:
            status = driver.find_element(By.ID, "recaptcha-anchor")
            status_bool = status.get_attribute("aria-checked")
            if status_bool == "true":
                break
        except:
            continue

    # switch back to the default frame
    driver.switch_to.default_content()
    # click the login button
    submit_button = driver.find_element(
        By.CSS_SELECTOR, 'span[class="button yellow submit-btn"]'
    )
    submit_button.click()


def accept_cookies():
    accept = driver.find_element(By.CSS_SELECTOR, 'p[class="fc-button-label"]')
    accept.click()


def click_login_button():
    login_button = driver.find_element(
        By.CSS_SELECTOR, 'a[class="sign_in track-click"]'
    )
    login_button.click()


def input_beer_name(beer_name):
    time.sleep(0.3)
    input_field = driver.find_element(By.CSS_SELECTOR, 'input[id="search-term"]')
    input_field.click()

    time.sleep(0.1)
    input_field.send_keys(beer_name)

    submit_button = driver.find_element(
        By.CSS_SELECTOR, 'input[aria-label="search button"]'
    )
    submit_button.click()


def get_rating(beer_name):
    try:
        beer_rating = driver.find_element(By.CSS_SELECTOR, 'div[class="caps"]')
    except:
        print("no beers found")

    score = float(beer_rating.get_attribute("data-rating"))
    print(f"rating of {beer_name} = {score}")


def main():
    accept_cookies()
    click_login_button()
    login()
    input_beer_name(beer_name)
    get_rating(beer_name)


main()
