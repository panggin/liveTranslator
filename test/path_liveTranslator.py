# test/path_liveTranslator.py

import sys
import os

# 현재 파일의 디렉토리를 기준으로 부모 디렉토리 경로 추가 (LiveTranslator/)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
