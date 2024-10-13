import os
import sys
from dotenv import load_dotenv
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget

class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()

if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("API_KEY") # Get API_KEY from local .env file
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
    