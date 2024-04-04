import sys

import cv2 as cv
from time import time
from threading import *
import numpy as np
import Quartz as QZ
from queue import Queue

from PyQt5.QtCore import QRect, QEvent
from PyQt5.QtWidgets import QApplication

from units.textOverlayWindow import TextOverlayWindow
from units.winCaptureHandler import WindowCaptureHandler 


if __name__ == "__main__":

    app = QApplication(sys.argv)

    wincapHandler = WindowCaptureHandler('Google')  # 캡쳐할 창의 이름 넣기
    overlay = TextOverlayWindow()

    # 타겟 화면 크기 가져오기
    winFullRect = wincapHandler.get_full_window_rect()
    
    # 오버레이 화면 크기 설정 및 실행
    overlay.setLimitRect(winFullRect)
    overlay.show()

    overlay.fKeyPressed.connect(wincapHandler.run_capture)

    sys.exit(app.exec_())