import os.path
import signal
import sys
import databaseHandler as db
import categories
import products
import menus


def signal_handler(sig, frame):
    print("CTRL-C -- exit!\nBye")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

# Initialize database
db.initialize()

# Initialize categories
categories.initialize()

# Initialize products
products.initialize()

# Initialize main menu
mainMenu = menus.MainMenu()
mainMenu.show()
