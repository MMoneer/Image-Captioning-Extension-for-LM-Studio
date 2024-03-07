import sys
import os
import requests
import time
from PySide6 import QtWidgets
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QTimer, QUrl, Slot
from PySide6.QtWidgets import QFileDialog
from captioning_ui import Ui_MainWindow
from openai import OpenAI
import base64
import threading
from configparser import ConfigParser

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.folder_path_pt.clicked.connect(self.select_source_folder)
        self.caption_dest_pt.clicked.connect(self.select_destination_folder)
        self.run_cation_pt.clicked.connect(self.run_captioning)
        self.info_pt.clicked.connect(self.open_url)
        
        # Read configuration from the file
        config = ConfigParser()
        config.read('config.ini')
        self.client = OpenAI(base_url=config.get('OpenAI', 'base_url'), api_key=config.get('OpenAI', 'api_key'))
        base_url = config.get('OpenAI', 'base_url')  # Fetch base_url from config file
        self.checker = self.ServerChecker(base_url, self.label_server_status)  # Replace your_label_server_status_object with your actual label object
        self.checker.start_checking()
        
        self.progress_timer = QTimer(self)  # Initialize QTimer
        self.progress_timer.timeout.connect(self.update_progress)  # Connect timer to update_progress method
        self.current_progress = 0  # Variable to track progress
    
    def closeEvent(self, event):
        # Stop the server checking process if it's active
        if self.checker.is_running:
            self.checker.stop_checking()
            self.checker.join()

        # Terminate any running threads related to captioning
        if hasattr(self, "new_thread"):
            if self.new_thread.is_alive():
                self.new_thread.terminate()
                self.new_thread.join()

        # Stop the progress timer
        if self.progress_timer.isActive():
            self.progress_timer.stop()

        # Call the default closeEvent to ensure proper window closing
        super().closeEvent(event)
    
    def open_url(self):
        url = "https://github.com/lachhabw/Image-Captioning-Extension-for-LM-Studio"  # Replace with the URL you want to open
        QDesktopServices.openUrl(QUrl(url))
        
    
    class ServerChecker:
        def __init__(self, base_url, label_server_status):
            self.base_url = base_url
            self.label_server_status = label_server_status
            self.is_running = False
            self.thread = None

        def check_server(self):
            try:
                response = requests.get(self.base_url)
                if response.status_code == 200:
                    self.label_server_status.setStyleSheet("color: green; background-color: rgba(0, 0, 0, 0)")
                    self.label_server_status.setText("Connected")
                else:
                    self.label_server_status.setStyleSheet("color: red; background-color: rgba(0, 0, 0, 0)")
                    self.label_server_status.setText("Not Connected")
            except requests.exceptions.RequestException:
                self.label_server_status.setStyleSheet("color: red; background-color: rgba(0, 0, 0, 0)")
                self.label_server_status.setText("Not Connected")

        def start_checking(self):
            self.is_running = True
            self.thread = threading.Thread(target=self.check_server)
            self.thread.start()
            threading.Timer(30, self.start_checking).start()  # Check every 30 seconds    
        
        def stop_checking(self):
            self.is_running = False

        def join(self):
            if self.thread is not None:
                self.thread.join()

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
        

    def run_captioning_thread(self):
        # Disable the captioning button
        self.run_cation_pt.setDisabled(True)
        # Start a new thread for captioning
        self.new_thread = threading.Thread(target=self.run_captioning_with_thread)
        self.new_thread.start()

    def run_captioning_with_thread(self):
        try:
            self.run_captioning()
        finally:
            # Enable the captioning button after the process finishes
            self.run_cation_pt.setEnabled(True)

    def update_progress(self):
        # Update progress bar
        self.progressBar.setValue(self.current_progress)

        # If progress reaches maximum value, stop QTimer
        if self.current_progress == self.progressBar.maximum():
            self.progress_timer.stop()
            
            # Enable the captioning button after the process finishes
            self.run_cation_pt.setEnabled(True)
    
    def run_captioning(self):
        # Get folders paths
        self.source_folder_path = self.lineEdit_folder_path.text()
        self.destination_folder_path = self.lineEdit_caption_path.text()
        self.progressBar.setValue(0)

        if not self.source_folder_path:
            self.textEdit.append("Please select the source folder.")
            return

        if not self.destination_folder_path:
            # If destination folder is not selected, use source folder as destination
            self.textEdit.append("<font color='blue'>The captions will be saved in the same images folder.</font>")
            self.destination_folder_path = self.source_folder_path

        try:
            # Check the existence of folders
            os.listdir(self.source_folder_path)
            os.listdir(self.destination_folder_path)
            files = os.listdir(self.source_folder_path)
            n_files = len(files)

            self.progressBar.setMaximum(n_files)
            self.current_progress = 0  # Variable to track progress
            
            # Start progress timer
            self.progress_timer.start()

            for i, file in enumerate(files):
                file_path = os.path.join(self.source_folder_path, file)
                destination_path = os.path.join(self.destination_folder_path, f"{file.split('.')[0]}.txt")
                img = self.load_img64(file_path)
                if not img:
                    continue

                captions = self.caption_server(img)
                if not captions:
                    self.textEdit.append("- Failure: ")
                    self.textEdit.append(f"Unable to caption the image '{file}'. Check if the image is valid, with a supported format (jpeg, jpg, png, are recommended).")
                else:
                    with open(destination_path, "w") as f:
                        f.write(captions)
                    
                    self.textEdit.append("<font color='green'>- Success: </font>")
                    self.textEdit.append(f"Image '{file}' has been captioned and the result saved to '{destination_path}'")
                    # Introduce a delay between iterations
                    time.sleep(0.1)  # Adjust sleep time as needed
                    
                # Increment current_progress
                self.current_progress += 1

                # Update progress bar after each iteration
                self.progressBar.setValue(self.current_progress)
            
            # Stop progress timer
            self.progress_timer.stop()
            
            # Add a green message indicating the process has finished
            self.textEdit.append("""<font color='green' style='font-weight: bold;'>############################<br>
    Captioning process has finished.🎉<br>
    ############################</font>""")

        except FileNotFoundError:
            self.textEdit.append("Error: Folder not found.")
        except Exception as e:
            self.textEdit.append(f"Error: {e}")

        finally:
            # Enable the captioning button after the process finishes
            self.run_cation_pt.setEnabled(True)
    
    
           
    def load_img64(self, file_path):
        base64_image = ""
        try:
            image = open(file_path, "rb").read()
            base64_image = base64.b64encode(image).decode("utf-8")
        except Exception as e:
            self.textEdit.append(f"Couldn't read the file: {file_path}\n")
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
            stream=True
        )

        captions = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                caption = chunk.choices[0].delta.content
                captions += caption
        return captions.strip()
    

if __name__ == "__main__":
  app = QtWidgets.QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec())
