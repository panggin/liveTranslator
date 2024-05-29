# test/0_overlayTextWin_test.py <- liveTranslator/overlay/overlayTextWin.py

import sys
import time
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QObject, QThread, QTimer, QRect, QEvent, pyqtSignal, pyqtSlot

from path_liveTranslator import *
from main.liveTranslator.overlay import OverlayTextWin


# 시그널 전달을 확인하기 위한 스레드
class SignalEmit(QThread):
    transText = pyqtSignal(str)      # 오버레이 창에 배치될 텍스트 전달 시그널
    styleSheetUpdated = pyqtSignal() # 오버레이 스타일시트 변경을 알리는 시그널

    def __init__(self):
        super().__init__()
        self.transTextList = ['Hello', 'World', 'Python', 'Overlay', 'Text', 'Window']

    def run(self):
        self.emitTransText()
        self.emitStyleSheetUpdated()

    @pyqtSlot(QRect)
    def fKeySignalToCapReceiver(self, wincap_rect:QRect):
        print(f'F key signal to capture window received : {wincap_rect}')
        self.start()

    @pyqtSlot()
    def fKeySignalToCtrlReceiver(self):
        print('F key signal to control panel received')

    def emitTransText(self):
        for text in self.transTextList:
            print(f'Translated text emit : {text}')
            self.transText.emit(text)
            time.sleep(2)

    def emitStyleSheetUpdated(self):
        self.styleSheetUpdated.emit()
        
#-------------------------------------------------------------

# OverlayTextWin의 디버깅 클래스
class OverlayTextWinForDebug(OverlayTextWin):

    # 이벤트 필터 확인
    def eventFilter(self, obj:QObject, event:QEvent):

        # F키 누름 - 창 크기 고정
        if not self.lock_resize and event.type() == QEvent.KeyPress and event.key() == Qt.Key_F:
            print('Key F signal emit')
            print(f'label_rect : {self.label_rect}')

        # Q키 누름 - 프로그램 종료
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Q:
            print('Application exit')
        
        return super().eventFilter(obj, event)
    
    # 시그널 전달받음 확인
    @pyqtSlot(str) # OverlayTextWin <-- WindowCaptureHandler
    def updateLabelText(self, text:str):
        print(f'translated text signal received : {text}')
        return super().updateLabelText(text)

    @pyqtSlot()
    def updateOverlayStyle(self):
        print(f'stylesheet updated signal received')
        return super().updateOverlayStyle()


# 오버레이 창(OverlayTextWin) 동작 확인
if __name__ == '__main__':
    print(sys.path)
    
    app = QApplication(sys.argv)

    limitRect = QRect(310, 78, 1199, 626) # 클래스 생성 시 사용
    signalEmit = SignalEmit() # 텍스트 배치 확인을 위한 시그널 발생 클래스

    overlay = OverlayTextWinForDebug(limitRect)
    # overlay = OverlayTextWin(limitRect)
    overlay.show()

    # F키 시그널 전달 확인
    overlay.fKeyPressedToCap.connect(signalEmit.fKeySignalToCapReceiver)
    overlay.fKeyPressedToCtrl.connect(signalEmit.fKeySignalToCtrlReceiver)

    signalEmit.transText.connect(overlay.updateLabelText)
    signalEmit.styleSheetUpdated.connect(overlay.updateOverlayStyle)

    sys.exit(app.exec_())