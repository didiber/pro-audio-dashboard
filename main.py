import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer
import subprocess

class AudioDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pro Audio Control Dashboard")
        self.setGeometry(100, 100, 400, 200)

        self.label_sample_rate = QLabel("Sample Rate: Loading...", self)
        self.label_buffer_size = QLabel("Buffer Size: Loading...", self)

        layout = QVBoxLayout()
        layout.addWidget(self.label_sample_rate)
        layout.addWidget(self.label_buffer_size)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_audio_status)
        self.timer.start(2000)  # Aktualisierung alle 2 Sekunden

    def update_audio_status(self):
        self.label_sample_rate.setText(f"Sample Rate: {self.get_sample_rate()} Hz")
        self.label_buffer_size.setText(f"Buffer Size: {self.get_buffer_size()} Frames")

    def get_sample_rate(self):
        try:
            output = subprocess.check_output(["wpctl", "status"], text=True)
            for line in output.split("\n"):
                if "clock.rate" in line:
                    return line.split()[-1]
        except Exception:
            return "Unknown"
        return "Unknown"

    def get_buffer_size(self):
        try:
            output = subprocess.check_output(["pw-cli", "info", "0"], text=True)
            for line in output.split("\n"):
                if "quantum" in line:
                    return line.split()[-1]
        except Exception:
            return "Unknown"
        return "Unknown"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AudioDashboard()
    window.show()
    sys.exit(app.exec())
