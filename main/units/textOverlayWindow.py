import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt, QPoint, QEvent

from selectionArea import SelectionArea
from overlayStyle import *

class TextOverlayWindow(SelectionArea):
    def __init__(self):
        super().__init__()

        self.enable_moving = False # 드래그하여 창 이동 가능


    # 마우스 클릭 이벤트 처리
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if self.enable_moving :
            self.dragging = True
            self.start_pos = event.globalPos()
            # self.start_pos = event.globalPos() - self.label_geometry.topLeft()
            print('label geometry : ', self.label_geometry) # debugging
            self.printDragPos('move start') # debugging
    
    # 마우스 이동 이벤트 처리
    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.enable_moving and self.dragging and self.start_pos:
            mv = self.label_geometry.topLeft() + (event.globalPos() - self.start_pos)
            self.move(mv)
            event.accept()
    
    # 마우스 릴리스 이벤트 처리
    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if self.enable_moving:
            self.label_geometry = self.frameGeometry()
            print('window : ', self.frameGeometry()) # debugging
            print('label : ', self.label.frameGeometry()) # debugging
            self.start_pos = None
            self.dragging = False

    # 마우스 올리기 이벤트 처리
    def enterEvent(self, event):
        if self.enable_drawing  == False and self.enable_moving == False:
            self.label.setStyleSheet(transparent_style)

    # 마우스 올리기 이벤트 처리
    def leaveEvent(self, event):
        if self.enable_drawing == False and self.enable_moving == False:
            self.label.setStyleSheet(default_style)

    # 이벤트 필터
    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_R:
            print("press key R") # debugging
            self.close()
            self.__init__()
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_M:
            print("press key M") # debugging
            self.enable_moving = ~self.enable_moving
            self.label.setStyleSheet("background-color: rgba(255, 255, 255, 100); color: White; font-family: Arial; font-size: 20px;")

        return super().eventFilter(obj, event)
    

# 디버깅을 위한 메인함수
if __name__ == "__main__":
    app = QApplication(sys.argv)    
    overlay = TextOverlayWindow()
    # print(QApplication.desktop().availableGeometry())
    sys.exit(app.exec_())