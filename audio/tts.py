import os
from gtts import gTTS
import pygame

info = {
    1: {
        'name': '양파링', 
        'price': 3000, 
        'event': '1+1 행사 중, 2개에 3천원',
        'shortinfo': '양파링의 짧은설명', 
        'specificinfo': '양파링의 구체적설명'
    },
    2: {
        'name': '양파링', 
        'price': 3000, 
        'event': '1+1 행사 중, 2개에 3천원',
        'shortinfo': '양파링의 짧은설명', 
        'specificinfo': '양파링의 구체적설명'
    },
    3: {
        'name': '양파링', 
        'price': 3000, 
        'event': '1+1 행사 중, 2개에 3천원',
        'shortinfo': '양파링의 짧은설명', 
        'specificinfo': '양파링의 구체적설명'
    },
    4: {
        'name': '양파링', 
        'price': 3000, 
        'event': '1+1 행사 중, 2개에 3천원',
        'shortinfo': '양파링의 짧은설명', 
        'specificinfo': '양파링의 구체적설명'
    },
    5: {
        'name': '양파링', 
        'price': 3000, 
        'event': '1+1 행사 중, 2개에 3천원',
        'shortinfo': '양파링의 짧은설명', 
        'specificinfo': '양파링의 구체적설명'
    },
    6: {
        'name': '양파링', 
        'price': 3000, 
        'event': '1+1 행사 중, 2개에 3천원',
        'shortinfo': '양파링의 짧은설명', 
        'specificinfo': '양파링의 구체적설명'
    }
}
products = { 1: "양파링", 2: "신짱", 3: "꼬깔콘", 4: "흰색 몬스터", 5: "핑크색 몬스터", 6: "주황색 몬스터" }


def tts_speak(product_ID, volumn, info_state):  # 제품 아이디를 받아 tts로 말해주는 함수
    product_infos = info[product_ID]
    product_info_lst = list(product_infos.values())
    info_states =list(info_state.values())
    text=''
    for inx, isTrue in enumerate(info_states):
        if isTrue:
            text = text +' '+ product_info_lst[inx]
    if text =='':
        text = product_info_lst[0]

    tts = gTTS(text, lang='ko')  # 아이디에 대응되는 이름을 한국어로 말하는 tts 객체 생성
    tts_file = "product_name.mp3"  # tts 객체 저장할 파일 이름
    tts.save(tts_file)  # tts 객체를 파일에 저장

    pygame.mixer.init()  # pygame 초기화
    pygame.mixer.music.load(tts_file)  # mp3 파일 로드
    pygame.mixer.music.set_volume(volumn / 100) # Adjust volume (0.0 to 1.0)
    pygame.mixer.music.play()  # mp3 파일 재생


    while pygame.mixer.music.get_busy():  # 재생이 끝날 때까지 대기
        pygame.time.Clock().tick(10)

    pygame.mixer.quit()  # 믹서 종료
    os.remove(tts_file)  # 일시적으로 생성된 tts_file 지우기

