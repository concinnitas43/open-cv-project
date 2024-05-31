from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

text = "안녕하세요"
tts = gTTS(text=text, lang='ko')

tts.save("test-audio-file.mp3")

audio = AudioSegment.from_mp3("test-audio-file.mp3")

play(audio)
