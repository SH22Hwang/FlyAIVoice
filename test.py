from module_test import TTS
import time
import base64


def base64_to_wav(base64_string, output_file_path):
    # Decode the Base64 string
    audio_data = base64.b64decode(base64_string)
    
    # Write the decoded bytes to a file with a .wav extension
    with open(output_file_path, 'wb') as wav_file:
        wav_file.write(audio_data)


# TTS 인스턴스를 생성합니다.
tts = TTS()

# 테스트할 텍스트와 발화자 설정
text = "안녕하세요, 이것은 테스트입니다."
speaker = tts.speakers[0]  # 첫 번째 발화자를 선택합니다. 실제 사용시에는 발화자 리스트를 확인해야 합니다.

start = time.time()
# TTS를 사용하여 음성 합성을 수행합니다.
# audio2base64 = tts.generate(text)
audio2bytes = tts.generate(text)
end = time.time()

# 결과를 확인합니다.
print(f"Time: {end - start:.5f} sec")

print(f"audio2bytes type: {type(audio2bytes)}")
print(f"bytes: {audio2bytes[:10]}")

audio2base64 = base64.b64encode(audio2bytes)
print(f"audio2base64 type: {type(audio2base64)}")
print(f"base64: {audio2base64[:10]}")

# Example usage
output_file_path = "output_base64towav.wav"  # Specify the output file path

base64_to_wav(audio2base64, output_file_path)