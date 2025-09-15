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

podcast.yaml 파일을 수정한다. 

```yaml
# podcast.yml
channel_title: "테스트 팟캐스트"
channel_link: "https://your-podcast-website.com"
channel_description: "이것은 예시 팟캐스트입니다."
channel_author: "홍길동"
channel_image: "https://your-podcast-website.com/images/cover.png"

episodes:
  - title: "Attention is all you need"
    description: "트랜스포머와 현대 AI 언어 모델의 탄생 비화"
    audio_file: "audio/001.mp3"
    audio_size: 15326618
    duration: "17:59"
    pub_date: "2025-09-15 22:07:39"
```

원래 이런 식인데, gen.py에서 duration, audio_size는 자동으로 입력하도록 변경했다. 

그래서 

```yaml
# podcast.yml
channel_title: "테스트 팟캐스트"
channel_link: "https://your-podcast-website.com"
channel_description: "이것은 예시 팟캐스트입니다."
channel_author: "홍길동"
channel_image: "https://your-podcast-website.com/images/cover.png"

episodes:
  - title: "Attention is all you need"
    description: "트랜스포머와 현대 AI 언어 모델의 탄생 비화"
    audio_file: "audio/001.mp3"
    pub_date: "2025-09-15 22:07:39"
```

이렇게만 입력하면 된다.

새로운 내용을 입력할 때마다 `- title: ~ audio_file`까지 추가한다. 

순서가 중요한데, 새로운 파일이 맨 위에 나오도록 해야 한다. 

```yaml
# podcast.yaml
channel_title: "테스트 팟캐스트"
channel_link: "https://your-podcast-website.com"
channel_description: "이것은 예시 팟캐스트입니다."
channel_author: "홍길동"
channel_image: "https://your-podcast-website.com/images/cover.png"

episodes:
  - title: "2번째 에피소드"
    description: "2번째 에피소드"
    audio_file: "audio/002.mp3"
    pub_date: "2025-09-15 22:07:39"

  - title: "1번째 에피소드"
    description: "1번째 에피소드"
    audio_file: "audio/001.mp3"
    pub_date: "2025-09-15 22:07:39"
```

이렇게 podcast.yaml 파일을 수정한 다음,   
feed.xml 파일을 만들기 위해,

```ps
python gen.py
```

를 실행하면 그에 맞게 feed.xml 파일이 생성된다.

https://stuousk.github.io/podcast/feed.xml

```xml
<rss xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">
<channel>
<title>테스트 팟캐스트</title>
<link>https://your-podcast-website.com</link>
<description>이것은 예시 팟캐스트입니다.</description>
<itunes:author>홍길동</itunes:author>
<itunes:image href="https://your-podcast-website.com/images/cover.png"/>
<item>
<title>Attention is all you need</title>
<description>트랜스포머와 현대 AI 언어 모델의 탄생 비화</description>
<guid>audio/001.mp3</guid>
<enclosure url="https://stuousk.github.io/podcast/audio/001.mp3" length="15326618" type="audio/mpeg"/>
<pubDate>Mon, 15 Sep 2025 22:21:09 </pubDate>
<itunes:duration>17:59</itunes:duration>
</item>
</channel>
</rss>
```