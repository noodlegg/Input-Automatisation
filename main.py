from objective import Objective
from tkinter import Tk
import time
import re

# Automated sequence of actions for interaction with Discord bot
# Requires you to have the Discord client in the foreground
# TODO: Instead of time.sleep() it should await for some period of time

r = Tk()
Discord = Objective("Discord")
OCR = Objective("OCR")
countSpawned = 0
countClaimed = 0

# Execution loop
if __name__ == "__main__":
    while True:
        # Type something in Discord chat
        try:
            Discord.clickAtImg("dc_input.PNG")
            Discord.write(".")
            Discord.hotkey("enter")
            time.sleep(0.7)
        except:
            print("Couldn't find Discord input field!")
            continue

        # Check whether card spawned
        try:
            startCoord = Discord.locateImg("dc_spawn.PNG")
            countSpawned += 1
        except:
            print("No card spawn detected!")
            time.sleep(30)
            continue
            
        # Click on the card to enlarge
        Discord.clickAtCoord((startCoord[0]+100, startCoord[1]+100))
        time.sleep(0.5)
        try:
            startCoord = Discord.locateImg("dc_card.PNG")
        except:
            print("Did not detect enlarged card!")
            Discord.hotkey("esc")
            continue

        # Screenshot the code using OCR
        OCR.hotkey("ctrl", "d", "1")
        # Offset to start at the top left of the code
        coords = list(startCoord)
        coords[0] += 7
        coords[1] -= 64
        startCoord = tuple(coords)
        OCR.dragRelative(startCoord, 295, 44)

        # Close card enlargement in Discord
        Discord.clickAtCoord(startCoord)
        Discord.hotkey("esc")
        time.sleep(1.2)

        # Retrieve code from OCR
        # try:
        #     OCR.clickAtImg("ocr_read.PNG")
        #     time.sleep(1)
        #     OCR.clickAtImg("ocr_copy.PNG")
        # except:
        #     print("Failed to click on OCR interface!")
        #     continue
        code = r.clipboard_get()
        # Only keep letters without spaces using RegEx
        code = re.sub('[^a-zA-Z]+', '', code)
        output = "claim " + code
        print("Output is going to be: " + output)
        Discord.clickAtImg("dc_input.PNG")
        Discord.write(output)
        Discord.hotkey("enter")
        time.sleep(1)

        # Check whether card is claimed successfully
        try:
            Discord.locateImg("dc_claimed.PNG")
            countClaimed += 1
        except:
            print("Failed to claim the card!")
        print("Spawns: " + str(countSpawned) + " / Claimed: " + str(countClaimed))

        # Workaround for the EasyScreenOCR limit
        if countSpawned % 20 == 0:
            OCR.clickAtImg("taskbar_expand.PNG")
            OCR.clickAtImg("ocr_icon.PNG", "right")
            OCR.clickAtImg("ocr_exit.PNG")
            OCR.clickAtImg("ocr_crack.PNG")
            OCR.clickAtImg("ocr_crack.PNG")
            time.sleep(0.5)
            OCR.hotkey("enter")
            OCR.hotkey("enter")
            OCR.clickAtImg("ocr_shortcut.PNG")
            OCR.clickAtImg("ocr_shortcut.PNG")
        time.sleep(60)


