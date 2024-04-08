import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import QEvent, QObject, Qt, QPoint, QRect, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPainter, QPen

from .overlayStyle import *

class SelectionArea(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initFlag()
        self.initRectAndPos()
        self.initUI()

    def initFlag(self):
        self.dragging = False  # 드래그 중인지 여부를 나타내는 플래그
        self.enable_drawing = True # 범위 지정이 가능한지 여부를 나타내는 플래그

    def initRectAndPos(self):
        # 화면 정보
        self.limit_rect = QApplication.desktop().availableGeometry() # 선택 가능 범위
        self.label_rect = None # 라벨 위치 정보

        # 드래그 위치 정보
        self.start_pos = None  # 드래그 시작 위치를 저장하는 변수
        self.end_pos = None  # 드래그 끝 위치를 저장하는 변수

    def initUI(self):
        self.setWindowTitle("Overlay Window")

        # 윈도우의 특성 설정 (오버레이 창)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # 오버레이 창에 표시할 라벨 추가
        self.label = QLabel(None, self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet(default_style)
        self.label.setText("Set window position by dragging")

        # 오버레이 창 위치 및 크기 설정
        self.setLabelGeometryWithGlobalRect(self.limit_rect)

        # 이벤트 필터 등록
        self.installEventFilter(self)


    def paintEvent(self, event):
        # 드래그 중인 경우에만 사각형을 그립니다.
        if self.enable_drawing and self.dragging:
            painter = QPainter(self)
            painter.setPen(QPen(Qt.green, 3, Qt.SolidLine))
            rect = QRect(self.start_pos, self.end_pos)
            painter.drawRect(rect)

    # 마우스 클릭 이벤트 처리
    def mousePressEvent(self, event):
        if self.enable_drawing and event.buttons() == Qt.LeftButton:
            self.dragging = True
            self.start_pos = event.pos()
            self.end_pos = event.pos()

    # 마우스 이동 이벤트 처리
    def mouseMoveEvent(self, event):
        if self.enable_drawing and self.dragging:
            currPos = event.pos()
            if 0 <= currPos.x() <= self.limit_rect.width(): # 드래그 가능 범위 확인 (x)
                self.end_pos.setX(currPos.x())
            if 0 <= currPos.y() <= self.limit_rect.height(): # 드래그 가능 범위 확인 (y)
                self.end_pos.setY(currPos.y())
            self.update()

    # 마우스 릴리스 이벤트 처리
    def mouseReleaseEvent(self, event):
        if self.enable_drawing and event.button() == Qt.LeftButton:
            self.dragging = False

        # 직사각형으로 범위 지정됨
        if (self.enable_drawing and event.button() == Qt.LeftButton
            and self.start_pos != self.end_pos):
            self.enable_drawing = False
            
            self.start_pos = self.mapToGlobal(self.start_pos)
            self.end_pos = self.mapToGlobal(self.end_pos)
            startPos, endPos = QPoint(self.start_pos), QPoint(self.end_pos)

            # 시작점을 왼쪽 위, 끝점을 오른쪽 아래로 지정
            if startPos.x() > endPos.x():
                self.start_pos.setX(endPos.x())
                self.end_pos.setX(startPos.x())

            if startPos.y() > endPos.y():
                self.start_pos.setY(endPos.y())
                self.end_pos.setY(startPos.y())

            self.setLabelGeometryWithGlobalRect(QRect(self.start_pos, self.end_pos))
            self.label.setText("This is selection area")

        self.resetDragInfo()

    # 이벤트 필터
    def eventFilter(self, obj, event):
        # R키가 눌렸을 때 선택 영역 지정 초기화
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_R:
            self.initFlag()
            self.initRectAndPos()
            self.setLabelGeometryWithGlobalRect(self.limit_rect)
        return False
    
    def getLabelRect(self):
        return self.label_rect

    def setLabelGeometryWithGlobalRect(self, posRect):
        self.setGeometry(posRect)
        self.label.setGeometry(0, 0, abs(posRect.width()), abs(posRect.height()))
        self.label_rect = self.frameGeometry()

        # print('window : ', self.frameGeometry()) #
        # print('label : ', self.label.frameGeometry()) #

        self.update()

    def resetDragInfo(self):
        self.start_pos = None
        self.end_pos = None

    
    
    
    # 디버깅 함수
    def printDragPos(self, statusText):
        print("----------------------------")
        print(f'{statusText} - start_pos : {self.start_pos}')
        print(f'{statusText} - end_pos : {self.end_pos}')
        print("----------------------------")

    def printFlags(self, statusText="result"):
        print("----------------------------")
        print(f'{statusText} - dragging : {self.dragging}')
        print(f'{statusText} - drawing : {self.enable_drawing}')
        print("----------------------------")

# --------------------------------------------
# 디버깅을 위한 함수
# if __name__ == "__main__":
#     app = QApplication(sys.argv)    
    
#     overlay = SelectionArea()
#     overlay.show()

#     sys.exit(app.exec_())
