import sys
from PyQt5.QtCore import QRect, QEvent, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication

from path_liveTranslator import * # liveTranslator 프로젝트 path 추가
from liveTranslator import *


# LiveTranslator 프로그램 실행
if __name__ == '__main__':
    print(sys.path, '\n') # debug
    
    app = QApplication(sys.argv)    

    # 컨트롤 패널 객체 생성 및 화면에 배치
    controlPanelWin = control.ControlPanel()
    controlPanelWin.show()

    # 소스 화면 입력 및 화면 캡처 객체 생성
    windowName = controlPanelWin.get_user_input()
    wincapHandlerWin = capture.WindowCaptureHandler(windowName)

    # 소스 화면 크기 가져오기
    winFullRect = wincapHandlerWin.get_full_window_rect()

    # 오버레이 자막 객체 생성 및 화면 크기 설정
    overlayWin = overlay.OverlayTextWin()
    overlayWin.setLimitRect(winFullRect)
    overlayWin.show()

    # 시그널 연결
    print('main >>> signal connect') # debug
    
    overlayWin.fKeyPressedToCap.connect(wincapHandlerWin.start_capture)
    overlayWin.fKeyPressedToCtrl.connect(controlPanelWin.overlayTextInfoUI)
    overlayWin.applicationQuit.connect(wincapHandlerWin.quit_thread)

    controlPanelWin.styleSheetUpdated.connect(overlayWin.updateOverlayStyle)
    controlPanelWin.applicationQuit.connect(wincapHandlerWin.quit_thread)

    wincapHandlerWin.transText.connect(overlayWin.updateLabelText)

    sys.exit(app.exec_())

