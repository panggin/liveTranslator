# test/0_overlayRangeWin_test.py <- liveTranslator/overlay/overlayRangeWin.py

import sys
from PyQt5.QtWidgets import QApplication

from path_liveTranslator import *
from main.liveTranslator.overlay import OverlayRangeWin


class OverlayRangeWinForDebug(OverlayRangeWin):
    
    def __init__(self):
        super().__init__()

    def initRectAndPos(self):
        if self.enable_drawing :
            super().initRectAndPos()
            print(f'limit_rect : {self.limit_rect}')

    def mousePressEvent(self, event):
        if self.enable_drawing :
            super().mousePressEvent(event)
            print(f'start_pos : {self.mapToGlobal(self.start_pos)}')

    def mouseMoveEvent(self, event):
        if self.enable_drawing :
            super().mouseMoveEvent(event)
            print(f'start_pos : {self.mapToGlobal(self.start_pos)} / end_pos : {self.mapToGlobal(self.start_pos)}')
    
    def mouseReleaseEvent(self, event):
        if self.enable_drawing :
            print(f'start_pos : {self.mapToGlobal(self.start_pos)} / end_pos : {self.mapToGlobal(self.start_pos)}')
            super().mouseReleaseEvent(event)
            print(f'label_rect : {self.label_rect}')


if __name__ == '__main__':
    print(sys.path)
    
    app = QApplication(sys.argv)    

    overlay = OverlayRangeWinForDebug()
    # overlay = OverlayRangeWin()
    overlay.show()

    sys.exit(app.exec_())