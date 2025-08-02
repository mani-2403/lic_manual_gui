from PyQt6.QtWidgets import QApplication, QWidget, QPushButton
from PyQt6.QtGui import QPainter, QColor, QPen, QFont
from PyQt6.QtCore import Qt
import sys

class XnorGateCircuit(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transistor XNOR Gate Circuit")
        self.setGeometry(100, 100, 1200, 600)

        self.switch1_on = False  # Power
        self.switch2_on = False  # Input A
        self.switch3_on = False  # Input B

        # Buttons
        self.s1_btn = QPushButton("Switch 1 OFF", self)
        self.s1_btn.setGeometry(50, 40, 150, 40)
        self.s1_btn.clicked.connect(self.toggle_s1)

        self.s2_btn = QPushButton("Switch 2A OFF", self)
        self.s2_btn.setGeometry(50, 90, 150, 40)
        self.s2_btn.clicked.connect(self.toggle_s2)

        self.s3_btn = QPushButton("Switch 3B OFF", self)
        self.s3_btn.setGeometry(50, 140, 150, 40)
        self.s3_btn.clicked.connect(self.toggle_s3)

    def toggle_s1(self):
        self.switch1_on = not self.switch1_on
        self.s1_btn.setText(f"Switch 1 {'ON' if self.switch1_on else 'OFF'}")
        self.update()

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

        # Block positions
        bx = {
            'battery_pos': (150, 200),
            'switch1': (300, 200),
            'resistor3': (450, 200),

            'switch2': (300, 100),
            'resistor1': (450, 100),

            'switch3': (300, 300),
            'resistor2': (450, 300),

            'transistor1': (600, 180),  # A path
            'transistor2': (600, 240),  # B path

            'led': (750, 210),
            'battery_neg': (900, 350)
        }

        # XNOR logic
        xnor_on = self.switch1_on and (
            (self.switch2_on and self.switch3_on) or
            (not self.switch2_on and not self.switch3_on)
        )

        # Components
        self.draw_block(painter, *bx['battery_pos'], 100, 40, "Battery (+)")
        self.draw_block(painter, *bx['switch1'], 100, 40, "Switch 1", "lightgreen" if self.switch1_on else "lightgray")
        self.draw_block(painter, *bx['resistor3'], 100, 40, "Resistor 3")

        self.draw_block(painter, *bx['switch2'], 100, 40, "Switch 2A", "lightgreen" if self.switch2_on else "lightgray")
        self.draw_block(painter, *bx['resistor1'], 100, 40, "Resistor 1")

        self.draw_block(painter, *bx['switch3'], 100, 40, "Switch 3B", "lightgreen" if self.switch3_on else "lightgray")
        self.draw_block(painter, *bx['resistor2'], 100, 40, "Resistor 2")

        self.draw_block(painter, *bx['transistor1'], 100, 40, "Transistor A")
        self.draw_block(painter, *bx['transistor2'], 100, 40, "Transistor B")

        self.draw_block(painter, *bx['led'], 100, 40, "LED", "yellow" if xnor_on else "lightgray")
        self.draw_block(painter, *bx['battery_neg'], 100, 40, "Battery (−)")

        # Draw wiring
        def line(x1, y1, x2, y2):
            painter.drawLine(x1, y1, x2, y2)

        # Power path: Battery+ to Switch1 → Resistor3 → Split to 2 Transistors
        line(250, 220, 300, 220)  # Battery+ to Switch1
        line(400, 220, 450, 220)  # Switch1 to Resistor3
        line(550, 200, 600, 200)  # Resistor3 to middle split

        # Top: A path to Transistor A
        line(350, 200, 350, 140)
        line(400, 120, 450, 120)
        line(550, 120, 650, 120)
        line(650, 120, 650, 180)

        # Bottom: B path to Transistor B
        line(350, 240, 350, 300)
        line(400, 320, 450, 320)
        line(550, 320, 650, 320)
        line(650, 320, 650, 280)

        # Transistor A emitter to LED
        line(700, 220, 750, 220)

        # Transistor B emitter to LED
        line(700, 240, 750, 240)

        # LED to Battery−
        line(850, 240, 900, 240)
        line(900, 240, 900, 370)

        # Axes (same X-Y layout)
        painter.setPen(QPen(Qt.GlobalColor.darkGray, 1, Qt.PenStyle.DashLine))
        painter.drawLine(0, 300, self.width(), 300)
        painter.drawText(self.width() - 60, 295, "X →")

        painter.drawLine(50, 0, 50, self.height())
        painter.drawText(10, 20, "↑ Y")

        for x in range(100, self.width(), 100):
            painter.drawLine(x, 295, x, 305)
            painter.drawText(x - 10, 290, str(x))

        for y in range(100, self.height(), 100):
            painter.drawLine(45, y, 55, y)
            painter.drawText(10, y + 5, str(y))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = XnorGateCircuit()
    win.show()
    sys.exit(app.exec())
