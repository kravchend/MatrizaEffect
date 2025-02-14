import sys
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QSlider, QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QColor, QFont


class MatrixRain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Matrix Rain with Effects")
        self.setGeometry(280, 200, 1000, 600)  

        self.speed = 50 
        self.symbol_size = 7 
        self.tail_length = 20  
        self.symbols = []  

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(self.speed)

        self.init_ui()

        self.init_rain()

    def init_ui(self):
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        layout = QVBoxLayout()

        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setMinimum(10)
        self.speed_slider.setMaximum(200)
        self.speed_slider.setValue(self.speed)
        self.speed_slider.valueChanged.connect(self.change_speed)

        layout.addWidget(QLabel(""))
        layout.addWidget(self.speed_slider)

        self.main_widget.setLayout(layout)

    def change_speed(self, value):
        self.speed = value
        self.timer.setInterval(self.speed)

    def init_rain(self):
        columns = self.width() // self.symbol_size
        self.symbols = [
            {
                "x": col * self.symbol_size,
                "y": random.randint(-600, 0),
                "speed": random.randint(4, 30),
                "tail": []
            }
            for col in range(columns)
        ]

    def update_frame(self):
        for symbol in self.symbols:
            if symbol["y"] > 0:
                symbol["tail"].append((symbol["x"], symbol["y"]))
                if len(symbol["tail"]) > self.tail_length: 
                    symbol["tail"].pop(5)

            symbol["y"] += symbol["speed"]

            if symbol["y"] > self.height():
                symbol["y"] = random.randint(-1500, 0)
                symbol["tail"].clear()

        self.repaint()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0))
        painter.setFont(QFont("Courier", 16))

        for symbol in self.symbols:
            intensity = random.randint(180, 255) 
            painter.setPen(QColor(0, intensity, 0))
            text = random.choice(["0", "1", chr(random.randint(0x30A0, 0x30FF))])
            painter.drawText(symbol["x"], symbol["y"], text)

            for i, (x, y) in enumerate(symbol["tail"]):
                tail_intensity = max(0, 255 - (i * (255// self.tail_length))) 
                painter.setPen(QColor(5, tail_intensity, 5))
                painter.drawText(x, y, random.choice(["0", "1", chr(random.randint(0x30A0, 0x30FF))]))

        painter.end()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MatrixRain()
    window.show()
    sys.exit(app.exec())
