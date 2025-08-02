from PyQt6.QtWidgets import QApplication, QWidget, QPushButton
from PyQt6.QtGui import QPainter, QColor, QPen, QFont
from PyQt6.QtCore import Qt
import sys

class NorGateCircuit(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NOR Gate - Clean Aligned Circuit")
        self.setGeometry(100, 100, 1200, 600)

        self.switch2_on = False
        self.switch3_on = False

        # Buttons
        self.s2_btn = QPushButton("Switch 2A OFF", self)
        self.s2_btn.setGeometry(50, 100, 150, 40)
        self.s2_btn.clicked.connect(self.toggle_s2)

        self.s3_btn = QPushButton("Switch 3B OFF", self)
        self.s3_btn.setGeometry(50, 160, 150, 40)
        self.s3_btn.clicked.connect(self.toggle_s3)

    def toggle_s2(self):
        self.switch2_on = not self.switch2_on
        self.s2_btn.setText(f"Switch 2A {'ON' if self.switch2_on else 'OFF'}")
        self.update()

    def toggle_s3(self):
        self.switch3_on = not self.switch3_on
        self.s3_btn.setText(f"Switch 3B {'ON' if self.switch3_on else 'OFF'}")
        self.update()

    def draw_block(self, painter, x, y, w, h, label, color=Qt.GlobalColor.white):
        painter.setBrush(QColor(color))
        painter.drawRect(x, y, w, h)
        painter.drawText(x + 6, y + h // 2 + 5, label)
        painter.setBrush(Qt.BrushStyle.NoBrush)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.GlobalColor.black, 2))
        painter.setFont(QFont("Arial", 10))

        bx = {
            'battery_pos': (100, 220),
            'resistor3': (250, 220),

            'switch2': (250, 120),
            'resistor1': (370, 120),

            'switch3': (250, 320),
            'resistor2': (370, 320),

            'transistor1': (500, 170),
            'transistor2': (500, 270),

            'led': (650, 200),
            'battery_neg': (650, 420)
        }

        # Draw components
        self.draw_block(painter, *bx['battery_pos'], 100, 40, "Battery (+)")
        self.draw_block(painter, *bx['resistor3'], 100, 40, "Resistor 3")

        self.draw_block(painter, *bx['switch2'], 100, 40, "Switch 2A", "lightgreen" if self.switch2_on else "lightgray")
        self.draw_block(painter, *bx['resistor1'], 100, 40, "Resistor 1")

        self.draw_block(painter, *bx['switch3'], 100, 40, "Switch 3B", "lightgreen" if self.switch3_on else "lightgray")
        self.draw_block(painter, *bx['resistor2'], 100, 40, "Resistor 2")

        self.draw_block(painter, *bx['transistor1'], 100, 60, "Transistor 1")
        self.draw_block(painter, *bx['transistor2'], 100, 60, "Transistor 2")

        led_color = "lightgray" if self.switch2_on or self.switch3_on else "yellow"
        self.draw_block(painter, *bx['led'], 100, 40, "LED", led_color)

        self.draw_block(painter, *bx['battery_neg'], 100, 40, "Battery (−)")
        # X-axis
        painter.drawLine(0, 300, self.width(), 300)
        painter.drawText(self.width() - 60, 295, "X →")

# Y-axis
        painter.drawLine(50, 0, 50, self.height())
        painter.drawText(10, 20, "↑ Y")

# Optional: tick marks on axes
        for x in range(100, self.width(), 100):
            painter.drawLine(x, 295, x, 305)
            painter.drawText(x - 10, 290, str(x))

        for y in range(100, self.height(), 100):
            painter.drawLine(45, y, 55, y)
            painter.drawText(10, y + 5, str(y))
        # Wiring
        def line(x1, y1, x2, y2):
            painter.drawLine(x1, y1, x2, y2)

        def line(x1, y1, x2, y2):
            painter.drawLine(x1, y1, x2, y2)

        # Battery (+) to Resistor3 (separated cleanly)
        line(200, 240, 250, 240)

        # Junction: from Resistor3 to right and up/down
        line(300, 220, 300, 160)  # up
        line(300, 220, 300, 320) # down

        # Switch 2A branch
        line(350, 140, 360, 140)
        line(350, 140, 370, 140)
        line(470, 140, 470, 190)
        line(470, 190, 500, 190)  # to Transistor1 Base

        # Switch 3B branch
        line(350, 340, 360, 340)
        line(350, 340, 370, 340)
        line(470, 340, 470, 190)  # merge to same base

        # Resistor3 straight to Transistor2 Base
        line(350, 240, 470, 240)
        line(470, 240, 550, 240)
        line(550, 240, 550, 270)

        # Transistor 1 Collector to LED
        line(600, 170, 600, 200)
        line(600, 200, 650, 200)

        # Transistor 2 Collector to LED (via vertical to same Y)
        line(600, 270, 600, 200)

        # LED to Battery (−)
        line(750, 220, 750, 440)
        line(600, 440, 650, 440)

        # Emitters to Ground
        line(600, 230, 600, 440)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = NorGateCircuit()
    win.show()
    sys.exit(app.exec())
