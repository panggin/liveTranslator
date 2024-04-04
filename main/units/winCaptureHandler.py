import sys
sys.path.append("main/units/windowCapture.py")

from PyQt5.QtCore import QEvent, Qt, QPoint, QRect
import cv2 as cv
from time import time

from windowCapture import WindowCapture


class WindowCaptureHandler:

    # properties
    wincap = None # 화면 캡처 객체
    wincap_rect = None # 캡처 대상 화면 크기
    enable_capture_show = True # 화면 확인 가능 여부(디버깅)

    capture_rect = None # 캡처할 영역 크기
    capture_x = 0
    capture_y = 0
    capture_width = 0
    capture_height = 0

    def __init__(self, given_window_name=None):
        self.wincap = WindowCapture(given_window_name)
        self.wincap_rect = self.get_full_window_rect()


    def run_capture(self, selectionRect):
        # loop_time = time() # debugging
        # selectionRect = QRect(706,303,631,362)
        self.set_capture_rect(selectionRect)

        while True:
            # screenshot = self.wincap.get_image_from_window()
            screenshot = self.get_crop_image_from_window()

            if self.enable_capture_show :
                cv.imshow('Window capture', screenshot) # 화면 확인

            # debug the loop rate
            # print('FPS {}'.format(1 / (time() - loop_time))) # debugging
            # loop_time = time() # debugging

            if cv.waitKey(1) == ord('q'):
                self.enable_capture_show = False
                cv.destroyAllWindows()
                # break
            
    def get_full_window_rect(self):
        return QRect(self.wincap.window_x, self.wincap.window_y, 
                     self.wincap.window_width, self.wincap.window_height)

    def set_capture_rect(self, selectionRect):
        self.capture_rect = selectionRect

        self.capture_x = selectionRect.x() - self.wincap.window_x
        self.capture_y = selectionRect.y() - self.wincap.window_y
        self.capture_width = selectionRect.width()
        self.capture_height = selectionRect.height()

    def get_crop_image_from_window(self):
        screenshot = self.wincap.get_image_from_window()        
        return screenshot[self.capture_y:self.capture_y+self.capture_height, 
                          self.capture_x:self.capture_x+self.capture_width]
