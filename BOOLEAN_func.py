from PyQt6.QtWidgets import QApplication, QWidget, QPushButton
from PyQt6.QtGui import QPainter, QColor, QPen, QFont
from PyQt6.QtCore import Qt
import sys

class BooleanCircuitGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Boolean Function GUI - F = C’(B’ + A’D) + D’B’")
        self.setGeometry(100, 100, 1400, 700)

        self.A = False
        self.B = False
        self.C = False
        self.D = False

        self.btn_A = QPushButton("A OFF", self)
        self.btn_A.setGeometry(50, 40, 150, 40)
        self.btn_A.clicked.connect(self.toggle_A)

        self.btn_B = QPushButton("B OFF", self)
        self.btn_B.setGeometry(50, 90, 150, 40)
        self.btn_B.clicked.connect(self.toggle_B)

        self.btn_C = QPushButton("C OFF", self)
        self.btn_C.setGeometry(50, 140, 150, 40)
        self.btn_C.clicked.connect(self.toggle_C)

        self.btn_D = QPushButton("D OFF", self)
        self.btn_D.setGeometry(50, 190, 150, 40)
        self.btn_D.clicked.connect(self.toggle_D)

    def toggle_A(self):
        self.A = not self.A
        self.btn_A.setText(f"A {'ON' if self.A else 'OFF'}")
        self.update()

    def toggle_B(self):
        self.B = not self.B
        self.btn_B.setText(f"B {'ON' if self.B else 'OFF'}")
        self.update()

    def toggle_C(self):
        self.C = not self.C
        self.btn_C.setText(f"C {'ON' if self.C else 'OFF'}")
        self.update()

    def toggle_D(self):
        self.D = not self.D
        self.btn_D.setText(f"D {'ON' if self.D else 'OFF'}")
        self.update()

    def draw_block(self, painter, x, y, w, h, label, color=Qt.GlobalColor.white):
        painter.setBrush(QColor(color))
        painter.drawRect(x, y, w, h)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawText(x + 6, y + h // 2 + 5, label)

    def draw_l_line(self, painter, x1, y1, x2, y2):
        painter.setPen(QPen(Qt.GlobalColor.black, 2))
        if x1 != x2:
            painter.drawLine(x1, y1, x2, y1)  # horizontal
        if y1 != y2:
            painter.drawLine(x2, y1, x2, y2)  # vertical

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setFont(QFont("Arial", 10))

        A = int(self.A)
        B = int(self.B)
        C = int(self.C)
        D = int(self.D)

        notA = 1 - A
        notB = 1 - B
        notC = 1 - C
        notD = 1 - D

        inner1 = notB | (notA & D)
        term1 = notC & inner1
        term2 = notD & notB
        F = term1 | term2

        blocks = {
            'A': (250, 60), 'notA': (360, 60),
            'B': (250, 140), 'notB_input': (360, 140),
            'C': (250, 220), 'notC': (360, 220),
            'D': (250, 300), 'notD': (360, 300),
            'notB1': (500, 100), 'notA_and_D': (500, 180),
            'or1': (630, 140), 'term1': (760, 140),
            'notD_term2': (500, 260), 'notB2': (500, 340),
            'term2': (630, 300), 'final_or': (760, 220), 'led': (900, 220)
        }

        # Draw input and NOT blocks
        self.draw_block(painter, *blocks['A'], 80, 30, f"A = {A}", "lightgreen" if A else "lightgray")
        self.draw_block(painter, *blocks['B'], 80, 30, f"B = {B}", "lightgreen" if B else "lightgray")
        self.draw_block(painter, *blocks['C'], 80, 30, f"C = {C}", "lightgreen" if C else "lightgray")
        self.draw_block(painter, *blocks['D'], 80, 30, f"D = {D}", "lightgreen" if D else "lightgray")

        self.draw_block(painter, *blocks['notA'], 80, 30, f"¬A", "lightgreen" if notA else "lightgray")
        self.draw_block(painter, *blocks['notB_input'], 80, 30, f"¬B", "lightgreen" if notB else "lightgray")
        self.draw_block(painter, *blocks['notC'], 80, 30, f"¬C", "lightgreen" if notC else "lightgray")
        self.draw_block(painter, *blocks['notD'], 80, 30, f"¬D", "lightgreen" if notD else "lightgray")

        # Draw logic blocks
        self.draw_block(painter, *blocks['notB1'], 100, 30, "¬B")
        self.draw_block(painter, *blocks['notA_and_D'], 100, 30, "¬A · D")
        self.draw_block(painter, *blocks['or1'], 100, 30, "B′ + A′D")
        self.draw_block(painter, *blocks['term1'], 100, 30, "Term1")
        self.draw_block(painter, *blocks['notD_term2'], 100, 30, "¬D")
        self.draw_block(painter, *blocks['notB2'], 100, 30, "¬B")
        self.draw_block(painter, *blocks['term2'], 100, 30, "D′ · B′")
        self.draw_block(painter, *blocks['final_or'], 120, 30, "F = T1 + T2")
        self.draw_block(painter, *blocks['led'], 80, 30, "LED", "yellow" if F else "lightgray")
        painter.drawText(900, 210, f"F = {F}")

        # L-shaped wire connections
        def connect(label1, label2):
            x1, y1 = blocks[label1][0] + 80, blocks[label1][1] + 15
            x2, y2 = blocks[label2][0], blocks[label2][1] + 15
            self.draw_l_line(painter, x1, y1, x2, y2)

        connect('notA', 'notA_and_D')
        connect('D', 'notA_and_D')
        connect('notB_input', 'notB1')
        connect('notB1', 'or1')
        connect('notA_and_D', 'or1')
        connect('notC', 'term1')
        connect('or1', 'term1')
        connect('notD', 'notD_term2')
        connect('notB_input', 'notB2')
        connect('notD_term2', 'term2')
        connect('notB2', 'term2')
        connect('term1', 'final_or')
        connect('term2', 'final_or')
        connect('final_or', 'led')

        # Axis Grid (optional)
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
    win = BooleanCircuitGUI()
    win.show()
    sys.exit(app.exec())
