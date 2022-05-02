import os
import platform
import traceback
import time
from random import seed, random
import argparse

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

from tkinter import Tk
from tkinter import filedialog

try:
    import autoit
except ModuleNotFoundError:
    pass


def whatsapp_login():
    global wait, wait_long, browser, search_button, back_button
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
    wait_long = WebDriverWait(browser, 10)
    browser.get(Link)
    browser.maximize_window()

    input("\nAfter the page loads properly, press [ENTER]\n")
    input(
        "Now, try to copy the message until the 'WA preview' for the links loads properly, then delete it again\nFinally press [ENTER]\n")

    # Defining the buttons
    search_x_arg = "//button[.//span[@data-icon='search']]"
    search_button = wait.until(
        EC.presence_of_element_located((By.XPATH, search_x_arg)))

    back_x_arg = "//span[@data-icon='back']/.."
    back_button = wait.until(
        EC.presence_of_element_located((By.XPATH, back_x_arg)))

def isSearchActive():
    search_active = back_button.value_of_css_property("opacity")
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
        fp = open(contact_file_path, "r")
        fp.close()
    except:
        print("Select contact file")
        root = Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        contact_file_path = file_path

    try:
        fp = open(contact_file_path, "r")
        fp.close()
    except Exception as e:
        raise e

    return contact_file_path

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


def send_message(target, isAttach, image_path):
    name_x_arg = '//span[@title="' + target + '"]'
    mainname_x_arg = '//*[@id="main"]/header/div[2]/div/div/span[@title="' + target + '"]'
    msgbtn_x_arg = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span[@data-icon="send"]/..'
    msgbox_x_arg = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]'
    voicebtn_x_arg = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span[@data-icon="ptt"]/..'
    backbtn_x_arg = '//*[@id="side"]/div[1]/div/button[@aria-label="Chat list"]'
    loopbtn_x_arg = '//*[@id="side"]/div[1]/div/button[@aria-label="Search or start new chat"]'

    if isSearchActive():
        print("Search is active, unpressing the button")
        search_button.click()
        wait_long.until(
            EC.presence_of_element_located((By.XPATH, loopbtn_x_arg)))

    search_button.click()
    wait_long.until(
        EC.presence_of_element_located((By.XPATH, backbtn_x_arg)))

    actions = ActionChains(browser)
    actions.send_keys(target)
    actions.perform()

    try:
        group_title = wait.until(
            EC.presence_of_element_located((By.XPATH, name_x_arg)))
        group_title.click()
    except:
        error =  "TIDAK ADA DI WA"
        return error

    try:
        browser.find_element_by_xpath(
            "//*[contains(text(),'t send a message to blocked contact')]")
        error = "DIBLOCK"
        return error
    except:
        pass

    try:
        browser.find_element_by_xpath(
            "//*[contains(text(),'Tidak dapat mengirim pesan ke kontak terblokir')]")
        error = "DIBLOCK"
        return error
    except:
        pass

    wait_long.until(
        EC.presence_of_element_located((By.XPATH, mainname_x_arg)))

    input_box = wait.until(
        EC.presence_of_element_located((By.XPATH, msgbox_x_arg)))

    ActionChains(browser).key_down(Keys.CONTROL).key_down('v').perform()
    ActionChains(browser).key_up(Keys.CONTROL).key_up('v').perform()

    send_button = wait.until(
        EC.presence_of_element_located((By.XPATH, msgbtn_x_arg)))
    send_button.click()
    voice_button = wait.until(
        EC.presence_of_element_located((By.XPATH, voicebtn_x_arg)))
    print("Message sent successfully to " + target)
    

    if (isAttach == "yes"):
        try:
            send_attachment(image_path)
        except:
            print('Attachment not sent.')


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
    imgsend_x_arg = '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div[2]/div/div/span'
    imgsend_button = wait.until(
        EC.presence_of_element_located((By.XPATH, imgsend_x_arg)))

    try:
        
        imgsend_button.click()
    except:
        traceback.print_exc()


def sender(contact, isAttach, image_path):
    # Initiating error file
    error_file = open('contact_error.txt', 'w')
    error_file.write(
        "Here are some contacts that give errors in this session\n")
    error_file.close()
    error_file = open('contact_error.txt', 'a', buffering=1)

    # Iterating through contacts list

    fp = open(contact, "r")
    while True:
        target = fp.readline()
        target = target.replace("\n", "")
        if not target:
            break

        try:
            status = send_message(target, isAttach, image_path)
        except:
            print(target + " perlu di cek")
            error_file.write(target + "\n")
            search_button.click()

        if status:
            print(target + " " + status)
            error_file.write(target + "\n")
            search_button.click()

        time.sleep(1)

    error_file.close()


if __name__ == "__main__":
    # Initiating contacts, attachment, and message
    contact_path = contact_parser()
    isAttach, image_path = attachment_verification()

    # Login and Scan
    whatsapp_login()

    # Sending the messages
    sender(contact_path, isAttach, image_path)

    print("Done!\nKontak kontak tanpa WA disimpan pada file 'contact_error.txt'")


# NOT YET USED

# new browser.executeScript("document.getElementById('gsc-i-id1').value='Selenium'");

# def import_message():
#     input("Copy the message that you want to send\n Then press [ENTER]")
#     # copy message to clipboard
#     try:
#         r = Tk()
#         r.withdraw()
#         copied_text = r.clipboard_get()
#         return copied_text
#     except:
#         return None

# def update_clipboard(original_msg):
#     r = Tk()
#     r.withdraw()
#     r.clipboard_append(original_msg)
#     r.update()

    
# if __name__ == "__main__":
#     # Initiating contacts, attachment, and message
#     list_of_contact = import_contacts()
#     isAttach, image_path = attachment_verification()
#     original_msg = import_message()

#     # Login and Scan
#     whatsapp_login(fmsg)

#     # Sending the messages
#     sender(list_of_contact, isAttach, original_msg, image_path)

#     print("Done!\nKontak kontak tanpa WA disimpan pada file 'contact_error.txt'")