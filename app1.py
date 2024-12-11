import sys
import mysql.connector
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton,
    QLineEdit, QLabel, QMessageBox, QStackedWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor
from plotly_graph_plotter import PlotlyGraphPlotter  # Import the main window


# Database connection function
def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",  # XAMPP MySQL host
            user="root",       # Default XAMPP MySQL username
            password="",       # Default XAMPP MySQL password
            database="user_auth"
        )
        return connection
    except mysql.connector.Error as err:
        QMessageBox.critical(None, "Database Error", f"Error: {str(err)}")
        sys.exit()


# Base Window Class for Styling
class StyledWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                background-color: black;
                color: green;
                font-size: 16px;
                font-family: Arial, sans-serif;
            }
            QPushButton {
                background-color: green;
                color: black;
                font-size: 16px;
                border: 1px solid green;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: lightgreen;
            }
            QLineEdit {
                background-color: black;
                color: green;
                border: 1px solid green;
                padding: 5px;
            }
        """)
        self.setGeometry(100, 100, 1200, 800)  # Set size and position for all windows


# Sign-Up Window
class SignUpWindow(StyledWindow):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Sign Up")
        self.layout = QVBoxLayout(self)

        self.label = QLabel("Create an Account")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Enter Username")
        self.layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_input)

        self.sign_up_button = QPushButton("Sign Up", self)
        self.sign_up_button.clicked.connect(self.sign_up)
        self.layout.addWidget(self.sign_up_button)

        self.go_to_login_button = QPushButton("Go to Log In", self)
        self.go_to_login_button.clicked.connect(self.go_to_login)
        self.layout.addWidget(self.go_to_login_button)

    def sign_up(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return

        connection = create_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            connection.commit()
            QMessageBox.information(self, "Success", "Account created successfully!")
            self.go_to_login()
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Error", f"Error: {str(err)}")
        finally:
            cursor.close()
            connection.close()

    def go_to_login(self):
        self.stacked_widget.setCurrentIndex(0)  # Go to Log In screen


# Log-In Window
class LoginWindow(StyledWindow):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Log In")
        self.layout = QVBoxLayout(self)

        self.label = QLabel("Log In to Your Account")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Enter Username")
        self.layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_input)

        self.log_in_button = QPushButton("Log In", self)
        self.log_in_button.clicked.connect(self.log_in)
        self.layout.addWidget(self.log_in_button)

        self.go_to_sign_up_button = QPushButton("Create an Account", self)
        self.go_to_sign_up_button.clicked.connect(self.go_to_sign_up)
        self.layout.addWidget(self.go_to_sign_up_button)

    def log_in(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return

        connection = create_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()

            if user:
                QMessageBox.information(self, "Success", "Logged in successfully!")
                self.open_main_window()
            else:
                QMessageBox.warning(self, "Error", "Invalid username or password.")
        finally:
            cursor.close()
            connection.close()

    def open_main_window(self):
        self.close()
        self.main_window = PlotlyGraphPlotter()  # Open the main Plotly window
        self.main_window.show()
          # Destroy the Log-In window

    def go_to_sign_up(self):
        self.stacked_widget.setCurrentIndex(1)  # Go to Sign-Up screen


# Main Application
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Authentication System")
        self.setGeometry(100, 100, 1200, 800)  # Set size and position for the main window
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        self.login_window = LoginWindow(self.stacked_widget)
        self.sign_up_window = SignUpWindow(self.stacked_widget)

        self.stacked_widget.addWidget(self.login_window)
        self.stacked_widget.addWidget(self.sign_up_window)

        self.stacked_widget.setCurrentIndex(0)  # Start with Log In screen


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
