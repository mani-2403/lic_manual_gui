from PyQt6.QtWidgets import QApplication, QWidget, QPushButton
from PyQt6.QtGui import QPainter, QColor, QPen, QFont
from PyQt6.QtCore import Qt
import sys

class BlockCircuit(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Block Circuit - Diode OR Gate")
        self.setGeometry(100, 100, 1000, 600)

        self.switch1_on = False
        self.switch2_on = False

        # Buttons
        self.s1_btn = QPushButton("Switch 1 OFF", self)
        self.s1_btn.setGeometry(50, 20, 150, 40)
        self.s1_btn.clicked.connect(self.toggle_s1)

        self.s2_btn = QPushButton("Switch 2 OFF", self)
        self.s2_btn.setGeometry(50, 70, 150, 40)
        self.s2_btn.clicked.connect(self.toggle_s2)

    def toggle_s1(self):
        self.switch1_on = not self.switch1_on
        self.s1_btn.setText(f"Switch 1 {'ON' if self.switch1_on else 'OFF'}")
        self.update()

    def toggle_s2(self):
        self.switch2_on = not self.switch2_on
        self.s2_btn.setText(f"Switch 2 {'ON' if self.switch2_on else 'OFF'}")
        self.update()

    def draw_block(self, painter, x, y, w, h, label, color=Qt.GlobalColor.white):
        painter.setBrush(QColor(color))
        painter.drawRect(x, y, w, h)
        painter.drawText(x + 10, y + h // 2 + 5, label)
        painter.setBrush(Qt.BrushStyle.NoBrush)

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.GlobalColor.black, 2)
        painter.setPen(pen)
        font = QFont("Arial", 10)
        painter.setFont(font)

        # Block Positions
        bx = {
            'switch1': (150, 100),
            'diode1': (300, 100),

            'switch2': (150, 200),
            'diode2': (300, 200),

            'resistor1': (450, 150),
            'led': (600, 150),
            'battery_pos': (750, 150),
            'battery_neg': (150, 350)
        }

        # Draw Blocks
        self.draw_block(painter, *bx['switch1'], 100, 40, "Switch 1", "lightgreen" if self.switch1_on else "lightgray")
        self.draw_block(painter, *bx['diode1'], 100, 40, "Diode 1")

        self.draw_block(painter, *bx['switch2'], 100, 40, "Switch 2", "lightgreen" if self.switch2_on else "lightgray")
        self.draw_block(painter, *bx['diode2'], 100, 40, "Diode 2")

        self.draw_block(painter, *bx['resistor1'], 100, 40, "Resistor 1")

        # LED logic: ON if any one switch is ON
        led_color = "yellow" if (self.switch1_on or self.switch2_on) else "lightgray"
        self.draw_block(painter, *bx['led'], 100, 40, "LED", led_color)

        self.draw_block(painter, *bx['battery_pos'], 100, 40, "Battery (+)")
        self.draw_block(painter, *bx['battery_neg'], 100, 40, "Battery (−)")

        # Draw Connections
        def line(x1, y1, x2, y2):
            painter.drawLine(x1, y1, x2, y2)

        # Switches to Diodes
        line(250, 120, 300, 120)  # Switch1 to Diode1
        line(250, 220, 300, 220)  # Switch2 to Diode2

        # Diodes to Resistor (joined)
        line(400, 120, 450, 170)  # Diode1 to Resistor
        line(400, 220, 450, 170)  # Diode2 to Resistor

        # Resistor1 to LED
        line(550, 170, 600, 170)

        # LED to Battery +
        line(700, 170, 750, 170)

        # Battery (−) to Switches
        line(200, 370, 200, 140)  # to Switch1
        line(200, 370, 200, 240)  # to Switch2

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = BlockCircuit()
    win.show()
    sys.exit(app.exec())
