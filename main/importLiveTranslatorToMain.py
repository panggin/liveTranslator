## 메인 함수에서 liveTranslator를 사용할 수 있도록 import 문 작성

from liveTranslator.overlay.controlPanel import ControlPanel
from liveTranslator.overlay.overlayTextWin import OverlayTextWin

from liveTranslator.capture.wincapHandler import WindowCaptureHandler 

# 디버깅 시 활성화하여 테스트
from liveTranslator.capture.debug_wincapHandler import WindowCaptureHandlerForDebug # 디버깅

# from liveTranslator.overlay.test_emitTextThread import MyWindow, TextUpdateThread # 기능 테스트를 위한 일시적 추가