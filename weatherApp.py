import os
import sys
from dotenv import load_dotenv
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton
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
        grid = QGridLayout()
        central_widget.setLayout(grid)

        # Variables
        self.instruction = QLabel("Enter city name: ")
        self.city = QLineEdit()
        self.get_weather_btn = QPushButton("Get Weather")


        # Adding to grid layout
        grid.addWidget(self.instruction, 0, 0)
        grid.addWidget(self.city, 1, 0)
        grid.addWidget(self.get_weather_btn, 2, 0)

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
    