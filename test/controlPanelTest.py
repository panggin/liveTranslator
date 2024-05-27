import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, QTimer, pyqtSignal, pyqtSlot
from time import sleep

from path_liveTranslator import *
from main.liveTranslator.overlay import ControlPanel
from main.liveTranslator.overlay import StyleSheet


class SignalEmit(QObject):
    fKeyPressedToCtrl = pyqtSignal() # F키가 눌렸음을 알리는 시그널

    def emit_fKeyPressedToCtrl(self):
        QTimer.singleShot(1000, self.fKeyPressedToCtrl.emit)
        print('Key F signal emit')
        

class ControlPanelForDebug(ControlPanel):
    def __init__(self):
        super().__init__()

    @pyqtSlot()
    def overlayTextInfoUI(self):
        print('Key F signal get')
        super().overlayTextInfoUI()

    def set_text_size(self):
        super().set_text_size()
        print(f'user input : {self.userInput}')
        print(f'default_style : {StyleSheet.default_style}')
        print(f'transparent_style : {StyleSheet.transparent_style}')

    def set_color(self, target):
        super().set_color(target)
        print(f'user input : {self.color.getRgb()}')
        print(f'default_style : {StyleSheet.default_style}')
        print(f'transparent_style : {StyleSheet.transparent_style}')



if __name__ == '__main__':
    print(sys.path)
    app = QApplication(sys.argv)

    # 테스트할 객체 생성
    controlPanel = ControlPanelForDebug()
    # controlPanel = ControlPanel()
    controlPanel.show()

    # 시그널 객체 생성
    signalEmit = SignalEmit()
    signalEmit.fKeyPressedToCtrl.connect(controlPanel.overlayTextInfoUI)

    # 메인 로직
    windowName = controlPanel.get_user_input()
    print(f'window name : {windowName}')
    signalEmit.emit_fKeyPressedToCtrl()
    sys.exit(app.exec_())