# FlyAIVoice
> SKT Fly AI 4기 팀프로젝트... AI 음성 모델 리포지토리

- 작성자: 황승현
## 가상환경 설치

0. 개발환경 구성
- OS: WSL, Ubuntu 20.04
- `git clone https://github.com/SH22Hwang/FlyAIVoice.git`
- CUDA 12.1
- ffmpeg

1. . Conda 가상환경 만들기

`conda create -n venv python=3.10`

2. FlyAIVoice 디렉토리로 이동

3. 패키지 설치

`pip install -r requirements.txt`
`conda install --file packagelist.txt`

4. VITSfast 디렉토리로 이동

`cd FliAIVoice/VITSfast`

5. test.py로 테스트

`python ../test.py`