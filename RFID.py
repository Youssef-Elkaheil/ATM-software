from time import sleep
from PyQt5.QtCore import QThread, pyqtSignal
import os
# Replace this with your RFID reader library
# (e.g., SimpleMFRC522 for Raspberry Pi)
if os.getenv("RASPBERRY_PI") is not None:
    try:
        from mfrc522 import SimpleMFRC522
        class RFIDThread(QThread):
            # Define a signal to emit tag data and strength
            tag_read = pyqtSignal(str,str)

            def __init__(self):
                super().__init__()
                self.reader = SimpleMFRC522()
                self.is_running = True

            def run(self):
                while self.is_running:
                    try:
                        # Read data from the RFID reader
                        id, text = self.reader.read() 
                        if id:
                            # Emit signal with tag data and strength (optional)
                            self.tag_read.emit(str(text), str(id))  # Adjust strength value as needed
                    except Exception as e:
                        print(f"Error reading tag: {e}")
                    sleep(0.1)  # Adjust sleep time as needed
    except ImportError:
        print("mfrc522 not found. Assuming PC environment.")

