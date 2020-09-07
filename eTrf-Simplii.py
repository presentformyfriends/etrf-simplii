#! python3

import os, pyautogui, sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


def eTrf(cardNmbr, pword, amt):
    browser = webdriver.Firefox(service_log_path=os.devnull) # Define browser
    browser.get('https://www.simplii.com/en/home.html') # Open Simplii webpage

    # Click the "Sign On" button
    signOnButton = browser.find_element_by_css_selector('span.dropdown-label:nth-child(2)')
    signOnButton.click()

    # Login to Simplii website
    cardField = browser.find_element_by_xpath("//input[contains(@id, 'card-number')]")
    cardField.send_keys(cardNmbr) #LIVE KEY
    pwordField = browser.find_element_by_xpath("//input[contains(@id, 'password')]")
    pwordField.send_keys(pword) #LIVE KEY
    signOnButton = browser.find_element_by_css_selector('#button-1516987113640 > span:nth-child(1) > span:nth-child(1)')
    signOnButton.click()

    # Click on "Interac e-transfers" link on left side
    eTrfWait = EC.presence_of_element_located((By.LINK_TEXT, "Interac e-Transfers"))
    WebDriverWait(browser, 10).until(eTrfWait)
    eTrfLink = browser.find_element_by_link_text("Interac e-Transfers")
    eTrfLink.click()

    # Wait to load
    sendMoneyWait = EC.presence_of_element_located((By.LINK_TEXT, "Send Money"))
    WebDriverWait(browser, 10).until(sendMoneyWait)

    # Inputs amt variable in the "Amount:" field
    amount = browser.find_element_by_name("amount")
    amount.send_keys(amt)

    # Change "Kelly Kapoor" to whatever option you want for payee in the "Send Money To:" dropdown menu
    # Change "No Fee Chequing Account" to whatever account you want in the "Account:" dropdown menu
    menus = browser.find_elements_by_tag_name('SELECT')
    for menu in menus:
        if 'Kelly Kapoor' in menu.get_attribute('innerText'): # Change to recipient that you want
            menu.click()
            menu = Select(menu)
            menu.select_by_index(2)
        elif 'No Fee Chequing Account' in menu.get_attribute('innerText'): # Change to whichever account you want
            menu.click()
            menu = Select(menu)
            menu.select_by_index(1)
        else:
            pyautogui.alert('Could not access one of the dropdown menus')
            sys.exit()

    # Click first "Continue" button
    buttons = browser.find_elements_by_tag_name('BUTTON')

    for button in buttons:
        if button.get_attribute('innerText') == 'Continue':
            contBtnA = button
            contBtnA.submit()

    # Wait for url
    urlWait = EC.url_contains("/send/auto-deposit")
    WebDriverWait(browser, 10).until(urlWait)

    # Click second "Continue" button
    contBtnB = browser.find_element_by_xpath("//div[@class='action-bar row ember-view']//div[@class='ui-wrapper' and contains(., 'Continue')]")
    contBtnB.click()

    ## At this point, you can review the payment, and then manually click the Confirm button. Or, if you want it truly automatic so that the Confirm button is
    ## pressed automatically, you can uncomment the lines below AT YOUR OWN RISK...

##    # Wait for popup
##    popupWait = EC.url_contains("/send/verification")
##    WebDriverWait(browser, 10).until(popupWait)
##
##    # Click "Confirm" button in popup window
##    confBtn = browser.find_element_by_xpath("//div[@class='action-bar row ember-view']//div[@class='ui-wrapper' and contains(., 'Cancel')]") # Change to Confirm
##    confBtn.click()
##
##    # Exit the browser
##    browser.quit()
    

eTrf('cardNmbr', 'pword', 'amt') # Substitute your own values here, do not include '$' in dollarAmount
