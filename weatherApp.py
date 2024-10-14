import os
import sys
import requests
from dotenv import load_dotenv
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
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
        hbox = QHBoxLayout()

        # Variables
        self.instruction = QLabel("Enter city name: ")
        self.city_input = QLineEdit()
        self.get_weather_btn = QPushButton("Get Weather")
        self.temperature_label = QLabel("Temperature")
        self.humidity_label = QLabel("Humidity")
        self.condition_label = QLabel("Condition")

        # Adding to layout
        vbox.addWidget(self.instruction)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_btn)
        hbox.addWidget(self.temperature_label)
        hbox.addWidget(self.humidity_label)
        vbox.addLayout(hbox)
        vbox.addWidget(self.condition_label)

        self.get_weather_btn.clicked.connect(self.get_weather)

    # Move application to center of screen
    def centerWindow(self):
        screen_center = QApplication.desktop().screenGeometry().center()
        frame_geometry = self.frameGeometry()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())

    def get_weather(self):
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}" # API call by city name

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200: # Successful request code
                self.display_weather(data)

        except Exception as e:
            print(e)

    def display_weather(self, data):
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        self.temperature_label.setText(str(temperature))
        self.humidity_label.setText(str(humidity))

if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("API_KEY") # Get API_KEY from local .env file
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
    