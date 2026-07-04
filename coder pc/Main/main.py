
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from OS.kernel import kernel
from Server.server import start_server
from Main.config import config
from Apps.desktop import launch_desktop
import threading
import time


def main():
    print("Booting PyOS Kernel...")
    kernel.boot()
    
    print("Starting Server in background...")
    server_thread = threading.Thread(target=start_server, args=(config.SERVER_HOST, config.SERVER_PORT), daemon=True)
    server_thread.start()
    time.sleep(1)
    
    print("Launching Desktop GUI...")
    launch_desktop()


if __name__ == "__main__":
    main()
