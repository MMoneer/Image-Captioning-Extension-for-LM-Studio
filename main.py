import sys
import os
import requests
import time
import subprocess
from PySide6 import QtWidgets
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QTimer, QUrl, QThread, Signal
from PySide6.QtWidgets import QFileDialog
from captioning_ui import Ui_MainWindow
import base64
from configparser import ConfigParser
from openai import OpenAI
from playsound import playsound


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.folder_path_pt.clicked.connect(self.select_source_folder)
        self.caption_dest_pt.clicked.connect(self.select_destination_folder)
        self.run_cation_pt.clicked.connect(self.run_captioning)
        self.info_pt.clicked.connect(self.open_url)
        self.spinBox_checkserver_time.valueChanged.connect(self.update_check_interval)

        # Read configuration from the file
        config = ConfigParser()
        config.read('config.ini')
        self.client = OpenAI(base_url=config.get('OpenAI', 'base_url'), api_key=config.get('OpenAI', 'api_key'))
        base_url = config.get('OpenAI', 'base_url')  # Fetch base_url from config file
        check_interval = config.getint('Settings', 'check_interval', fallback=10)  # Fetch interval from config with a fallback
        self.checker = self.ServerChecker(self.label_server_status, check_interval)  # Correct parameter order
        self.checker.start()

        self.progress_timer = QTimer(self)  # Initialize QTimer
        self.progress_timer.timeout.connect(self.update_progress)  # Connect timer to update_progress method
        self.current_progress = 0  # Variable to track progress

    def update_check_interval(self):
        new_interval = int(self.spinBox_checkserver_time.value())  # Ensure interval is an integer
        self.checker.update_interval(new_interval)
    
    def closeEvent(self, event):
        # Stop the server checking process if it's active
        if self.checker.isRunning():
            self.checker.stop()
            self.checker.wait()

        # Terminate any running threads related to captioning
        if hasattr(self, "captioning_thread"):
            if self.captioning_thread.isRunning():
                self.captioning_thread.stop()
                self.captioning_thread.wait()

        # Stop the progress timer
        if self.progress_timer.isActive():
            self.progress_timer.stop()

        # Call the default closeEvent to ensure proper window closing
        super().closeEvent(event)

    def update_progress(self, value):
        # Update progress bar
        self.progressBar.setValue(value)

        # If progress reaches maximum value, stop QTimer
        if value >= self.progressBar.maximum():
            self.progress_timer.stop()
            # Enable the captioning button after the process finishes
            self.run_cation_pt.setEnabled(True)

    def open_url(self):
        url = "https://github.com/lachhabw/Image-Captioning-Extension-for-LM-Studio"  # Replace with the URL you want to open
        QDesktopServices.openUrl(QUrl(url))

    class ServerChecker(QThread):
        def __init__(self, label_server_status, interval=10):
            super().__init__()
            self.interval = int(interval)  # Ensure interval is an integer
            self.label_server_status = label_server_status
            self.is_running = True

        def update_interval(self, new_interval):
            self.interval = int(new_interval)  # Ensure interval is an integer

        def run(self):
            while self.is_running:
                try:
                    result = subprocess.run(["lms", "status"], capture_output=True, text=True, creationflags=subprocess.DETACHED_PROCESS)
                    output = result.stdout
                    
                    # print(f"DEBUG: subprocess.run output: {output}")  # Debug print

                    if "Server:  OFF" in output:
                        # print("DEBUG: Setting label_server_status to Not Connected")  # Debug print
                        self.label_server_status.setStyleSheet("color: red; background-color: rgba(0, 0, 0, 0)")
                        self.label_server_status.setText("Not Connected")
                    else:
                        # print("DEBUG: Setting label_server_status to Connected")  # Debug print
                        self.label_server_status.setStyleSheet("color: green; background-color: rgba(0, 0, 0, 0)")
                        self.label_server_status.setText("Connected")
                except requests.exceptions.RequestException as e:
                    # print(f"DEBUG: Exception occurred: {e}")  # Debug print
                    self.label_server_status.setStyleSheet("color: red; background-color: rgba(0, 0, 0, 0)")
                    self.label_server_status.setText("Not Connected")

                # print(f"DEBUG: self.interval type: {type(self.interval)}, value: {self.interval}")  # Debug print
                time.sleep(self.interval)

        def stop(self):
            self.is_running = False
            self.wait()

    class CaptioningThread(QThread):
        progress_update = Signal(int)
        set_progress_max = Signal(int)

        def __init__(self, client, source_folder, destination_folder, text_edit):
            super().__init__()
            self.client = client
            self.source_folder = source_folder
            self.destination_folder = destination_folder
            self.text_edit = text_edit
            self.is_running = True

        def run(self):
            try:
                files = [file for file in os.listdir(self.source_folder) if file.lower().endswith((".png", ".jpg", ".jpeg"))]
                n_files = len(files)
                self.set_progress_max.emit(n_files)  # Emit total file count to set progress bar maximum

                for i, file in enumerate(files):
                    if not self.is_running:
                        break
                    file_path = os.path.join(self.source_folder, file)
                    destination_path = os.path.join(self.destination_folder, f"{file.split('.')[0]}.txt")
                    img = self.load_img64(file_path)
                    if not img:
                        continue

                    captions = self.caption_server(img)
                    if not captions:
                        self.text_edit.append("- Failure: ")
                        self.text_edit.append(f"Unable to caption the image '{file}'. Check if the image is valid, with a supported format (jpeg, jpg, png, are recommended).")
                    else:
                        with open(destination_path, "w") as f:
                            f.write(captions)

                        self.text_edit.append("<font color='green'>- Success: </font>")
                        self.text_edit.append(f"Image '{file}' has been captioned and the result saved to '{destination_path}'")
                        # Introduce a delay between iterations
                        time.sleep(0.1)  # Adjust sleep time as needed

                    self.progress_update.emit(i + 1)

                self.progress_update.emit(n_files)
                self.text_edit.append("""<font color='green' style='font-weight: bold;'>############################<br>
Captioning process has finished.🎉<br>
############################</font>""")
                playsound('success.wav')
            except Exception as e:
                self.text_edit.append(f"Error: {e}")

        def stop(self):
            self.is_running = False

        def load_img64(self, file_path):
            base64_image = ""
            try:
                image = open(file_path, "rb").read()
                base64_image = base64.b64encode(image).decode("utf-8")
            except Exception as e:
                self.text_edit.append(f"Couldn't read the file: {file_path}\n")
            return base64_image

        def caption_server(self, base64_image):
            completion = self.client.chat.completions.create(
                model="local-model",  # not used
                messages=[
                    {
                        "role": "system",
                        "content": "This is a chat between a user and an assistant. The assistant is helping the user to describe an image.",
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Describe in detail what this image depicts in as much detail as possible without mistakes."},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                },
                            },
                        ],
                    }
                ],
                max_tokens=1000,
                stream=True,
            )

            captions = ""
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    caption = chunk.choices[0].delta.content
                    captions += caption
            return captions.strip()

    def select_source_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Source Folder')
        self.lineEdit_folder_path.setText(folder_path)
        self.source_folder_path = folder_path
        # check files type is PNG, JPEG, and JPG or not
        image_files = [name for name in os.listdir(folder_path) if name.lower().endswith((".png", ".jpg", ".jpeg"))]
        files_count = len(image_files)
        self.lcdNumber.display(str(files_count))

    def select_destination_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Destination Folder')
        self.lineEdit_caption_path.setText(folder_path)
        self.destination_folder_path = folder_path

    def run_captioning(self):
        # Get folders paths
        source_folder_path = self.lineEdit_folder_path.text()
        destination_folder_path = self.lineEdit_caption_path.text()
        self.progressBar.setValue(0)

        if not source_folder_path:
            self.textEdit.append("Please select the source folder.")
            return

        if not destination_folder_path:
            # If destination folder is not selected, use source folder as destination
            self.textEdit.append("<font color='blue'>The captions will be saved in the same images folder.</font>")
            destination_folder_path = source_folder_path

        self.captioning_thread = self.CaptioningThread(self.client, source_folder_path, destination_folder_path, self.textEdit)
        self.captioning_thread.progress_update.connect(self.update_progress)
        self.captioning_thread.set_progress_max.connect(self.progressBar.setMaximum)
        self.captioning_thread.start()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())