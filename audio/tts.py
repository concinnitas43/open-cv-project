import os
from gtts import gTTS
import playsound

products = { 1: "양파링", 2: "신짱", 3: "꼬깔콘", 4: "흰색 몬스터", 5: "핑크색 몬스터", 6: "주황색 몬스터" }

def tts_speak(product_ID):  # 제품 아이디를 받아 tts로 말해주는 함수
    tts = gTTS(text=products.get(product_ID, "알 수 없는 제품 ID"), lang='ko')  # 아이디에 대응되는 이름을 한국어로 말하는 tts 객체 생성
    tts_file = "product_name.mp3"  # tts 객체 저장할 파일 이름
    tts.save(tts_file)  # tts 객체를 파일에 저장
    playsound.playsound(tts_file)  # tts 소리 내기
    os.remove(tts_file)  # 일시적으로 생성된 tts_file 지우기
