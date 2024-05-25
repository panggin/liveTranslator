# debug_wincapHandler.py

from PyQt5.QtCore import pyqtSignal, pyqtSlot
import cv2 as cv
from time import time
from numpy import ndarray
from typing import Optional

from .wincapHandler import WindowCaptureHandler


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

