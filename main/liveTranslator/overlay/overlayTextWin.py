import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, Qt, QEvent, QRect, pyqtSignal, pyqtSlot

from .overlayRangeWin import OverlayRangeWin
from .overlayStyle import *


class OverlayTextWin(OverlayRangeWin):

    fKeyPressedToCap = pyqtSignal(QRect)  # F키가 눌렸음을 화면 캡처 스레드에 알리는 시그널
    fKeyPressedToCtrl = pyqtSignal()      # F키가 눌렸음을 컨트롤 패널에 알리는 시그널
    applicationQuit = pyqtSignal()        # 프로그램 종료를 알리는 시그널

    def __init__(self, limitRect=None):
        super().__init__() # OverlayRangeWin.__init__() 호출
        self.initFlag()

        self.limit_rect = limitRect if limitRect is not None else self.limit_rect
        self.setLabelGeometryWithGlobalRect(self.limit_rect)

        print('overlay >>> init OverlayTextWindow') # debug

    def initFlag(self):
        super().initFlag()
        self.lock_resize = False # 크기 고정 여부

    #-------------------------------------------------------------

    # 마우스가 라벨에 올라갔을 때 이벤트 처리 -> 투명화
    def enterEvent(self, event):
        if self.lock_resize:
            self.label.setStyleSheet(StyleSheet.transparent_style)

    # 마우스가 라벨에서 벗어났을 때 이벤트 처리
    def leaveEvent(self, event):
        if self.lock_resize:
            self.label.setStyleSheet(StyleSheet.default_style)


    # 이벤트 필터
    def eventFilter(self, obj:QObject, event:QEvent):
        # R키 누름 - 창 크기 재조정
        if not self.lock_resize and event.type() == QEvent.KeyPress and event.key() == Qt.Key_R:
            print('overlay >>> press key R - reset overlay range') # debug
            self.initFlag() # 플래그 초기화
            self.setLabelGeometryWithGlobalRect(self.limit_rect)
            return True

        # F키 누름 - 창 크기 고정
        if not self.lock_resize and event.type() == QEvent.KeyPress and event.key() == Qt.Key_F:
            print('overlay >>> press key F - lock window size') # debug
            self.lock_resize = True
            self.enable_drawing = False

            self.label.setStyleSheet(StyleSheet.default_style)

            self.fKeyPressedToCap.emit(self.label_rect)  # 화면 캡처 스레드로 선택 범위 전달
            self.fKeyPressedToCtrl.emit()                # 컨트롤 패널로 시그널 전달
            return True

        # Q키 누름 - 프로그램 종료
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Q:
            print('overlay >>> press key Q - application exit') # debug
            self.applicationQuit.emit()
            QApplication.quit()
            return True
        
        return super().eventFilter(obj, event)

    #-------------------------------------------------------------

    def setLimitRect(self, limitRect:QRect):
        self.limit_rect = limitRect
        self.setLabelGeometryWithGlobalRect(self.limit_rect)

    def getLabelRect(self):
        labelRect = self.label_rect if self.lock_resize else None
        return labelRect
    
    @pyqtSlot(str) # OverlayTextWin <-- WindowCaptureHandler
    def updateLabelText(self, text:str):
        if text is not None:
            self.label.setText(text)

    @pyqtSlot()
    def updateOverlayStyle(self):
        self.label.setStyleSheet(StyleSheet.default_style)
    
    