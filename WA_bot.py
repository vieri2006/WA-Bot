# Importing traceback to catch xml button not found errors in the future
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

browser = None
Contact = None
contact_tanpa_wa = []
Link = "https://web.whatsapp.com/"
wait = None
choice = None
docChoice = None
doc_filename = None
unsaved_Contacts = None


def whatsapp_login():
    global wait, browser, Link
    chrome_options = Options()
    chrome_options.add_argument('--user-data-dir=./User_Data')
    chrome_options.add_argument("--log-level=3")
    browser = webdriver.Chrome(
        executable_path=chrome_default_path, options=chrome_options)
    wait = WebDriverWait(browser, 3)
    browser.get(Link)
    browser.maximize_window()


def input_message():
    global message
    # Enter your Good Morning Msg
    print("Here's your message (emojis might not be printed in the console)\n")
    message = open("message.txt", "r", encoding="utf8")
    message = message.read()
    print(message)


def send_message(target):
    global message, wait, browser
    try:
        button_x_arg = "//button[.//span[@data-icon='search']]"
        search_button = wait.until(
            EC.presence_of_element_located((By.XPATH, button_x_arg)))
        search_button.click()

        actions = ActionChains(browser)
        actions.send_keys(target[1:-1])
        actions.perform()

        time.sleep(5)

        x_arg = '//span[contains(@title,' + target + ')]'
        ct = 0
        while ct != 2:
            try:
                group_title = wait.until(
                    EC.presence_of_element_located((By.XPATH, x_arg)))
                group_title.click()
                break
            except:
                print("Gagal kirim ke " + target)
                ct += 1
                time.sleep(3)

                contact_tanpa_wa.append(target[1:-1])
                print(target + " tidak ada di WA")
                search_button.click()
                return

        input_box = browser.find_element_by_xpath(
            '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')

        ActionChains(browser).key_down(Keys.CONTROL).key_down('v').key_up(Keys.CONTROL).key_up(
            'v').key_up(Keys.BACKSPACE).perform()

        input_box.send_keys(Keys.ENTER)
        print("Message sent successfully to " + target)

    except NoSuchElementException as e:
        print("send message exception: ", e)
        return


def send_attachment(image_path):
    # Attachment Drop Down Menu
    try:
        clipButton = browser.find_element_by_xpath(
            '//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/div/span')
        clipButton.click()
    except:
        traceback.print_exc()
    time.sleep(1)

    # To send Videos and Images.
    try:
        mediaButton = browser.find_element_by_xpath(
            '//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/span/div/div/ul/li[1]/button')
        mediaButton.click()
    except:
        traceback.print_exc()
    time.sleep(2)

    # SET THE COORDINATES
    autoit.send(image_path)
    autoit.send("{ENTER}")

    time.sleep(2)

    try:
        whatsapp_send_button = browser.find_element_by_xpath(
            '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div')
        whatsapp_send_button.click()
    except:
        traceback.print_exc()


def import_contacts():
    global Contact, unsaved_Contacts
    Contact = []
    unsaved_Contacts = []
    fp = open("contacts.txt", "r")
    while True:
        line = fp.readline()
        con = ' '.join(line.split())
        if con and con.isdigit():
            unsaved_Contacts.append(int(con))
        elif con:
            Contact.append('\"' + con + '\"')
        if not line:
            break
    fp.close()


def sender():
    global Contact, choice, docChoice, unsaved_Contacts
    print(Contact, unsaved_Contacts)
    for i in Contact:
        try:
            send_message(i)
        except:
            pass
        if (isAttachment == "yes"):
            try:
                send_attachment(image_path)
            except:
                print('Attachment not sent.')
    time.sleep(5)


if __name__ == "__main__":

    import_contacts()
    input_message()

    # copy message to clipboard
    r = Tk()
    r.withdraw()
    r.clipboard_append(message)
    r.update()
    r.destroy()

    # Send Attachment Media only Images/Video
    isAttachment = input("Would you like to send attachment(yes/no): ")

    if isAttachment == "yes":
        input("To send attachment: Put the image on `.\\attachment`")
        image_name = input("Write the name of the file (including the file format): ")
        image_path = os.getcwd() + "\\attachment\\" + image_name
        print(image_path)

        while not os.path.exists(image_path):
            image_name = input("Wrong file name, Write the name of the file (including the file format): ")
            image_path = os.getcwd() + "\\attachment\\" + image_name
            print(image_path)

    # Let us login and Scan
    whatsapp_login()
    input("\nAfter the page loads properly, press [ENTER]\n")
    input("Now, try to copy the message until the 'WA preview' for the links loads properly, then delete it again\nFinally press [ENTER]\n")

    sender()
    
    contact_error = open('contact_error.txt', 'w')
    contact_tanpa_wa = "\n".join(contact_tanpa_wa)
    contact_error.write(contact_tanpa_wa)
    print("Done!\nKontak kontak tanpa WA disimpan pada file 'contact_error.txt'")
