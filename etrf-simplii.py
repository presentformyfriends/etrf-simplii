#! python3

import os
import pyautogui
import time
import sys
import undetected_chromedriver as uc
from pathlib import Path
from datetime import datetime
from decimal import Decimal
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options


def login(driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//input[contains(@id, 'card-number')]")
        )
    ).send_keys(
        CARD_NUMBER
    )  # Environment variable
    driver.find_element(
        "xpath", "//input[contains(@id, 'password')]"
    ).send_keys(
        PASSWORD
    )  # Environment variable
    driver.find_element("xpath", "//button//span[text()='Sign on']").click()


def sendCode(driver):
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[text()='Send code']")
            )
        ).click()
        # Prompt user for code
        passcode = pyautogui.prompt(
            "Simplii is asking for a confirmation code\n\nPlease enter it now"
        )
        if passcode != "":
            code_field = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.NAME, "otvc"))
            )  # WebDriverWait for something else like URL so as not to waste time!

            # Enter code and submit
            code_field = driver.find_element("name", "otvc")
            code_field.send_keys(passcode)

            # Wait for Next button and click it
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//ui-button/div[text()=\"Next\"]"))).click()
        else:
            print("Passcode not found")
            input("Press ENTER to continue...")
    except:
        NoSuchElementException
        print("Unable to click 'Send Code' button")


def remindLater(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[@class='ui-wrapper'][text()='Remind me later']",
                )
            )
        ).click()
    except:
        NoSuchElementException
        print("No Remind Me Later screen")


def popupClose(driver):
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, '//button[@aria-label="Close Message"]')
            )
        ).click()
        time.sleep(
            1
        )  # 1 second sleep to avoid ad interfering with clicking other elements
    except:
        NoSuchElementException
        print("No pop-up")


def transfer(amount):
    # Set Undetected Chromedriver Options
    options = uc.ChromeOptions()
    options.add_argument(
        "--no-first-run --no-service-autorun --password-store=basic"
    )  # Disable password popups
    options.add_experimental_option(
        "safebrowsing", {"enabled": True})  # Block popups
    options.add_argument("--disable-extensions")  # Disable extensions
    options.add_argument("--incognito")
    driver = uc.Chrome(options=options)  # Define Undetected Chromedriver

    # Load Simplii website
    driver.get("https://www.simplii.com/en/home.html")

    # Maximize browser window
    driver.maximize_window()

    # Click the "Sign On" button
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[@id="sign-on"]'))
    ).click()

    # Login to Simplii website
    login(driver)

    # Mitigate for "Remind Me Later" screen
    remindLater(driver)

    # Mitigate for second login
    try:
        login(driver)
    except:
        NoSuchElementException
        print("No second login")

    # Mitigate for "Verify your identity with code" screen
    sendCode(driver)

    # Mitigate AGAIN for case of Mortgage Ad page, click on 'Remind me later'
    remindLater(driver)

    # Wait until url changes
    WebDriverWait(driver, 10).until(EC.url_contains("accounts"))

    # Mitigate for pop-ups FIND A WAY TO PREVENT ANY AND ALL POP-UPS FROM OPENING EVER
    popupClose(driver)

    # Click on "Interac e-transfers" link on left side
    eTrfWait = EC.presence_of_element_located(
        (By.LINK_TEXT, "Interac e-Transfers")
    )
    WebDriverWait(driver, 5).until(eTrfWait)
    eTrfLink = driver.find_element(By.LINK_TEXT, "Interac e-Transfers")
    eTrfLink.click()

    # Wait for page to load
    sendMoneyWait = EC.presence_of_element_located(
        (By.LINK_TEXT, "Send Money")
    )
    WebDriverWait(driver, 5).until(sendMoneyWait)

    # Mitigate for ad popup
    popupClose(driver)

    # Enter amount in the "Amount:" field
    amount_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='amount']"))
    )
    amount_field.send_keys(str(amount))

    # Choose option from "Send Money To:" dropdown menu (change "PAYEE" to the name of your payee)
    # Choose account type option from "Account:" dropdown menu (change "ACCOUNT_TYPE" to your account type i.e. chequing)
    menus = driver.find_elements(By.TAG_NAME, "SELECT")
    for menu in menus:
        if "PAYEE" in menu.get_attribute("innerText"):
            menu.click()
            menu = Select(menu)
            menu.select_by_visible_text("PAYEE")
        elif "ACCOUNT_TYPE" in menu.get_attribute("innerText"):
            menu.click()
            menu = Select(menu)
            # You could also do select_by_index(1) but this approach is more stable
            for option in menu.options:
                optionText = option.get_attribute("text")
                if optionText.startswith("ACCOUNT_TYPE"):
                    option.click()
        else:
            pyautogui.alert("Could not access one of the dropdown menus")
            input("Press Enter to close...")
            driver.quit()

    # Click first "Continue" button
    buttons = driver.find_elements(By.TAG_NAME, "BUTTON")
    for button in buttons:
        if button.get_attribute("innerText") == "Continue":
            contBtnA = button
            contBtnA.submit()

    # Wait for url
    urlWait = EC.url_contains("/send/auto-deposit")
    WebDriverWait(driver, 10).until(urlWait)

    # Click second "Continue" button (hidden, took forever to find the path!)
    contBtnB = driver.find_element(
        "xpath",
        "//div[@class='action-bar row ember-view']//div[@class='ui-wrapper' and contains(., 'Continue')]",
    )
    contBtnB.click()

    # Wait for "Send Money Verification" url (popup)
    verifyBoxWait = EC.url_contains("/send/verification")
    WebDriverWait(driver, 10).until(verifyBoxWait)

    # Alert dialog box for user to press confirm and then wait for screenshot
    confirm = pyautogui.confirm(
        "I will wait for you to press the website's 'Send Money' button\n\nThen, I will scroll down and take a screenshot for your records\n\nPress OK to continue or Cancel to abort")
    if confirm == "OK":
        # Wait for "Send Money Confimation" url, which indicates that user has pressed the 'Confirm' button:
        confirmBoxWait = EC.url_contains(
            "/send/confirmation"
        )  # https://online.simplii.com/ebm-resources/public/client/web/index.html#/etransfers/send/confirmation
        WebDriverWait(driver, 500).until(confirmBoxWait)

        # Mitigate for pop-ups
        popupClose(driver)

        # Scroll down to arrange page for screenshot
        successDiv = driver.find_element(
            "xpath", "//div[text()='Your transfer has been sent']"
        )
        successDiv.location_once_scrolled_into_view
        time.sleep(
            5
        )  # 5 seconds sleep to ensure proper scrolling

        # Take screenshot and save it with today's date (replace "/SCREENSHOT/PATH" with your own path)
        todayDateTime = datetime.today().strftime("%Y-%m-%d_%H-%M-%S")
        pyautogui.screenshot(
            "/SCREENSHOT/PATH/" + todayDateTime + "_paid.png"
        )

        # Alert dialog box to close
        pyautogui.alert("Screenshot saved! Press OK to close the driver")

        # Close driver and exit
        driver.quit()
    else:
        driver.quit()


# MAIN #
raw_amount = 150.00  # Replace with your own amount
amount = Decimal(raw_amount)

print("""
             /$$                /$$$$$$                /$$                         /$$ /$$ /$$
            | $$               /$$__  $$              |__/                        | $$|__/|__/
  /$$$$$$  /$$$$$$    /$$$$$$ | $$  \__/      /$$$$$$$ /$$ /$$$$$$/$$$$   /$$$$$$ | $$ /$$ /$$
 /$$__  $$|_  $$_/   /$$__  $$| $$$$ /$$$$$$ /$$_____/| $$| $$_  $$_  $$ /$$__  $$| $$| $$| $$
| $$$$$$$$  | $$    | $$  \__/| $$_/|______/|  $$$$$$ | $$| $$ \ $$ \ $$| $$  \ $$| $$| $$| $$
| $$_____/  | $$ /$$| $$      | $$           \____  $$| $$| $$ | $$ | $$| $$  | $$| $$| $$| $$
|  $$$$$$$  |  $$$$/| $$      | $$           /$$$$$$$/| $$| $$ | $$ | $$| $$$$$$$/| $$| $$| $$
 \_______/   \___/  |__/      |__/          |_______/ |__/|__/ |__/ |__/| $$____/ |__/|__/|__/
                                                                        | $$                  
                                                                        | $$                  
                                                                        |__/                        
""")

transfer(amount)
