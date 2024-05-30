# test/1_overlayTexteWin_wincapHandler_test.py 
# <- liveTranslator/overlay/overlayTextWin.py + liveTranslator/capture/wincapHandler.py

import sys
import time
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QObject, QThread, QRect, QEvent, pyqtSignal, pyqtSlot

from path_liveTranslator import *
from main.liveTranslator.overlay import OverlayTextWin
from main.liveTranslator.capture import WindowCaptureHandler
        
#-------------------------------------------------------------

# OverlayTextWin 객체와 WindowCaptureHandler 객체의 상호작용 확인
if __name__ == '__main__':
    print(sys.path)
    
    app = QApplication(sys.argv)

    windowName = input('캡처할 창 이름을 입력하세요 : ')
    print(f'user input : {windowName}')
    windowName = None if windowName == '' else windowName

    wincapHandler = WindowCaptureHandler(windowName) # capture
    overlay = OverlayTextWin() # overlay

    # 소스 화면 크기 가져오기
    winFullRect = wincapHandler.get_full_window_rect()

    # 캡처 영역 지정을 위한 오버레이 화면 크기 설정 및 배치
    overlay.setLimitRect(winFullRect)
    overlay.show()

    # 시그널 연결
    overlay.fKeyPressedToCap.connect(wincapHandler.start_capture)
    wincapHandler.transText.connect(overlay.updateLabelText)

    sys.exit(app.exec_())