import os
import sys
import requests
from dotenv import load_dotenv
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QRadioButton, QButtonGroup
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
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()

        # Variables
        self.instruction = QLabel("Enter city name: ")
        self.city_input = QLineEdit()
        self.get_weather_btn = QPushButton("Get Weather")
        self.temperature_label = QLabel("Temperature")
        self.humidity_label = QLabel("Humidity")
        self.condition_label = QLabel("Condition")
        self.unit_label = QLabel("Temperature Unit: ")
        self.unit_choice1 = QRadioButton("Kelvin (K)")
        self.unit_choice2 = QRadioButton("Celsius (°C)")
        self.unit_choice3 = QRadioButton("Fahrenheit (°F)")
        self.unit_choice_group = QButtonGroup()
        self.unit_choice_group.addButton(self.unit_choice1)
        self.unit_choice_group.addButton(self.unit_choice2)
        self.unit_choice_group.addButton(self.unit_choice3)

        # Adding to layout
        vbox.addWidget(self.instruction)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_btn)
        vbox.addWidget(self.unit_label)
        hbox1.addWidget(self.unit_choice1)
        hbox1.addWidget(self.unit_choice2)
        hbox1.addWidget(self.unit_choice3)
        vbox.addLayout(hbox1)
        hbox2.addWidget(self.temperature_label)
        hbox2.addWidget(self.humidity_label)
        vbox.addLayout(hbox2)
        vbox.addWidget(self.condition_label)

        # Connect buttons
        self.get_weather_btn.clicked.connect(self.get_weather)
        self.unit_choice1.toggled.connect(self.unit_changed)
        self.unit_choice2.toggled.connect(self.unit_changed)
        self.unit_choice3.toggled.connect(self.unit_changed)

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

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("400 Bad Request:\nPlease check your input")
                case 401:
                    self.display_error("401 Unauthorized:\nInvalid API key")
                case 403:
                    self.display_error("403 Forbidden:\nAccess is denied")
                case 404:
                    self.display_error("404 Not Found:\nCity not found")
                case 500:
                    self.display_error("500 Internal Server Error:\nPlease try again later")
                case 502:
                    self.display_error("502 Bad Gateway:\nInvalid response from server")
                case 503:
                    self.display_error("503 Service Unavailable:\nServer is down")
                case 504:
                    self.display_error("504 Gateway Timeout:\nNo response from the server")
                case _:
                    self.display_error(f"HTTP error occured:\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection")

        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nRequest timed out")

        except requests.exceptions.TooManyRedirects:
            self.display_error("Too Many Redirects:\nCheck the URL")
        
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")

    def display_weather(self, data):
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        condition = data["weather"][0]["description"]


        self.temperature_label.setText(str(temperature))
        self.humidity_label.setText(str(humidity))
        self.condition_label.setText(str(condition).capitalize())

    def display_error(self, message):
        self.condition_label.setText(message)

    def unit_changed(self):
        radio_button = self.sender()
        if radio_button.isChecked():
            print(f"{radio_button.text()} is selected.")

if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("API_KEY") # Get API_KEY from local .env file
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
    