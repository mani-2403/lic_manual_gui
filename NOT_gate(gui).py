from PyQt6.QtWidgets import QApplication, QWidget, QPushButton
from PyQt6.QtGui import QPainter, QColor, QPen, QFont
from PyQt6.QtCore import Qt
import sys

class NotGateCircuit(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transistor NOT Gate - Perfectly Aligned Closed Loop")
        self.setGeometry(100, 100, 1100, 600)

        self.switch1_on = False
        self.switch2_on = False

        # Switch Buttons
        self.s1_btn = QPushButton("Switch 1 OFF", self)
        self.s1_btn.setGeometry(50, 50, 150, 40)
        self.s1_btn.clicked.connect(self.toggle_s1)

        self.s2_btn = QPushButton("Switch 2A OFF", self)
        self.s2_btn.setGeometry(50, 100, 150, 40)
        self.s2_btn.clicked.connect(self.toggle_s2)

    def toggle_s1(self):
        self.switch1_on = not self.switch1_on
        self.s1_btn.setText(f"Switch 1 {'ON' if self.switch1_on else 'OFF'}")
        self.update()

    def toggle_s2(self):
        self.switch2_on = not self.switch2_on
        self.s2_btn.setText(f"Switch 2A {'ON' if self.switch2_on else 'OFF'}")
        self.update()

    def draw_block(self, painter, x, y, w, h, label, color=Qt.GlobalColor.white):
        painter.setBrush(QColor(color))
        painter.drawRect(x, y, w, h)
        painter.drawText(x + 8, y + h // 2 + 5, label)
        painter.setBrush(Qt.BrushStyle.NoBrush)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.GlobalColor.black, 2))
        painter.setFont(QFont("Arial",10))

        # X, Y coordinates (perfect alignment)
        bx = {
            'battery_pos': (150, 250),
            'switch1':     (300, 250),
            'switch2':     (450, 250),
            'resistor2':   (600, 250),
            'transistor':  (750, 300),  # Base down at 280
            'resistor1':   (750, 150),
            'led':         (900, 150),
            'battery_neg': (750, 400)
        }

        # Draw components
        self.draw_block(painter, *bx['battery_pos'], 100, 40, "Battery (+)")
        self.draw_block(painter, *bx['switch1'], 100, 40, "Switch 1", "lightgreen" if self.switch1_on else "lightgray")
        self.draw_block(painter, *bx['switch2'], 100, 40, "Switch 2A", "lightgreen" if self.switch2_on else "lightgray")
        self.draw_block(painter, *bx['resistor2'], 100, 40, "Resistor 2")
        self.draw_block(painter, *bx['transistor'], 100, 60, "Transistor\nNPN")
        self.draw_block(painter, *bx['resistor1'], 100, 40, "Resistor 1")
        
        led_color = "yellow" if not (self.switch1_on and self.switch2_on) else "lightgray"
        self.draw_block(painter, *bx['led'], 100, 40, "LED", led_color)
        self.draw_block(painter, *bx['battery_neg'], 100, 40, "Battery (−)")

        def line(x1, y1, x2, y2):
            painter.drawLine(x1, y1, x2, y2)

        # Perfectly aligned closed loop wires

        # Battery (+) to Switch 1
        line(250, 270, 300, 270)

        # Switch 1 to Switch 2A
        line(400, 270, 450, 270)

        # Switch 2A to Resistor 2
        line(550, 270, 600, 270)

        # Resistor 2 to Transistor Base (center)
        line(700, 270, 750, 330)

        # Collector (top center of transistor) to Resistor 1
        line(800, 300, 800, 190)

        # Resistor 1 to LED
        line(850, 170, 900, 170)

        # LED to Battery (−) via Transistor Emitter
        line(1000, 170, 1000, 390)   # Down from LED
        line(1000, 390, 800, 390)    # Left to emitter path
        line(800, 360, 800, 390)     # Down from emitter to path
        line(800, 390, 800, 400)    # Left to Battery (−)

    # Result: fully closed, aligned NOT gate loop

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = NotGateCircuit()
    win.show()
    sys.exit(app.exec())
