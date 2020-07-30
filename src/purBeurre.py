import views.home as home
import config.config as config
import os.path
import signal
import sys
base_dir = os.path.dirname(__file__)
sys.path.append(base_dir)


def signal_handler(sig, frame):
    print("CTRL-C -- exit!\nBye")
    config.terminate()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


config.initialize()
Home = home.Home()
Home.show()
