## 해야할 것
# 1. 필요없는거 하위 폴더로
# 2. 샘플링 레이트 반환 x
# 3. 반환형은 byte
# 4. 스날
# 5. dependency

from module_test import TTS

# TTS 인스턴스를 생성합니다.
tts = TTS()

# 테스트할 텍스트와 발화자 설정
text = "안녕하세요, 이것은 테스트입니다."
speaker = tts.speakers[0]  # 첫 번째 발화자를 선택합니다. 실제 사용시에는 발화자 리스트를 확인해야 합니다.

# TTS를 사용하여 음성 합성을 수행합니다.
sampling_rate, audio = tts.generate(text)

# 결과를 확인합니다.
print(f"Sampling Rate: {sampling_rate}")
print(f"Audio Length: {len(audio)}")
print(f"Audio type: {type(audio)}")
# print(f"{audio}")
# print()

import base64
print(base64.b64encode(audio).decode("utf-8")[:10])

# # 음성 데이터를 파일로 저장합니다.
# import soundfile as sf
# sf.write('output_test.wav', audio, samplerate=sampling_rate)