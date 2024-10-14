import os
import sys
import requests
import datetime
import emoji
from dotenv import load_dotenv
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QRadioButton, QButtonGroup
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

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
        unit_hbox = QHBoxLayout()
        info_hbox = QHBoxLayout()
        button_hbox = QHBoxLayout()

        # Variables
        self.instruction = QLabel("Enter city name: ")
        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("e.g. Kuala Lumpur")
        self.get_weather_btn = QPushButton("Get Weather")
        self.temperature_label = QLabel("Temperature:\n-")
        self.humidity_label = QLabel("Humidity:\n-")
        self.condition_label = QLabel("Weather condition:\n-")
        self.unit_label = QLabel("Temperature Unit: ")
        self.unit_choice1 = QRadioButton("Kelvin (K)")
        self.unit_choice2 = QRadioButton("Celsius (°C)")
        self.unit_choice3 = QRadioButton("Fahrenheit (°F)")
        self.unit_choice_group = QButtonGroup()
        self.unit_choice_group.addButton(self.unit_choice1)
        self.unit_choice_group.addButton(self.unit_choice2)
        self.unit_choice_group.addButton(self.unit_choice3)
        self.unit_choice1.setChecked(True) # Kelvin checked by default
        self.time_label = QLabel()
        self.emoji_label = QLabel()
        self.error_label = QLabel()

        # Adding to layout
        vbox.addWidget(self.instruction)
        vbox.addWidget(self.city_input)
        button_hbox.addWidget(self.get_weather_btn)
        vbox.addLayout(button_hbox)
        vbox.addWidget(self.unit_label)
        unit_hbox.addWidget(self.unit_choice1)
        unit_hbox.addWidget(self.unit_choice2)
        unit_hbox.addWidget(self.unit_choice3)
        vbox.addLayout(unit_hbox)
        info_hbox.addWidget(self.temperature_label)
        info_hbox.addWidget(self.humidity_label)
        vbox.addLayout(info_hbox)
        vbox.addWidget(self.condition_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.time_label)
        vbox.addWidget(self.error_label)

        # Connect buttons
        self.get_weather_btn.clicked.connect(self.get_weather)

        # Styling
        self.instruction.setObjectName("instruction")
        self.city_input.setObjectName("city_input")
        self.get_weather_btn.setObjectName("get_weather_btn")
        self.temperature_label.setObjectName("temperature_label")
        self.humidity_label.setObjectName("humidity_label")
        self.condition_label.setObjectName("condition_label")
        self.unit_label.setObjectName("unit_label")
        self.unit_choice1.setObjectName("unit_choice1")
        self.unit_choice2.setObjectName("unit_choice2")
        self.unit_choice3.setObjectName("unit_choice3")
        self.unit_choice_group.setObjectName("unit_choice_group")
        self.time_label.setObjectName("time_label")
        self.emoji_label.setObjectName("emoji_label")

        self.setStyleSheet("""
                        * {
                           font-family: Verdana;
                           background-color: hsl(180, 90%, 95%);
                           font-size: 18px;
                        }
                           
                        QLabel#instruction {
                           font-size: 35px;
                           font-weight: bold;   
                        }
                           
                        QLineEdit#city_input {
                           border: 2px solid black;
                           font-size: 20px;
                           padding: 5px;   
                        }
                           
                        QPushButton {
                           background-color: hsl(193, 100%, 50%);
                           border: 2px solid hsl(207, 100%, 50%);
                           border-radius: 15px;
                        }
                           
                        QPushButton:hover {
                           background-color: hsl(193, 100%, 60%);
                           border: 2px solid hsl(207, 100, 30%);
                           font-weight: bold;
                        }
                                                         
                        QRadioButton::indicator {
                           width: 18px;
                           height: 18px;
                        }
                           
                        QLabel#temperature_label, QLabel#humidity_label, QLabel#condition_label {
                           font-size: 35px;
                           margin: 10px;
                        }
                           
                        QLabel#emoji_label {
                           font-family: Segoe UI Emoji;
                           font-size: 60px;
                        }
                        """)
        
        self.get_weather_btn.setFixedSize(200, 50)
        self.unit_label.setFixedHeight(40)
        unit_hbox.setSpacing(20)
        info_hbox.setSpacing(100)

        self.instruction.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        button_hbox.setAlignment(Qt.AlignCenter)
        self.unit_label.setAlignment(Qt.AlignCenter | Qt.AlignBottom)
        unit_hbox.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        info_hbox.setAlignment(Qt.AlignCenter)
        self.condition_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.time_label.setAlignment(Qt.AlignCenter)
        self.error_label.setAlignment(Qt.AlignCenter)

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
        self.error_label.clear()
        k_temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        weather_id = data["weather"][0]["id"]
        condition = data["weather"][0]["description"]
        unix_time = data["dt"]

        if self.unit_choice1.isChecked():
            self.temperature_label.setText(f"Temperature:\n{k_temperature:.2f} K")
        elif self.unit_choice2.isChecked():
            c_temperature = k_temperature - 273.15
            self.temperature_label.setText(f"Temperature:\n{c_temperature:.2f}°C")
        elif self.unit_choice3.isChecked():
            f_temperature = (k_temperature * 1.8) - 459.67
            self.temperature_label.setText(f"Temperature:\n{f_temperature:.2f}°F")
        else:
            self.temperature_label.setText("Pick a temperature unit!")

        self.humidity_label.setText(f"Humidity:\n{humidity}%")
        self.emoji_label.setText(self.get_emoji(weather_id))
        self.condition_label.setText(f"Weather condition:\n{str(condition).capitalize()}")

        # Unix time converted to Year-Month-Date Hour:Minute:Seconds UTC
        self.time_label.setText(f"Time Data is Taken:\n{datetime.datetime.fromtimestamp(unix_time, datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")}")

    def display_error(self, message):
        self.error_label.setText(message)
        self.temperature_label.setText("Temperature:\n-")
        self.humidity_label.setText("Humidity:\n-")
        self.condition_label.setText("Weather condition:\n-")
        self.emoji_label.clear()
        self.time_label.clear()

    def get_emoji(self, id):
        if 200 <= id <= 232: # Thunderstorm
            return emoji.emojize(":cloud_with_lightning_and_rain:")
        elif 300 <= id <= 531: # Drizzles / Rain
            return emoji.emojize(":cloud_with_rain:")
        elif 600 <= id <= 622: # Snow
            return emoji.emojize(":cloud_with_snow:")
        elif 701 <= id <= 761: # Haze / Smoke / Fog / etc.
            return emoji.emojize(":fog:")
        elif id == 762: # Volcanic ash
            return emoji.emojize(":volcano:")
        elif id == 771: # Squalls
            return emoji.emojize(":dashing_away:")
        elif id == 781: # Tornado
            return emoji.emojize(":tornado:")
        elif id == 800: # Clear
            return emoji.emojize(":sun:")
        elif 801 <= id <= 804: # Cloudy
            return emoji.emojize(":cloud:")
        else:
            return ""

if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("API_KEY") # Get API_KEY from local .env file
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
    