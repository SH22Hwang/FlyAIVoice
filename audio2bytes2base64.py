import torchaudio
from io import BytesIO
import base64

file_path = '/home/duckegg/audio/audio_3.wav'

# Example function to generate audio using torchaudio
def generate_audio():
    global file_path
    waveform, sample_rate = torchaudio.load(file_path)  # Assuming you have an audio file
    return waveform, sample_rate

# Save the generated audio to a BytesIO buffer as a WAV file
def save_audio_to_buffer(waveform, sample_rate):
    buffer = BytesIO()
    torchaudio.save(buffer, waveform, sample_rate, format='wav')
    buffer.seek(0)  # Rewind the buffer to the beginning so we can read from it
    return buffer

# Convert buffer to bytes and encode to Base64
def buffer_to_base64(buffer):
    audio_bytes = buffer.read()
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')  # Encode as Base64 and convert to string
    return audio_base64

# Generate audio
waveform, sample_rate = generate_audio()

# Save the generated audio to a buffer as WAV to include headers
audio_buffer = save_audio_to_buffer(waveform, sample_rate)

# Convert the audio in the buffer to Base64 for transmission
audio_base64 = buffer_to_base64(audio_buffer)

print(f"chatgpt buffer: {type(audio_buffer)} {audio_buffer.read()[:10]}")
print(f"chatgpt base64: {type(audio_base64)} {audio_base64[:10]}")
# At this point, audio_base64 is ready to be sent to Machine 2

def base64_to_wav(base64_string, output_file_path):
    # Decode the Base64 string
    audio_data = base64.b64decode(base64_string)
    
    # Write the decoded bytes to a file with a .wav extension
    with open(output_file_path, 'wb') as wav_file:
        wav_file.write(audio_data)

# Example usage
base64_string = audio_base64 # This should be replaced with your actual Base64 string
output_file_path = "output_wav2base642wav.wav"  # Specify the output file path

base64_to_wav(base64_string, output_file_path)

# def voice_model(index : int):    
#     with open(file_path, "rb") as f:
#         temp_file = f.read()
#     return temp_file

# def create_new_voice(audio : bytes):
#     encoded = base64.b64encode(audio).decode("utf-8")
#     return encoded

# def send_binary_voice(encoded : str):
#     binary_data = base64.b64decode(encoded)
#     return binary_data

# print("-" * 10, "기동기쓰 테스트", "-" * 10)

# temp_file = voice_model(3)
# print(type(temp_file))
# print(temp_file[:10], '\n')
# encoded = create_new_voice(temp_file)
# print(type(encoded))
# print(encoded[:10], '\n')
# binary_data = send_binary_voice(encoded)
# print(type(binary_data))
# print(binary_data[:10])