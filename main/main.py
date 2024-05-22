import sys

import cv2 as cv
from time import time
import numpy as np
import Quartz as QZ
from queue import Queue

from PyQt5.QtCore import QRect, QEvent, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication

from liveTranslator.overlay.infoWindow import InfoWindow 
from liveTranslator.overlay.textOverlayWindow import TextOverlayWindow
from liveTranslator.capture.wincapHandler import WindowCaptureHandler 

from liveTranslator.capture.debug_wincapHandler import WindowCaptureHandlerForDebug # 디버깅

from liveTranslator.overlay._emitTextThread import MyWindow, TextUpdateThread # 기능 테스트를 위한 일시적 추가


app = QApplication(sys.argv)

infoWindow = InfoWindow()
infoWindow.show()

windowName = infoWindow.get_text()
# windowName = 'Google' # 디버깅 - 캡처할 창 이름 Google로 지정
# wincapHandler = WindowCaptureHandler(windowName)  # 캡쳐할 창의 이름 넣기
wincapHandler = WindowCaptureHandlerForDebug(windowName) # 디버깅을 위한 WindowCaptureHandler
overlay = TextOverlayWindow()

# 타겟 화면 크기 가져오기
winFullRect = wincapHandler.get_full_window_rect()

# 오버레이 화면 크기 설정 및 실행
overlay.setLimitRect(winFullRect)
overlay.show()

overlay.fKeyPressedToCap.connect(wincapHandler.start_capture) # F키 눌렀을 때 화면 캡처 시작
overlay.fKeyPressedToInfo.connect(infoWindow.capInfoUI)

infoWindow.styleSheetUpdated.connect(overlay.updateOverlay)
wincapHandler.transText.connect(overlay.setLabelText) # 번역된 텍스트로 라벨 텍스트 설정
print('After Connect')

sys.exit(app.exec_())

