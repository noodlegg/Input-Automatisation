from objective import Objective
from tkinter import Tk
from pywinauto.application import Application
import time
import json
import random
import string
import datetime

# Automated creation of new OSRS accounts using Google Chrome
# the accounts will be stored in a JSON file

account = {}
dob = []
r = Tk()
chrome = Objective("GoogleChrome")
tempMailLink = "https://temp-mail.org/"
dir = "osrs/"

failCount = 0
attemptCount = 0

def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str

def fill_random_dateofbirth(objective):
    dob = [random.randint(1, 29), random.randint(1, 12), random.randint(1940, 2002)]
    objective.write(str(dob[0]))
    objective.hotkey("tab")
    objective.write(str(dob[1]))
    objective.hotkey("tab")
    objective.write(str(dob[2]))

if __name__ == "__main__":

    while (True):
        attemptCount += 1
        try:
            # TODO: Open/select Google Chrome as active window
            time.sleep(2)

            # Open incognito window
            chrome.hotkey("ctrl", "shift", "n")

            # Go to disposable e-mail site to retrieve e-mail address
            chrome.write(tempMailLink)
            chrome.hotkey("enter")
            time.sleep(6)
            chrome.clickAtImg(dir+"tempmail_copy.PNG")

            # Open new tab and go to OSRS site to sign up
            chrome.hotkey("ctrl", "t")
            chrome.write("https://secure.runescape.com/m=account-creation/create_account?theme=oldschool")
            chrome.hotkey("enter")
            time.sleep(5)

            # Sign up procedure
            email = r.clipboard_get()
            chrome.write(email)
            chrome.hotkey("tab")
            password = get_random_alphanumeric_string(8)
            chrome.write(password)
            chrome.hotkey("tab")
            fill_random_dateofbirth(chrome)

            try:
                chrome.clickAtImg(dir+"web_cookies.PNG")
            except:
                print("Don't need to accept cookies :]")

            chrome.clickAtImg(dir+"web_playnow.PNG")
            time.sleep(4)

            try:
                chrome.locateImg(dir+"web_signup_success.PNG")
            except:
                raise Exception("Account creation failed!")

            # Close tab and verify e-mail
            chrome.hotkey("ctrl", "w")
            time.sleep(2)
            attempt = 0
            sleepTime = 2
            while True:
                if attempt > 7:
                    raise Exception("Still no e-mail after 6 refreshes!")
                try:
                    attempt += 1
                    chrome.clickAtImg(dir+"tempmail_mail.PNG")
                    break
                except:
                    chrome.clickAtImg(dir+"tempmail_refresh.PNG")
                    time.sleep(sleepTime)
                    sleepTime *= 2

            time.sleep(2)
            chrome.scroll(-500)
            chrome.clickAtImg(dir+"tempmail_validate.PNG")
            time.sleep(8)
            try:
                chrome.locateImg(dir+"web_validation_success.PNG")
            except:
                raise Exception("E-mail validation link did not succeed!")

            # Store account credentials in JSON file
            account = {
                'email': email,
                'password': password,
                'createdAt': str(datetime.datetime.now()),
                'dateOfBirth': "-".join(dob)
            }
            with open('accounts.json', 'a') as f:
                json.dump(account, f, indent=2)
        except:
            failCount += 1
            print("Raised exception " + str(failCount) + " times.")

        # Close incognito window and hope we automatically refocus on Chrome
        chrome.hotkey("ctrl", "shift", "w")
        print("Success rate of " + str(attemptCount-failCount) + "/" + str(attemptCount))
