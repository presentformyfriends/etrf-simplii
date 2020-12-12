#! python3

import os, pyautogui, sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options


def eTrf(cardNmbr, pword, amt):
    Options().set_preference("dom.popup_maximum", 0) # Does not allow popups, shows message with number of popup windows blocked
    driver = webdriver.Firefox(service_log_path=os.devnull) # Define driver
    driver.get('https://www.simplii.com/en/home.html') # Navigate to Simplii website
    
    # Click the "Sign On" button
    signOnButton = driver.find_element_by_css_selector('span.dropdown-label:nth-child(2)')
    signOnButton.click()

    # Login to Simplii website
    cardField = driver.find_element_by_xpath("//input[contains(@id, 'card-number')]")
    cardField.send_keys(cardNmbr) #LIVE KEY
    pwordField = driver.find_element_by_xpath("//input[contains(@id, 'password')]")
    pwordField.send_keys(pword) #LIVE KEY
    signOnButton = driver.find_element_by_css_selector('#button-1516987113640 > span:nth-child(1) > span:nth-child(1)')
    signOnButton.click()

    # Click on "Interac e-transfers" link on left side
    eTrfWait = EC.presence_of_element_located((By.LINK_TEXT, "Interac e-Transfers"))
    WebDriverWait(driver, 10).until(eTrfWait)
    eTrfLink = driver.find_element_by_link_text("Interac e-Transfers")
    eTrfLink.click()

    # Wait to load
    sendMoneyWait = EC.presence_of_element_located((By.LINK_TEXT, "Send Money"))
    WebDriverWait(driver, 10).until(sendMoneyWait)

    # Inputs amt variable in the "Amount:" field
    amount = driver.find_element_by_name("amount")
    amount.send_keys(amt)

    # Mitigate for ad popup
    try:
        adCloseBtn = driver.find_element_by_xpath('//button[@aria-label="Close Message"]')
        adCloseBtn.click()
    except:
        NoSuchElementException

    # Change "Kelly Kapoor" to whatever option you want for payee in the "Send Money To:" dropdown menu
    # Change "No Fee Chequing Account" to whatever account you want in the "Account:" dropdown menu
    menus = driver.find_elements_by_tag_name('SELECT')
    for menu in menus:
        if 'Kelly Kapoor' in menu.get_attribute('innerText'): # Change to recipient that you want
            menu.click()
            menu = Select(menu)
            menu.select_by_visible_text('Kelly Kapoor')
        elif 'No Fee Chequing Account' in menu.get_attribute('innerText'): # Change to whichever account you want
            menu.click()
            menu = Select(menu)
            for option in menu.options:
                optionText = option.get_attribute('text')
                if optionText.startswith('No Fee Chequing Account'):
                    option.click()
        else:
            pyautogui.alert('Could not access one of the dropdown menus')
            sys.exit()

    # Click first "Continue" button
    buttons = driver.find_elements_by_tag_name('BUTTON')
    for button in buttons:
        if button.get_attribute('innerText') == 'Continue':
            contBtnA = button
            contBtnA.submit()

    # Wait for url
    urlWait = EC.url_contains("/send/auto-deposit")
    WebDriverWait(driver, 10).until(urlWait)

    # Click second "Continue" button
    contBtnB = driver.find_element_by_xpath("//div[@class='action-bar row ember-view']//div[@class='ui-wrapper' and contains(., 'Continue')]")
    contBtnB.click()

    # Wait for "Send Money Verification" url (popup)
    verifyBoxWait = EC.url_contains("/send/verification")
    WebDriverWait(driver, 10).until(verifyBoxWait)

    # Alert dialog box for user to press confirm and then wait for screenshot
    confirm = pyautogui.confirm('I will wait for you to press the website\'s Confirm button\n\nThen, I will scroll down and take a screenshot for your records\n\nPress OK to continue or Cancel to abort')
    if confirm == 'OK':
        # Wait for "Send Money Confimation" url, which indicates that user has pressed the 'Confirm' button:
        confirmBoxWait = EC.url_contains("/send/confirmation")
        WebDriverWait(driver, 500).until(confirmBoxWait)
        
        # Scroll down to arrange page for screenshot
        successDiv = driver.find_element_by_xpath("//div[@class='successful ']")
        successDiv.location_once_scrolled_into_view

        # Take screenshot
        todayDateTime = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
        pyautogui.screenshot('C:\\Users\\PATH\\'+todayDateTime+'_.png') # Customize PATH

        # Alert dialog box to close
        pyautogui.alert('All done! Press OK to close the driver')

        # Close driver and exit
        driver.close()
        sys.exit()
    else:
        driver.close()
        sys.exit()
    

eTrf('cardNmbr', 'pword', 'amt') # Substitute your own values here, do not include '$' in dollarAmount
