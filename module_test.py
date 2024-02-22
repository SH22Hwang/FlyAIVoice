import torch
from torch import no_grad, LongTensor
import soundfile as sf
from io import BytesIO
import base64

from VITSfast.models import SynthesizerTrn
from VITSfast.text import text_to_sequence
from VITSfast import commons
from VITSfast import utils

class TTS():
    def __init__(self, model_dir="../model/G_latest.pth", config_dir="../finetune_speaker.json"):
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"

        self.language_marks = {
            "Japanese": "",
            "日本語": "[JA]",
            "简体中文": "[ZH]",
            "English": "[EN]",
            "한국어": "[KO]",
            "Mix": "",
        }

        # 매개변수
        # self.model_dir = "../model/G_latest.pth"
        # self.config_dir = "./finetune_speaker.json"
        self.model_dir = model_dir
        self.config_dir = config_dir

        self.hps = utils.get_hparams_from_file(self.config_dir)

        self.net_g = SynthesizerTrn(
            len(self.hps.symbols),
            self.hps.data.filter_length // 2 + 1,
            self.hps.train.segment_size // self.hps.data.hop_length,
            n_speakers=self.hps.data.n_speakers,
            **self.hps.model).to(self.device)
        _ = self.net_g.eval()

        _ = utils.load_checkpoint(self.model_dir, self.net_g, None)
        self.speaker_ids = self.hps.speakers
        self.speakers = list(self.hps.speakers.keys())
    
    def get_text(self, text, hps, is_symbol):
        text_norm = text_to_sequence(text, hps.symbols, [] if is_symbol else hps.data.text_cleaners)
        if hps.data.add_blank:
            text_norm = commons.intersperse(text_norm, 0)
        text_norm = LongTensor(text_norm)
        return text_norm

    def tts_fn(self, text, speaker, language="한국어", speed=1):
        if language is not None:
            text = self.language_marks[language] + text + self.language_marks[language]
        
        speaker_id = self.speaker_ids[speaker]
        stn_tst = self.get_text(text, self.hps, False)
        with no_grad():
            x_tst = stn_tst.unsqueeze(0).to(self.device)
            x_tst_lengths = LongTensor([stn_tst.size(0)]).to(self.device)
            sid = LongTensor([speaker_id]).to(self.device)
            audio = self.net_g.infer(
                x_tst, x_tst_lengths, sid=sid, noise_scale=.667, noise_scale_w=0.8,
                length_scale=1.0 / speed
            )[0][0, 0].data.cpu().float().numpy()
        del stn_tst, x_tst, x_tst_lengths, sid
        return (self.hps.data.sampling_rate, audio)
        # return audio

    def audio_numpy_to_base64(self,sampling_rate, audio):
        # Convert the NumPy array to a BytesIO buffer as a WAV file
        buffer = BytesIO()
        sf.write(buffer, audio, sampling_rate, format='wav')
        buffer.seek(0)  # Rewind the buffer to start

        # Convert the buffer to a base64 string
        audio_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        return audio_base64
    
    def audio_numpy_to_bytes(self,sampling_rate, audio):
        # Convert the NumPy array to a BytesIO buffer as a WAV file
        buffer = BytesIO()
        sf.write(buffer, audio, sampling_rate, format='wav')
        buffer.seek(0)  # Rewind the buffer to start

        audio_bytes = buffer.getvalue()
        return audio_bytes

    def generate(self, text:str) -> str: # base64 반환 
        sampling_rate, audio = self.tts_fn(text, self.speakers[0], "한국어", 1)
        # audio_base64 = self.audio_numpy_to_base64(sampling_rate, audio)
        audio_bytes = self.audio_numpy_to_bytes(sampling_rate, audio)

        return audio_bytes

# 주의: utils, commons 모듈과 필요한 함수 및 변수 정의가 필요합니다.
# utils.get_hparams_from_file, commons.intersperse 등은 사용자 정의 함수이므로,
# 해당 코드를 실행하려면 이러한 함수들이 정의되어 있어야 합니다.
    
"""
import os
import numpy as np
import torch
from torch import no_grad, LongTensor
import argparse
import commons
from mel_processing import spectrogram_torch
import utils
from models import SynthesizerTrn
import librosa
import webbrowser

from text import text_to_sequence, _clean_text
device = "cuda:0" if torch.cuda.is_available() else "cpu"


language_marks = {
    "Japanese": "",
    "日本語": "[JA]",
    "简体中文": "[ZH]",
    "English": "[EN]",
    "한국어": "[KO]",
    "Mix": "",
}
lang = ['日本語', '简体中文', 'English', 'Mix','한국어']


class TTS():
    def __init__(self, text:str):
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"

        self.model_dir = "./model/G_latest.pth"
        config_dir = "./finetune_speaker.json"
        self.share = False

        self.hps = utils.get_hparams_from_file(config_dir)

        self.net_g = SynthesizerTrn( # model 불러오기
            len(self.hps.symbols),
            self.hps.data.filter_length // 2 + 1,
            self.hps.train.segment_size // self.hps.data.hop_length,
            n_speakers=self.hps.data.n_speakers,
            **self.hps.model).to(self.device)
        _ = self.net_g.eval()

        _ = utils.load_checkpoint(self.model_dir, self.net_g, None)
        self.speaker_ids = self.hps.speakers
        self.speakers = list(self.hps.speakers.keys())
    
    def get_text(self, text, hps, is_symbol):
        text_norm = text_to_sequence(text, hps.symbols, [] if is_symbol else hps.data.text_cleaners)
        if hps.data.add_blank:
            text_norm = commons.intersperse(text_norm, 0)
        text_norm = LongTensor(text_norm)
        return text_norm

    def tts_fn(self, text, speaker, language="한국어", speed=1):
        if language is not None:
            text = language_marks[language] + text + language_marks[language]
        
        speaker_id = self.speaker_ids[speaker]
        stn_tst = self.get_text(text, self.hps, False)
        with no_grad():
            x_tst = stn_tst.unsqueeze(0).to(device)
            x_tst_lengths = LongTensor([stn_tst.size(0)]).to(device)
            sid = LongTensor([speaker_id]).to(device)
            audio = self.net_g.infer(
                x_tst, x_tst_lengths, sid=sid, noise_scale=.667, noise_scale_w=0.8,
                length_scale=1.0 / speed
            )[0][0, 0].data.cpu().float().numpy()
        del stn_tst, x_tst, x_tst_lengths, sid
        return (self.hps.data.sampling_rate, audio)


    def generate(self, text:str):
        sampling_late, audio = self.tts_fn(self, text, self.speakers[0], "한국어", 1)
        return sampling_late, audio
"""