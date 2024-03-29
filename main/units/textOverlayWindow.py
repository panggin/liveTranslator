import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import QObject, Qt, QPoint, QEvent, QRect

from selectionArea import SelectionArea
from overlayStyle import *

class TextOverlayWindow(SelectionArea):
    def __init__(self, limitRect):
        super().__init__()
        self.enable_moving = False # 드래그하여 창 이동 가능
        self.lock_resize = False # 설정값 최종 결정 여부

        self.limit_rect = limitRect # 입력한 값으로 범위 제한 재설정
        self.setLabelGeometryWithGlobalRect(self.limit_rect)
        

    # 마우스 클릭 이벤트 처리
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if self.enable_moving :
            self.dragging = True
            self.start_pos = event.globalPos()
            print('label geometry : ', self.label_rect) # debugging
            self.printDragPos('move start') # debugging
    
    # 마우스 이동 이벤트 처리
    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.enable_moving and self.dragging and self.start_pos:
            mv = self.label_rect.topLeft() + (event.globalPos() - self.start_pos)
            self.move(mv)
            event.accept()
    
    # 마우스 릴리스 이벤트 처리
    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if self.enable_moving:
            self.label_rect = self.frameGeometry()
            print('window : ', self.frameGeometry()) # debugging
            print('label : ', self.label.frameGeometry()) # debugging
            self.start_pos = None
            self.dragging = False

    # 마우스가 라벨에 올라갔을 때 이벤트 처리
    def enterEvent(self, event):
        if not self.enable_drawing and not self.enable_moving:
            self.label.setStyleSheet(transparent_style)

    # 마우스가 라벨에서 벗어났을 때 이벤트 처리
    def leaveEvent(self, event):
        if not self.enable_drawing and not self.enable_moving:
            self.label.setStyleSheet(default_style)

    # 이벤트 필터
    def eventFilter(self, obj, event):
        if not self.lock_resize and event.type() == QEvent.KeyPress and event.key() == Qt.Key_R: # 창 크기 재조정
            print("press key R") # debugging
            self.close()
            self.__init__(self.limit_rect) # 초기화
            self.show()
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_F: # 창 최종 결정
            print("press key F") # debugging
            self.lock_resize = True
            self.enable_moving = True
            self.label.setStyleSheet(default_style)
        return False # 부모 클래스로 이벤트 전달X
    

# 디버깅을 위한 메인함수
if __name__ == "__main__":
    app = QApplication(sys.argv) 
    limitRect = QRect(100, 47, 908, 687)   
    overlay = TextOverlayWindow(limitRect)
    overlay.show()
    # print(QApplication.desktop().availableGeometry())
    sys.exit(app.exec_())