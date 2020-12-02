# WA Bot
Python Bot to automate Whatsapp message through Contacts list in Windows OS

## Pre-installation
1. Download the Repo

## Installation
1. Install Python in your Windows OS
2. Install some modules using `pip install pyautoit selenium`
3. Install PyAutoIt in the attached directory
4. Install the corresponding Google Chrome browser version. This Repo uses Chrome v87

## Before using it:
1. There are some issues with autoit so that the attachment windows pop-up doesn't work properly. The problem was circumvented by simulating clicks. Therefore: Set the click coordinate in `WA_bot.py` so that the location of the buttons suits the buttons position in the windows.
2. Make a list of contacts in `contacts.txt`
3. Make the message in `message.txt`. To insert emojis and formatted font, write the message in WA web first, then copy it to `message.txt` file. For formatting guide, use this https://faq.whatsapp.com/general/chats/how-to-format-your-messages/?lang=fb
4. To give a photo/ video attachment, put the photo/ video that you want to send in `.\attachment`

## To use it:
1. Open command prompt and navigate to the `WA_bot.py` directory
2. Run the script with `python WA_bot.py`. The Script will read your message and contacts. 
3. It will then ask if you want to send some attachment or not. If you want to send some attachments, type `yes` and write the file name (with the extension)

## Disclaimer:
The attachment function sends the file from your PC to WA directly. If you send some high-res file/ video, this may hog the bandwidth causing the script to stop working properly.

Credit: Remake of the work from https://github.com/shauryauppal/PyWhatsapp
