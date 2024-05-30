# wincapHandler.py

from PyQt5.QtCore import QRect, QThread, pyqtSignal, pyqtSlot
from numpy import ndarray
from typing import Optional

from .wincap import WindowCapture
from .textProcessor import LANG, TextProcessor


class WindowCaptureHandler(QThread):
    transText = pyqtSignal(str) # 추출된 텍스트를 번역하여 전달

    wincap = None # 화면 캡처 객체
    wincap_rect = None # 캡처 대상 화면 크기

    capture_rect = None # 캡처할 영역 크기
    capture_x = 0
    capture_y = 0
    capture_width = 0
    capture_height = 0

    def __init__(self, given_window_name:Optional[str]=None):
        super().__init__()
        self.wincap = WindowCapture(given_window_name)
        self.wincap_rect = self.get_full_window_rect()
        self.textProcessor = TextProcessor(LANG.ENG)

        self.threadRunning = False # 스레드 실행을 위한 플래그

        print('capture >>> init WindowCaptureHandler') # debug


# --------- 메인 로직 --------------
    @pyqtSlot(QRect)
    def start_capture(self, selectionRect:QRect):
        print('capture >>> capture thread started') # debug

        self.set_capture_rect(selectionRect)
        self.threadRunning = True
        self.start() # 아래 백그라운드 작업(run) 실행

    # 백그라운드 작업 - 실시간 캡처와 텍스트 추출 및 번역
    def run(self):
        while self.threadRunning:
            # print('capture >>> capture thread is running...') # debug
            screenshot = self.get_crop_image_from_window()
            text = self.textProcessor.emit_translated_text(screenshot)

            if text == '': continue
            self.transText.emit(text)

    # 시그널 전달 받을 경우 스레드 종료
    @pyqtSlot()
    def quit_thread(self):
        print('capture >> applicationQuit signal received') # debug
        print('capture >> thread quit') # debug
        self.threadRunning = False
        self.quit()
        self.wait()

# --------- 서브 로직 --------------
    def set_capture_rect(self, selectionRect:QRect):
        self.capture_rect = selectionRect

        self.capture_x = selectionRect.x() - self.wincap.window_x
        self.capture_y = selectionRect.y() - self.wincap.window_y
        self.capture_width = selectionRect.width()
        self.capture_height = selectionRect.height()

    def get_full_window_rect(self) -> QRect:
        return QRect(self.wincap.window_x, self.wincap.window_y, 
                     self.wincap.window_width, self.wincap.window_height)

    def get_crop_image_from_window(self) -> ndarray:
        screenshot = self.wincap.get_image_from_window()        
        return screenshot[self.capture_y:self.capture_y+self.capture_height, 
                          self.capture_x:self.capture_x+self.capture_width]


