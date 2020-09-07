from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException


import argparse as ap

import time
import datetime
from random import randint
import requests

# variables
username = 'jr6339'
password = 'ofed1663'
logfile = 'log.txt'
bot_token = '1305660558:AAFl_Eh_v_SY9fW6SbX49mRHDABjhqwY8hs'
bot_chatID = '266785130'
driver_path = r'C:/Users/rengwu/Desktop/Projects/Autoclockin/chromedriver_win32/chromedriver.exe'

# globals
delay = 5
log = True


def telegram_bot_sendtext(bot_message):
    send_text = 'https://api.telegram.org/bot' + bot_token + \
        '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    debug_print('Sending Telegram Text:' + bot_message)
    response = requests.get(send_text)
    return response.json()


def debug_print(string):
    prefix = "Clocker> ({}) ".format(str(datetime.datetime.now()))
    print(prefix + string)
    log = True
    if log:
        file = open(logfile, 'a')
        file.write("{}\n".format(prefix + string))
        file.close()


def clock_in(browser, clockInValue):
    debug_print('clocking in..')
    loginSuccess = login(browser)
    if (not loginSuccess):
        debug_print('login failed..')
        return False

    elif (loginSuccess):
        # wait for clockin button & click
        try:
            myElem = WebDriverWait(browser, delay).until(
                EC.presence_of_element_located((By.XPATH, "//input[@id='btnClockIn']")))
            time.sleep(1)
            myElem.click()
        except TimeoutException:
            debug_print("ClockinButton took too much time, terminating!")
            return False

        # wait for time selection input
        try:
            myElem = WebDriverWait(browser, delay).until(
                EC.presence_of_element_located((By.XPATH, "//select[@id='DDLShift']")))
            time.sleep(1)
            select = Select(browser.find_element_by_xpath(
                "//select[@id='DDLShift']"))
            select.select_by_visible_text(clockInValue)
            debug_print("selected by visible text: {}".format(clockInValue))
        except TimeoutException:
            debug_print("confirmation button took too much time, terminating!")
            return False

        # wait for confirmation dialog & click on ok
        try:
            myElem = WebDriverWait(browser, delay).until(
                EC.presence_of_element_located((By.XPATH, "//button[@onclick='TriggerClockIn();return false;']")))
            time.sleep(1)
            # myElem.click()
            debug_print("clock in button click!")
        except TimeoutException:
            debug_print("confirmation button took too much time, terminating!")
            return False

        # wait for alert and accept it
        try:
            debug_print("waiting for alert to close it..")
            myElem = WebDriverWait(browser, 20).until(
                EC.alert_is_present())
            time.sleep(1)
            alert = browser.switch_to.alert
            alert.accept()
        except TimeoutException:
            print("WaitAlert took too much time, skipping it!")
        time.sleep(10)

    browser.close()
    debug_print('browser closed successfully')
    return True


def clock_out(browser):
    debug_print('clocking out..')
    loginSuccess = login(browser)
    if (not loginSuccess):
        debug_print('login failed..')
        return False

    elif (loginSuccess):
        # wait for clockout button & click
        try:
            myElem = WebDriverWait(browser, delay).until(
                EC.presence_of_element_located((By.XPATH, "//input[@id='btnClockOut']")))
            time.sleep(1)
            myElem.click()
        except TimeoutException:
            debug_print("ClockoutButton took too much time, terminating!")
            return False

        # wait for confirmation dialog & click on ok
        try:
            myElem = WebDriverWait(browser, delay).until(
                EC.presence_of_element_located((By.XPATH, "//button[@onclick='TriggerClockOut();return false;']")))
            time.sleep(1)
            myElem.click()
            debug_print("clock out button click!")
        except TimeoutException:
            debug_print("confirmation button took too much time, terminating!")
            return False
        # wait for alert and accept it
        try:
            debug_print("waiting for alert to close it..")
            myElem = WebDriverWait(browser, 20).until(
                EC.alert_is_present())
            time.sleep(1)
            alert = browser.switch_to.alert
            alert.accept()
        except TimeoutException:
            debug_print("WaitAlert took too much time, skipping it!")
        time.sleep(10)

    browser.close()
    debug_print('browser closed successfully')
    return True


def login(browser):
    loginError = False
    errorMessage = ''
    debug_print('opening browser and logging in..')
    browser.get("https://apps3.teledirect.com.my/Portal/StaffLogin")

    # wait for input fields
    try:
        myElem = WebDriverWait(browser, delay).until(
            EC.presence_of_element_located((By.ID, 'mainContentPlaceholder_tbxUsername')))
        time.sleep(1)
    except TimeoutException:
        debug_print("Input Fields took too much time, terminating!")
        return False

    debug_print('inputting credentials')
    # input text fields
    for i in range(len(username)):
        username_input = browser.find_element_by_xpath(
            "//input[@id='mainContentPlaceholder_tbxUsername']")
        username_input.send_keys(username[i])
        time.sleep(0.02)

    for i in range(len(password)):
        password_input = browser.find_element_by_xpath(
            "//input[@id='mainContentPlaceholder_tbxPassword']")
        password_input.send_keys(password[i])
        time.sleep(0.02)

    login_btn = browser.find_element_by_xpath(
        "//input[@id='mainContentPlaceholder_btnLogin']")
    login_btn.click()

    debug_print('waiting for login & alert modal..')
    # wait for alert & accept it
    try:
        myElem = WebDriverWait(browser, 20).until(
            EC.alert_is_present())
        time.sleep(1)
        alert = browser.switch_to.alert
        alert.accept()
    except TimeoutException:
        debug_print("WaitAlert took too much time, skipping it!")
        loginError = True
        errorMessage = 'closemodal button took too much time, skipping it!'

    # close modal
    try:
        elem = WebDriverWait(browser, delay).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='closeModal']")))
        closeBtn = browser.find_element_by_xpath(
            "//div[@class='closeModal']")
        closeBtn.click()
        debug_print('modal closed')
    except TimeoutException:
        debug_print("closemodal button took too much time, skipping it!")
        loginError = True
        errorMessage = 'closemodal button took too much time, skipping it!'

    if loginError:
        telegram_bot_sendtext('Login Error!', errorMessage)

    debug_print('login success!')
    return True


if __name__ == "__main__":
    parser = ap.ArgumentParser()
    parser.add_argument("clock", help="'in' or 'out'", type=str)
    parser.add_argument(
        "timeString", help="clockinvalue: visible text from dropdown selector", type=str)
    parser.add_argument("log", help="'log' or 'nah'", type=str)

    arguments = parser.parse_args()
    procedure = arguments.clock
    clockInValue = arguments.timeString
    logging = arguments.log

    debug_print('Clocking in with parameters:')
    debug_print(' - procedure : \t' + procedure)
    debug_print(' - clockInValue : \t' + clockInValue)
    debug_print(' - log : \t' + logging)

    if (logging == 'log'):
        log = True
    else:
        log = False

    browser = webdriver.Chrome(driver_path)
    browser.set_page_load_timeout(30)

    if procedure == 'in':
        clockedIn = clock_in(browser, clockInValue)
        if (not clockedIn):
            telegram_bot_sendtext('Script failure, not clocked in!')
            telegram_bot_sendtext('Check the script log.txt for more details')
    elif procedure == 'out':
        clockedOut = clock_out(browser)
        if (not clockedOut):
            telegram_bot_sendtext('Script failure, not clocked out!')
            telegram_bot_sendtext('Check the script log.txt for more details')
    else:
        debug_print('what..? clock in or out?')
