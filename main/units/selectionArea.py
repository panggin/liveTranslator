import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import QEvent, Qt, QPoint, QRect
from PyQt5.QtGui import QPainter, QPen

class SelectionArea(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Overlay Window")

        # 플래그
        self.dragging = False  # 드래그 중인지 여부를 나타내는 플래그
        self.enable_drawing = True # 범위 지정이 가능한지 여부를 나타내는 플래그
        self.enable_moving = False # 드래그하여 창 이동 가능

        # 위치 정보
        self.start_pos = QPoint(0,0)  # 드래그 시작 위치를 저장하는 변수
        self.end_pos = QPoint(0,0)  # 드래그 끝 위치를 저장하는 변수
        self.drag_pos = [0,0,0,0]

        # 윈도우의 특성 설정 (오버레이 창)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(0, 0, QApplication.desktop().width(), QApplication.desktop().height())  # 창 위치 및 크기 설정(고정)

        
        # 오버레이 창에 표시할 라벨 추가
        self.label = QLabel(None, self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background-color: rgba(255, 255, 255, 100);")
        self.label.setGeometry(0, 0, QApplication.desktop().width(), QApplication.desktop().height())  # 라벨 위치 및 크기 설정
        self.label.setText("Set window position by dragging")

        # 이벤트 필터 등록
        self.installEventFilter(self)

        # 오버레이 창 배치
        self.show()

        self.printFlags("init") # debugging
    
    def paintEvent(self, event):
        # 드래그 중인 경우에만 사각형을 그립니다.
        if self.dragging and self.enable_drawing:
            painter = QPainter(self)
            painter.setPen(QPen(Qt.green, 2, Qt.SolidLine))
            rect = QRect(self.start_pos, self.end_pos)
            painter.drawRect(rect)

    # 마우스 클릭 이벤트 처리
    def mousePressEvent(self, event):
        if self.enable_drawing and event.buttons() == Qt.LeftButton:
            self.dragging = True
            self.start_pos = event.pos()
            self.end_pos = event.pos()

            self.printPos("mouse press") # debugging

    # 마우스 이동 이벤트 처리
    def mouseMoveEvent(self, event):
        if self.enable_drawing and self.dragging:
            self.end_pos = event.pos()
            self.update()

    # 마우스 릴리스 이벤트 처리
    def mouseReleaseEvent(self, event):
        if self.enable_drawing and event.button() == Qt.LeftButton:
            self.dragging = False
            self.printPos("mouse release") # debugging

            if self.enable_drawing and self.start_pos != self.end_pos:
                self.enable_drawing = False
                self.enable_moving = True

                self.drag_pos = self.getDragPos()
                self.printPos("drag complete") # debugging
                self.printFlags("drag complete") # debugging
                self.resizeWithDragPos(self.drag_pos)
                self.label.setText("This is subtitle overlay window")

            self.update()

    def getDragPos(self):
        w = abs(self.start_pos.x() - self.end_pos.x())
        h = abs(self.start_pos.y() - self.end_pos.y())
        return [self.start_pos.x(), self.start_pos.y(), w, h]
    
    def resizeWithDragPos(self, pos):
        self.setGeometry(pos[0], pos[1], pos[2], pos[3])
        self.label.setGeometry(0, 0, pos[2], pos[3])

    def resizeWindowWithDragPos(self, pos):
        self.setGeometry(pos[0], pos[1], pos[2], pos[3])

    def resizeLabelWithDragPos(self, pos):
        self.label.setGeometry(pos[0], pos[1], pos[2], pos[3])

    def resetSelection(self):
        resetPos = [0,0,QApplication.desktop().width(), QApplication.desktop().height()]
        self.resizeWithDragPos(resetPos)

        self.dragging = False
        self.enable_drawing = True
        self.enable_moving = False

        self.label.setText("Set window position by dragging")
        self.printFlags("reset") # debugging
    
    # 이벤트 필터
    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_R:
            print("press key R") # debugging
            self.resetSelection()
        return super().eventFilter(obj, event)
    
    # 디버깅 함수
    def printPos(self, statusText):
        print("----------------------------")
        print(f'{statusText} - start_pos : {self.start_pos}')
        print(f'{statusText} - end_pos : {self.end_pos}')
        print(f'{statusText} - drag_pos : {self.drag_pos}')
        print("----------------------------")

    def printFlags(self, statusText="result"):
        print("----------------------------")
        print(f'{statusText} - dragging : {self.dragging}')
        print(f'{statusText} - drawing : {self.enable_drawing}')
        print(f'{statusText} - moving : {self.enable_moving}')
        print("----------------------------")


# 디버깅을 위한 메인함수
if __name__ == "__main__":
    app = QApplication(sys.argv)    
    overlay = SelectionArea()
    sys.exit(app.exec_())
