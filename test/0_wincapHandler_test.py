# test/0_wincapHandler_test.py <- liveTranslator/capture/wincapHandler.py

import cv2 as cv
from time import time
from numpy import ndarray
from typing import Optional
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QRect, QThread, pyqtSignal, pyqtSlot

from path_liveTranslator import *
from main.liveTranslator.capture import WindowCaptureHandler


class SignalHandler(QThread):
    fKeyPressedToCap = pyqtSignal(QRect)

    def __init__(self, selectionRect):
        super().__init__()
        self.selectionRect = selectionRect
        print(selectionRect)

    def emit_fKeySignal_withRect(self):
        self.fKeyPressedToCap.emit(self.selectionRect)

    @pyqtSlot(str)
    def transTextReceiver(self, text):
        print('----------- translated -----------\n')
        print(text + '\n')



class WindowCaptureHandlerForDebug(WindowCaptureHandler):
    imageEmit = pyqtSignal(ndarray)

    def __init__(self, given_window_name:Optional[str]=None):
        super().__init__(given_window_name)
        self.imageEmit.connect(self.imshowFromImageEmit)

    def run(self):
        self.loop_time = time() # init for printFPS
        while True:
            screenshot = self.get_crop_image_from_window()
            self.imageEmit.emit(screenshot)
            text = self.textProcessor.emit_translated_text(screenshot)

            if text == '': continue
            self.transText.emit(text)

            self.printTransText(text)
            self.printFPS()

    @pyqtSlot(ndarray)
    def imshowFromImageEmit(self, screenshot:ndarray):
        cv.imshow('show capture area', screenshot) # 화면 확인

    def printTransText(self, text):
        print(f'Translated Text : {text}')

    def printFPS(self):
        # debug the loop rate
        print('FPS {}'.format(1 / (time() - self.loop_time)))
        self.loop_time = time()


# 지정한 창 실시간 캡처(WindowCaptureHandler) 확인
if __name__ == '__main__':
    print(sys.path)

    app = QApplication(sys.argv)

    windowName = input('캡처할 창 이름을 입력하세요 : ')
    wincapHandler = WindowCaptureHandlerForDebug(windowName)
    signalHandler = SignalHandler(wincapHandler.wincap_rect)
    
    signalHandler.fKeyPressedToCap.connect(wincapHandler.start_capture)
    wincapHandler.transText.connect(signalHandler.transTextReceiver)

    signalHandler.emit_fKeySignal_withRect()
    
    sys.exit(app.exec_())

