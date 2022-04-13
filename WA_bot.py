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
from tkinter import filedialog
import time
from random import seed, random
import argparse

try:
    import autoit
except ModuleNotFoundError:
    pass


def whatsapp_login(original_msg):
    global wait, browser, search_button, button_frame
    bot_path = os.getcwd()
    user_data_path = os.path.join(bot_path, 'User_Data')
    if platform.system() == 'Darwin':
        # MACOS Path
        chrome_default_path = os.path.join(bot_path, 'driver/chromedriver')
    else:
        # Windows Path
        chrome_default_path = os.path.join(bot_path, 'driver/chromedriver.exe')

    Link = "https://web.whatsapp.com/"
    chrome_options = Options()
    chrome_options.add_argument('--user-data-dir=%s' % user_data_path)
    chrome_options.add_argument("--log-level=3")
    browser = webdriver.Chrome(
        executable_path=chrome_default_path, options=chrome_options)
    wait = WebDriverWait(browser, 2)
    browser.get(Link)
    browser.maximize_window()

    input("\nAfter the page loads properly, press [ENTER]\n")
    input(
        "Now, try to copy the message until the 'WA preview' for the links loads properly, then delete it again\nFinally press [ENTER]\n")

    # Defining the search button
    button_x_arg = "//button[.//span[@data-icon='search']]"
    search_button = wait.until(
        EC.presence_of_element_located((By.XPATH, button_x_arg)))

    frame_x_arg = "//span[@data-icon='back']/.."
    button_frame = wait.until(
        EC.presence_of_element_located((By.XPATH, frame_x_arg)))


def isSearchActive():
    search_active = button_frame.value_of_css_property("opacity")
    return(int(search_active))


def contact_parser():
    # Parsing the argument and checks if the contact file exist
    parser = argparse.ArgumentParser(description='Add contact-file argument')
    parser.add_argument('contact_file', type=str, nargs=1)
    try:
        args = parser.parse_args()
        contact_file_name = args.contact_file[0]
        contact_file_path = os.path.join(
            os.getcwd(), "contacts", contact_file_name+".txt")
    except:
        print("Select contact file")
        root = Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        contact_file_path = file_path

    return contact_file_path


def import_contacts():
    contact_file_path = contact_parser()
    contact = []
    try:
        fp = open(contact_file_path, "r")
    except Exception as e:
        raise e

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
    input("Copy the message that you want to send\n Then press [ENTER]")
    # copy message to clipboard
    try:
        r = Tk()
        r.withdraw()
        copied_text = r.clipboard_get()
        return copied_text
    except:
        return None


def update_clipboard(original_msg):
    r = Tk()
    r.withdraw()
    r.clipboard_append(original_msg)
    r.update()


def attachment_verification():
    isAttach = input("Would you like to send attachment(yes/no):")

    if isAttach == "yes":
        print("Select attachment file")
        root = Tk()
        root.withdraw()
        image_path = filedialog.askopenfilename()
        image_path = image_path.replace('/', '\\')
    else:
        image_path = None
    return isAttach, image_path


def send_message(target, image_path):
    if isSearchActive():
        print("Search is active, unpressing the button")
        search_button.click()

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

        try:
            browser.find_element_by_xpath(
                "//*[contains(text(),'Tidak dapat mengirim pesan ke kontak terblokir')]")
            search_button.click()
            error_file.write(target[1:-1] + "\n")
            print(target + " di block")
            return
        except:
            pass
        time.sleep(1)

        input_box = browser.find_element_by_xpath(
            '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]')

        ActionChains(browser).key_down(Keys.CONTROL).key_down('v').perform()
        ActionChains(browser).key_up(Keys.CONTROL).key_up('v').perform()

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
            '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div/span')

        clipButton.click()
    except:
        pass
    time.sleep(.5)

    # Clicking the Media button
    try:
        mediaButton = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div[1]/div/ul/li[1]/button/span')))
        mediaButton.click()
    except:
        pass
    time.sleep(1)

    # Sending paths to pop-up windows
    autoit.send(path)
    autoit.send("{ENTER}")

    # Clicking the send button
    try:
        x_arg_imgsend = '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div[2]/div/div/span'
        whatsapp_send_button = wait.until(
            EC.presence_of_element_located((By.XPATH, x_arg_imgsend)))
        whatsapp_send_button.click()
    except:
        traceback.print_exc()


def sender(contact, isAttach, original_msg, image_path):
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
        time.sleep(1 + random()*10/5)

    error_file.close()


if __name__ == "__main__":
    # Initiating contacts, attachment, and message
    list_of_contact = import_contacts()
    isAttach, image_path = attachment_verification()
    original_msg = import_message()

    # Login and Scan
    whatsapp_login(fmsg)

    # Sending the messages
    sender(list_of_contact, isAttach, original_msg, image_path)

    print("Done!\nKontak kontak tanpa WA disimpan pada file 'contact_error.txt'")
