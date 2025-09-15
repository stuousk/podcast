# podcast
팟캐스트 만들기 

오늘 2025. 9. 15. 현재 [https://github.com/marketplace/actions/podcast-generator](https://github.com/marketplace/actions/podcast-generator) 은 안 된다. 제일 편한 방법인데.

그래서 자체적으로 generator를 만들었다.

## 환경설정
```ps
python -m venv venv
.\venv\Scripts\activate
python -m pip install --upgrade pip

pip install PyYAML
pip install mutagen
```

- mutagen은 mp3 파일의 길이를 분초 형식으로 가져오기 위해
