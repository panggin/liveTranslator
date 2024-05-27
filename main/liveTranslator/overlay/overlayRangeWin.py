# liveTranslator/overlay/overlayRangeWin.py

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt, QEvent, QObject, QPoint, QRect
from PyQt5.QtGui import QPainter, QPen

from .overlayStyle import *


class OverlayRangeWin(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initFlag()         # 플래그 초기화
        self.initRectAndPos()   # 위치 정보 초기화
        self.initUI()           # UI 구성 초기화
        print('>>> init OverlayRangeWindow')

    def initFlag(self):
        self.dragging = False      # 드래그 중인지 확인하는 플래그
        self.enable_drawing = True # 범위 지정이 가능한 상태인지 확인하는 플래그

    def initRectAndPos(self):
        # 화면 구성 위치 정보
        self.limit_rect = QApplication.desktop().availableGeometry() # 최대 선택 가능 범위
        self.label_rect = None # 라벨 위치 정보

        # 드래그 중 위치 정보
        self.start_pos = None  # 드래그 시작 위치를 저장하는 변수
        self.end_pos = None    # 드래그 끝 위치를 저장하는 변수

    def initUI(self):
        self.setWindowTitle("Overlay Window")

        # 윈도우의 특성 설정 (오버레이 창)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # 오버레이 창에 표시할 라벨 추가 및 초기화
        self.label = QLabel(None, self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet(StyleSheet.transparent_style)

        # 오버레이 창 위치 및 크기 설정
        self.setLabelGeometryWithGlobalRect(self.limit_rect)

        # 이벤트 필터 등록
        self.installEventFilter(self)

    #-------------------------------------------------------------

    # 드래그한 선택 위치 사각형으로 표시
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
            if 0 <= currPos.x() <= self.limit_rect.width(): # 드래그 가능 범위 확인 (x 좌표)
                self.end_pos.setX(currPos.x())
            if 0 <= currPos.y() <= self.limit_rect.height(): # 드래그 가능 범위 확인 (y 좌표)
                self.end_pos.setY(currPos.y())
            self.update()

    # 마우스 릴리스 이벤트 처리
    def mouseReleaseEvent(self, event):
        if self.enable_drawing and event.button() == Qt.LeftButton:
            self.dragging = False

        # 드래그한 직사각형으로 범위 지정
        if (self.enable_drawing and event.button() == Qt.LeftButton
            and self.start_pos != self.end_pos):
            self.enable_drawing = False # 범위 지정 불가능으로 변경
            
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

        self.resetDragInfo() # 시작점, 끝점 초기화

    # 이벤트 필터
    def eventFilter(self, obj:QObject, event:QEvent):
        # R키가 눌렸을 때 선택 영역 지정 초기화
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_R:
            self.initFlag()
            self.initRectAndPos()
            self.setLabelGeometryWithGlobalRect(self.limit_rect)
            print('>>> press key R - reset overlay range')
            return True
        return super().eventFilter(obj, event)
        
    #-------------------------------------------------------------

    def getLabelRect(self) -> QRect:
        return self.label_rect

    def setLabelGeometryWithGlobalRect(self, posRect:QRect):
        self.setGeometry(posRect)
        self.label.setGeometry(0, 0, abs(posRect.width()), abs(posRect.height()))
        self.label_rect = self.frameGeometry()
        self.update()

    def resetDragInfo(self):
        self.start_pos = None
        self.end_pos = None
