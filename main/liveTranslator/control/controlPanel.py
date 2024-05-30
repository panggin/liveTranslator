# liveTranslator/overlay/controlPanel.py

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QInputDialog, QColorDialog
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt

from ..overlay.overlayStyle import Color, StyleSheet


class ControlPanel(QWidget):
    styleSheetUpdated = pyqtSignal()  # 스타일 변경을 알리는 시그널
    applicationQuit = pyqtSignal()    # 프로그램 종료를 알리는 시그널

    def __init__(self):
        super().__init__()
        self.userInput = None # 사용자로부터 받은 입력값
        self.setWindowTitle('컨트롤 패널')
        self.setGeometry(0, 0, 200, 100) # 컨트롤 패널 크기 설정
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        print('control >>> init ControlPanel') # debug

        self.initUI()
        self.set_window_name()


    def initUI(self):
        # 수직 레이아웃 생성
        self.layout = QVBoxLayout()

        #-------------- 1. 캡처 영역 선택 시 표시될 화면 --------------------

        # 첫 번째 레이블 생성 및 레이아웃에 추가
        self.label1 = QLabel('R : 선택 영역 재설정')
        self.layout.addWidget(self.label1)

        # 두 번째 레이블 생성 및 레이아웃에 추가
        self.label2 = QLabel('F : 선택 영역의 화면 캡처 진행')
        self.layout.addWidget(self.label2)

        #-------------- 2. 번역 자막 배치 시 표시될 화면 --------------------

        # 텍스트 크기 변경 버튼 생성 및 레이아웃에 추가
        self.button1 = QPushButton('텍스트 크기 변경')
        self.button1.clicked.connect(self.set_text_size)
        self.layout.addWidget(self.button1)

        # 텍스트 색상 변경 버튼 생성 및 레이아웃에 추가
        self.button2 = QPushButton('텍스트 색상 변경')
        self.button2.clicked.connect(lambda : self.set_color(StyleSheet.textColor))
        self.layout.addWidget(self.button2)

        # 배경 색상 변경 버튼 생성 및 레이아웃에 추가
        self.button3 = QPushButton('배경 색상 변경')
        self.button3.clicked.connect(lambda : self.set_color(StyleSheet.backgroundColor))
        self.layout.addWidget(self.button3)

        # 프로그램 종료 버튼 생성 및 레이아웃에 추가
        self.button4 = QPushButton('프로그램 종료 (Q)')
        self.button4.clicked.connect(self.exit_application)
        self.layout.addWidget(self.button4)

        #-------------------------------------------------------------
        # 레이아웃 설정
        self.hideOverlayRangeInfoUI()
        self.hideOverlayTextInfoUI()
        self.setLayout(self.layout)



#-------------- 0. 화면 캡처를 진행할 창 선택 (사용자 입력) ------------

    def set_window_name(self):
        self.userInput, ok_pressed = QInputDialog.getText(self, '화면 캡처 설정', '화면 캡처할 창 이름 입력:')
        if ok_pressed: # 사용자 입력을 받았을 경우 다음 UI 화면으로 넘어감
            print('control >>> get user input') # debug
            self.overlayRangeInfoUI()


#-------------- 1. 캡처 영역 선택 시 표시될 화면 --------------------

    def overlayRangeInfoUI(self):
        self.showOverlayRangeInfoUI() # 미리 배치해둔 화면 표시

    def hideOverlayRangeInfoUI(self):
        self.label1.hide()
        self.label2.hide()

    def showOverlayRangeInfoUI(self):
        self.label1.show()
        self.label2.show()


# ------------- 2. 번역 자막 배치 관련 레이아웃 ---------------------

    @pyqtSlot()
    def overlayTextInfoUI(self):
        self.hideOverlayRangeInfoUI() # 1번 화면 숨기기
        self.showOverlayTextInfoUI()  # 2번 화면 표시

    def hideOverlayTextInfoUI(self):
        self.button1.hide()
        self.button2.hide()
        self.button3.hide()
        self.button4.hide()

    def showOverlayTextInfoUI(self):
        self.button1.show()
        self.button2.show()
        self.button3.show()
        self.button4.show()

    # button1과 연결 - 텍스트 크기 변경
    def set_text_size(self):
        self.userInput, ok_pressed = QInputDialog.getInt(self, '텍스트 크기 변경', '텍스트 크기 입력:', 15, 5)
        if ok_pressed:
            print('control >>> update text size') # debug
            StyleSheet.textSize = self.userInput
            StyleSheet.update_style_sheet() # 오버레이 스타일시트 업데이트
            self.styleSheetUpdated.emit()

    # button2, button3과 연결 - 텍스트 색상 변경 / 배경 색상 변경
    def set_color(self, target:Color):
        self.color = QColorDialog.getColor() # 색상 대화 상자를 사용자로부터 색상 선택 받음

        # 사용자가 색상을 선택한 경우에만 처리
        if self.color.isValid():
            print('control >>> update color') # debug
            target.red, target.green, target.blue = self.color.red(), self.color.green(), self.color.blue()
            StyleSheet.update_style_sheet() # 오버레이 스타일시트 업데이트
            self.styleSheetUpdated.emit()

    # button4와 연결 - 프로그램 종료 시그널 전달 및 프로그램 종료
    def exit_application(self):
        print('control >>> application exit') # debug
        self.applicationQuit.emit()
        QApplication.quit()


# ------------- 클래스 외부로 데이터 전달 --------------------------

    def get_user_input(self):
        self.userInput = None if self.userInput == '' else self.userInput
        return self.userInput


