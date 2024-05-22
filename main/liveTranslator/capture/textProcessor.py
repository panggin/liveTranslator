# textProcessor.py

from enum import Enum
from copy import deepcopy
from numpy import ndarray

import pytesseract
from googletrans import Translator # 번역 기능 추가

class LANG(Enum):
    ENG = 0
    JPN = 1

class TextProcessor:
    # 텍스트 추출 및 번역기 언어 설정
    textSetting = {LANG.ENG : {'lang':'eng+kor', 'src':'en', 'dest':'ko'},
                   LANG.JPN : {'lang':'jpn+kor', 'src':'ja', 'dest':'ko'}}

    def __init__(self, language=LANG.ENG):
        self.translator = Translator()
        
        self.language = language
        self.lang = TextProcessor.textSetting[self.language]['lang']
        self.src = TextProcessor.textSetting[self.language]['src']
        self.dest = TextProcessor.textSetting[self.language]['dest']
        
        self.text = ''
        self.prevText = ''

    def emit_translated_text(self, screenshot:ndarray):
        self.text = self.get_text_from_image(screenshot)
        if self.text == '' or self.text == self.prevText: 
            return ''
        
        self.prevText = deepcopy(self.text)
        self.text = self.get_translated_text(self.text)

        return self.text
    

    def get_text_from_image(self, screenshot:ndarray):
        text = pytesseract.image_to_string(screenshot, lang=self.lang)
        # print(f'extracting : {text}') # 추출한 텍스트 확인
        return text

    def get_translated_text(self, text:str):
        result = self.translator.translate(text, src=self.src, dest=self.dest).text
        # print(f'translated : {result}') # 추출한 텍스트 확인
        return result