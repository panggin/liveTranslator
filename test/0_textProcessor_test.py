# test/0_textProcessor_test.py <- liveTranslator/capture/textProcessor.py

import sys
import cv2 as cv
from PyQt5.QtCore import pyqtSlot

from path_liveTranslator import *
from main.liveTranslator.capture import TextProcessor

@pyqtSlot(str)
def emit_translated_text_receiver(text:str):
    print(f'received : {text}')

# 이미지로부터 텍스트 추출 및 번역 기능 테스트
if __name__ == '__main__':
    print(sys.path)

    textProcessor = TextProcessor()

    imagePath = input('이미지 경로를 입력하세요 : ')
    image = cv.imread(imagePath, cv.IMREAD_COLOR)

    print('----------- extracted -----------\n')
    text = textProcessor.get_text_from_image(image)
    print(text)

    print('----------- translated -----------\n')
    transText = textProcessor.get_translated_text(text)
    print(transText)

    cv.imshow('input image', image)
    cv.waitKey(0)