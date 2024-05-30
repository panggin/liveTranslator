# test/1_overlayTextWin_controlPanel_test.py 
# <- liveTranslator/overlay/overlayTextWin.py + liveTranslator/control/controlPanel.py

import sys
import time
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QObject, QThread, QRect, QEvent, pyqtSignal, pyqtSlot

from path_liveTranslator import *
from main.liveTranslator.control import ControlPanel
from main.liveTranslator.overlay import OverlayTextWin


# WindowCaptureHandler를 대신하는 클래스
class WincapSignalHandler(QThread):
    transText = pyqtSignal(str) # 오버레이 창에 배치될 텍스트 전달 시그널

    def __init__(self):
        super().__init__()
        self.transTextList = ['Hello', 'World', 'Python', 'Overlay', 'Text', 'Window']

    def run(self):
        self.emitTransText()

    @pyqtSlot(QRect)
    def fKeySignalToCapReceiver(self, wincap_rect:QRect):
        print(f'F key signal to capture window received : {wincap_rect}')
        self.start()

    def emitTransText(self):
        for text in self.transTextList:
            print(f'Translated text emit : {text}')
            self.transText.emit(text)
            time.sleep(2)
        
#-------------------------------------------------------------

# ControlPanel 객체와 OverlayTextWin 객체의 상호작용 확인
if __name__ == '__main__':
    print(sys.path)
    
    app = QApplication(sys.argv)

    controlPanel = ControlPanel() # control
    controlPanel.show()

    window_name = controlPanel.get_user_input()
    print(f'user input : {window_name}')

    limitRect = QRect(310, 78, 1199, 626)
    overlay = OverlayTextWin(limitRect) # overlay
    overlay.show()

    wincapSignalHandler = WincapSignalHandler() # capture

    # 시그널 연결
    overlay.fKeyPressedToCap.connect(wincapSignalHandler.fKeySignalToCapReceiver)
    overlay.fKeyPressedToCtrl.connect(controlPanel.overlayTextInfoUI)
    
    controlPanel.styleSheetUpdated.connect(overlay.updateOverlayStyle)

    wincapSignalHandler.transText.connect(overlay.updateLabelText)

    sys.exit(app.exec_())