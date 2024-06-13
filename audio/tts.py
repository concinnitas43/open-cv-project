import os
from gtts import gTTS
import pygame


# 제품 정보
info = {
    0: {'name': "물품이 감지되지 않습니다."},
    1: {
        'name': '양파링', 
        'price': '4000', 
        'event': '2+1 행사 중, 3개에 8천원',
        'shortinfo': '약간 짠 맛이 나는 양파 베이스 과자', 
        'specificinfo': '양파를 베이스로 하는 감자, 베이컨 맛 등의 시즈닝이 들어간 고리모양의 과자. 맥주와 함께 먹으면 좋은 안주가 된다.'
    },
    2: {
        'name': '신짱', 
        'price': '3800', 
        'event': '행사 없음',
        'shortinfo': '원통형 튀긴 과자에 시럽을 묻힌 과자.', 
        'specificinfo': '원통형 튀긴 과자에 시럽을 묻힌 과자. 단 맛이 난다.'
    },
    3: {
        'name': '꼬깔콘', 
        'price': '3600', 
        'event': '행사 없음',
        'shortinfo': '꼬깔콘 매콤달콤한 맛', 
        'specificinfo': '꼬깔콘 중 가장 매운 맛이 강한 종류이다.'
    },
    4: {
        'name': '몬스터 흰색', 
        'price': '2200', 
        'event': '모든 몬스터 종류에 대해 2+1 행사중',
        'shortinfo': '몬스터 에너지 울트라', 
        'specificinfo': '몬스터 중 에너지 드링크의 설탕을 빼고 칼로리를 줄인 버전'
    },
    5: {
        'name': '몬스터 핑크색', 
        'price': '2200', 
        'event': '모든 몬스터 종류에 대해 2+1 행사중',
        'shortinfo': '몬스터 에너지 파이프라인 펀치', 
        'specificinfo': '패션프루트, 오렌지, 구아바를 베이스로 만든 몬스터 에너지 드링크'
    },
    6: {
        'name': '몬스터 주황색', 
        'price': '2200', 
        'event': '모든 몬스터 종류에 대해 2+1 행사중',
        'shortinfo': '몬스터 에너지 울트라 선라이즈', 
        'specificinfo': '열정을 위해 아침잠을 포기하는 이들을 위한 음료. 청량하고 상쾌한 맛이다.'
    }
}
# products = { 1: "양파링", 2: "신짱", 3: "꼬깔콘", 4: "흰색 몬스터", 5: "핑크색 몬스터", 6: "주황색 몬스터" }


def tts_speak(product_ID, Volume, info_state):  # 제품 아이디를 받아 tts로 말해주는 함수
    product_infos = info[product_ID]  # text를 만들기 위해 제품 정보 리스트를 받음
    product_info_lst = list(product_infos.values())  # 제품 정보들에 대한 리스트
    info_states =list(info_state.values())  # True False에 대한 리스트(제품 정보를 말할지 말지)
    text=''  # 빈 텍스트
    if product_ID != 0:
        for inx, isTrue in enumerate(info_states):  # 항목 넣어야되면 넣기
            if isTrue:
                text = text +' '+ product_info_lst[inx]  #띄어쓰기 하고 정보 넣기
    if text =='':  # 텍스트 비었으면
        text = product_info_lst[0]  # 이름 넣기

    tts = gTTS(text, lang='ko')  # 아이디에 대응되는 이름을 한국어로 말하는 tts 객체 생성
    tts_file = "product_name.mp3"  # tts 객체 저장할 파일 이름
    tts.save(tts_file)  # tts 객체를 파일에 저장

    pygame.mixer.init()  # pygame 초기화
    pygame.mixer.music.load(tts_file)  # mp3 파일 로드
    pygame.mixer.music.set_volume(Volume / 100) # Adjust volume (0.0 to 1.0)
    pygame.mixer.music.play()  # mp3 파일 재생


    while pygame.mixer.music.get_busy():  # 재생이 끝날 때까지 대기
        pygame.time.Clock().tick(10)

    pygame.mixer.quit()  # 믹서 종료
    os.remove(tts_file)  # 일시적으로 생성된 tts_file 지우기

