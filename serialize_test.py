import torch
import torchaudio
import numpy as np
import io
import pickle
import base64

# Replace 'your_file_path.wav' with the path to your .wav file
file_path = '/home/duckegg/audio/audio_3.wav'

def voice_model(index : int):    
    with open(file_path, "rb") as f:
        temp_file = f.read()
    return temp_file

def create_new_voice(audio : bytes):
    encoded = base64.b64encode(audio).decode("utf-8")
    return encoded

def send_binary_voice(encoded : str):
    binary_data = base64.b64decode(encoded)
    return binary_data

print("-" * 10, "기동기쓰 테스트", "-" * 10)

temp_file = voice_model(3)
print(type(temp_file))
print(temp_file[:10], '\n')
encoded = create_new_voice(temp_file)
print(type(encoded))
print(encoded[:10], '\n')
binary_data = send_binary_voice(encoded)
print(type(binary_data))
print(binary_data[:10])

print("-" * 10, "torchaudio", "-" * 10)

# Load the .wav file tensorsudio
waveform, sampling_rate = torchaudio.load(file_path)
audio = waveform.cpu().float().numpy()

print(f"Waveform tensor: {waveform}")
# print(f"raw audio base64: {base64.b64encode(raw_audio).decode('utf-8')[:10]}")
print(f"torchaudio base64: {base64.b64encode(audio).decode('utf-8')[:10]}")

# # 음성 데이터를 파일로 저장합니다.
torchaudio.save('./output_test.wav', torch.from_numpy(audio), int(sampling_rate))

# print(f"bytes(): {bytes(audio)[:10]}")

# bytes_with_tobytes = audio.tobytes()
# print(f"bytes_with_tobytes: {bytes_with_tobytes[:10]}")
# print(f"tobytes base64: {base64.b64encode(bytes_with_tobytes).decode('utf-8')[:10]}")

print("-" * 10, "승현쓰 테스트", "-" * 10)
# bytes_with_pickle = pickle.dumps(audio)
# print(f"bytes_with_pickle: {bytes_with_pickle[:10]}")
# print(f"tobytes base64: {base64.b64encode(bytes_with_pickle).decode('utf-8')[:10]}")
file_path = './output_test.wav'
temp_file = voice_model(3)
print(type(temp_file))
print(temp_file[:10], '\n')
encoded = create_new_voice(temp_file)
print(type(encoded))
print(encoded[:10], '\n')
binary_data = send_binary_voice(encoded)
print(type(binary_data))
print(binary_data[:10])