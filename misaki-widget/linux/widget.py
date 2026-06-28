import sys
import configparser
import os
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import QTimer, Qt, QRect
from PyQt6.QtGui import QPixmap, QPainter, QFont, QFontDatabase, QColor, QGuiApplication
from datetime import datetime

# SCRIPT'İN OLDUĞU KLASÖRÜ BUL (DAĞITIM İÇİN EN ÖNEMLİ KISIM)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class MisakiWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        # 1. Ekran ve Ayar Okuma
        screen = QGuiApplication.primaryScreen().geometry()
        screen_w, screen_h = screen.width(), screen.height()
        
        # Dosya yollarını BASE_DIR ile birleştiriyoruz
        config_path = os.path.join(BASE_DIR, 'config.ini')
        config = configparser.ConfigParser()
        config.read(config_path)
        
        w_config = config.get('Settings', 'width', fallback='auto')
        self.panel_h = int(config.get('Settings', 'panel_height', fallback=40))
        self.text_hex = config.get('Settings', 'text_color', fallback='#000000')
        self.debug = config.getboolean('Settings', 'debug', fallback=False)
        self.box_x = float(config.get('Settings', 'box_x', fallback=0.05))
        self.box_y = float(config.get('Settings', 'box_y', fallback=0.35))
        self.box_w = float(config.get('Settings', 'box_width', fallback=0.40))
        self.box_h = float(config.get('Settings', 'box_height', fallback=0.40))
        
        if w_config == 'auto':
            self.target_width = int(screen_w * 0.20)
        else:
            self.target_width = int(w_config)
            
        # 2. Görsel ve Font (Yine BASE_DIR kullanarak)
        font_path = os.path.join(BASE_DIR, "Cause-Light.ttf")
        img_path = os.path.join(BASE_DIR, "misaki.png")
        
        self.font_family = "Arial"
        if os.path.exists(font_path):
            fid = QFontDatabase.addApplicationFont(font_path)
            fams = QFontDatabase.applicationFontFamilies(fid)
            if fams: self.font_family = fams[0]
        
        self.pixmap = QPixmap(img_path)
        self.display_pixmap = self.pixmap.scaledToWidth(self.target_width, Qt.TransformationMode.SmoothTransformation)
        self.setFixedSize(self.display_pixmap.width(), self.display_pixmap.height())
        
        # 3. Konumlandırma
        x_cfg = config.get('Settings', 'x_position', fallback='auto')
        y_cfg = config.get('Settings', 'y_position', fallback='auto')
        
        final_x = int(x_cfg) if x_cfg != 'auto' else (screen_w - self.width() - 20)
        final_y = int(y_cfg) if y_cfg != 'auto' else (screen_h - self.height() - self.panel_h)
        
        self.move(final_x, final_y)
        
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnBottomHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_X11NetWmWindowTypeDesktop)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.display_pixmap)
        
        w, h = self.width(), self.height()
        box_rect = QRect(int(w * self.box_x), int(h * self.box_y), int(w * self.box_w), int(h * self.box_h))
        
        if self.debug:
            painter.setPen(QColor("#FF0000"))
            painter.drawRect(box_rect)
            
        now = datetime.now()
        text = now.strftime("%d %B\n%A\n%H:%M")
        
        font_size = int(w / 14) 
        painter.setFont(QFont(self.font_family, font_size, QFont.Weight.Bold))
        painter.setPen(QColor(self.text_hex))
        painter.drawText(box_rect, Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap, text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MisakiWidget()
    widget.show()
    sys.exit(app.exec())