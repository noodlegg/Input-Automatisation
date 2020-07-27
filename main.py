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
        Discord.clickAtImg("dc_input.PNG")
        Discord.write(".")
        Discord.hotkey("enter")
        time.sleep(1)

        # Check whether card spawned
        try:
            startCoord = Discord.locateImg("dc_spawn.PNG")
            countSpawned += 1
        except:
            print("No card spawn detected!")
            time.sleep(60)
            continue
            
        # Click on the card to enlarge
        Discord.clickAtCoord((startCoord[0]+100, startCoord[1]+100))
        time.sleep(1)
        try:
            startCoord = Discord.locateImg("dc_card.PNG")
        except:
            print("Did not detect enlarged card!")
            Discord.hotkey("esc")
            time.sleep(2)
            continue

        # Screenshot the code using OCR
        OCR.hotkey("ctrl", "d", "1")
        # Offset to start at the top left of the code
        coords = list(startCoord)
        coords[0] += 7
        coords[1] -= 64
        startCoord = tuple(coords)
        OCR.dragRelative(startCoord, 295, 40)

        # Close card enlargement in Discord
        Discord.clickAtCoord(startCoord)
        Discord.hotkey("esc")
        time.sleep(0.5)

        # Retrieve code from OCR
        try:
            OCR.clickAtImg("ocr_read.PNG")
            time.sleep(1.5)
            OCR.clickAtImg("ocr_copy.PNG")
        except:
            print("Failed to click on OCR interface!")
            continue
        code = r.clipboard_get()
        # Only keep letters without spaces using RegEx
        code = re.sub('[^a-zA-Z]+', '', code)
        output = "claim " + code
        print("Output is going to be: " + output)
        Discord.clickAtImg("dc_input.PNG")
        Discord.write(output)
        Discord.hotkey("enter")

        # Check whether card is claimed successfully
        try:
            Discord.locateImg("dc_claimed.PNG")
            countClaimed += 1
        except:
            print("Failed to claim the card!")
        print("Spawns: " + str(countSpawned) + " / Claimed: " + str(countClaimed))
        time.sleep(120)
