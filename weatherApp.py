import os
import sys
from dotenv import load_dotenv
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtGui import QIcon

class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App")
        self.setWindowIcon(QIcon("weatherIcon.png"))
        self.setFixedSize(600, 700)
        self.centerWindow()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        vbox = QVBoxLayout()
        central_widget.setLayout(vbox)

        # Variables
        self.instruction = QLabel("Enter city name: ")
        self.city = QLineEdit()
        self.get_weather_btn = QPushButton("Get Weather")
        self.temperature_label = QLabel("Temperature")
        self.humidity_label = QLabel("Humidity")
        self.condition_label = QLabel("Condition")

        # Adding to vbox layout
        vbox.addWidget(self.instruction)
        vbox.addWidget(self.city)
        vbox.addWidget(self.get_weather_btn)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.humidity_label)
        vbox.addWidget(self.condition_label)

    # Move application to center of screen
    def centerWindow(self):
        screen_center = QApplication.desktop().screenGeometry().center()
        frame_geometry = self.frameGeometry()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())
        

if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("API_KEY") # Get API_KEY from local .env file
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
    