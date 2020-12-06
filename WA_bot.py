import traceback
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

import os
import platform
from tkinter import Tk
import time
from random import seed, random

try:
    import autoit
except ModuleNotFoundError:
    pass

if platform.system() == 'Darwin':
    # MACOS Path
    chrome_default_path = os.getcwd() + '/driver/chromedriver'
else:
    # Windows Path
    chrome_default_path = os.getcwd() + '/driver/chromedriver.exe'


def whatsapp_login():
    global wait, browser, search_button
    Link = "https://web.whatsapp.com/"
    chrome_options = Options()
    chrome_options.add_argument('--user-data-dir=./User_Data')
    chrome_options.add_argument("--log-level=3")
    browser = webdriver.Chrome(
        executable_path=chrome_default_path, options=chrome_options)
    wait = WebDriverWait(browser, 5)
    browser.get(Link)
    browser.maximize_window()

    input("\nAfter the page loads properly, press [ENTER]\n")
    input(
        "Now, try to copy the message until the 'WA preview' for the links loads properly, then delete it again\nFinally press [ENTER]\n")
	
    # Defining the search button
    button_x_arg = "//button[.//span[@data-icon='search']]"
    search_button = wait.until(
        EC.presence_of_element_located((By.XPATH, button_x_arg)))


def import_contacts():
    contact = []
    fp = open("contacts.txt", "r")

    while True:
        line = fp.readline()
        con = ' '.join(line.split())
        if con:
            contact.append('\"' + con + '\"')
        if not line:
            break

    fp.close()
    return contact


def import_message():
    print("Here's your message (emojis might not be printed in the console)\n")
    message = open("message.txt", "r", encoding="utf8")
    message = message.read()
    print(message + "\n\n")
    # copy message to clipboard
    r = Tk()
    r.withdraw()
    r.clipboard_append(message)
    r.update()


def attachment_verification():
    isAttach = input("Would you like to send attachment(yes/no):")

    if isAttach == "yes":
        input(
            "\n\nTo send attachment: Put the image on `.\\attachment`, then press [ENTER]")
        image_name = input(
            "Write the name of the file (including the file format): ")
        image_path = os.getcwd() + "\\attachment\\" + image_name
        print(image_path)

        while not os.path.exists(image_path) and image_name != '':
            image_name = input(
                "Wrong file name, Write the name of the file (including the file format): ")
            image_path = os.getcwd() + "\\attachment\\" + image_name
            print(image_path)
    else:
        image_path = None
    return isAttach, image_path


def send_message(target, image_path):
    try:
        search_button.click()
        actions = ActionChains(browser)
        actions.send_keys(target[1:-1])
        actions.perform()

        name_x_arg = '//span[@title=' + target + ']'
        try:
            group_title = wait.until(
                EC.presence_of_element_located((By.XPATH, name_x_arg)))
            group_title.click()
        except:
            print(target + " tidak ada di WA")
            error_file.write(target[1:-1] + "\n")
            search_button.click()
            return

        try:
            browser.find_element_by_xpath(
                "//*[contains(text(),'t send a message to blocked contact')]")
            search_button.click()
            error_file.write(target[1:-1] + "\n")
            print(target + " di block")
            return
        except:
            pass

        input_box = browser.find_element_by_xpath(
            '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')

        ActionChains(browser).key_down(Keys.CONTROL).key_down('v').key_up(Keys.CONTROL).key_up(
            'v').key_up(Keys.BACKSPACE).perform()

        input_box.send_keys(Keys.ENTER)
        print("Message sent successfully to " + target)

        if (isAttach == "yes"):
            try:
                send_attachment(image_path)
            except:
                print('Attachment not sent.')

    except:
        return


def send_attachment(path):
    # Attachment Drop Down Menu
    try:
        clipButton = browser.find_element_by_xpath(
            '//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/div/span')
        clipButton.click()
    except:
        pass

    # Clicking the Media button
    try:
        mediaButton = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/span/div/div/ul/li[1]/button')))
        mediaButton.click()
    except:
        pass
    time.sleep(2)

    # Sending paths to pop-up windows
    autoit.send(path)
    autoit.send("{ENTER}")

    # Clicking the send button
    try:
        x_arg_imgsend = '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div'
        whatsapp_send_button = wait.until(
            EC.presence_of_element_located((By.XPATH, x_arg_imgsend)))
        whatsapp_send_button.click()
    except:
        traceback.print_exc()


def sender(contact, isAttach, image_path):
	global error_file
	
    # Seed to create random number to evade Whatsapp Bot detection
    seed(1)

    # Initiating error file
    error_file = open('contact_error.txt', 'w')
    error_file.write(
        "Here are some contacts that give errors in this session\n")
    error_file.close()
    error_file = open('contact_error.txt', 'a', buffering=1)
    
    # Iterating through contacts list
    for target in contact:
        try:
            send_message(target, image_path)
        except:
            pass
        time.sleep(2 + random()*10/5)
    
    error_file.close()


if __name__ == "__main__":
    # Initiating contacts, attachment, and message
    list_of_contact = import_contacts()
    isAttach, image_path = attachment_verification()
    import_message()

    # Login and Scan
    whatsapp_login()

    # Sending the messages
    sender(list_of_contact, isAttach, image_path)

    print("Done!\nKontak kontak tanpa WA disimpan pada file 'contact_error.txt'")
