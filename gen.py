import yaml
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime

import os
from mutagen.mp3 import MP3
from mutagen.mp3 import HeaderNotFoundError

# mp3 파일의 길이를 분초 형식으로 가져오는 함수
def get_mp3_duration(file_path):
    """
    MP3 파일의 길이를 분초 형식(MM:SS)으로 가져오는 함수

    :param file_path: MP3 파일의 경로
    :return: 'MM:SS' 형식의 문자열, 파일이 없거나 유효하지 않으면 None 반환
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found at '{file_path}'")
        return None

    try:
        audio = MP3(file_path)
        total_seconds = audio.info.length
        
        hours = int(total_seconds // 3600)
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)
        
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
    except HeaderNotFoundError:
        print(f"Error: '{file_path}' is not a valid MP3 file or has a corrupted header.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


# 팟캐스트 피드 생성 함수
def generate_podcast_feed(yaml_file_path, xml_file_path):
    """
    YAML 파일에서 데이터를 읽어 팟캐스트 RSS 피드를 생성합니다.
    """
    try:
        with open(yaml_file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: YAML file not found at '{yaml_file_path}'")
        return

    # XML 기본 구조 생성
    rss = ET.Element('rss', {
        'version': '2.0',
        'xmlns:itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
        'xmlns:atom': 'http://www.w3.org/2005/Atom'
    })
    channel = ET.SubElement(rss, 'channel')

    # 팟캐스트 채널 정보 추가
    ET.SubElement(channel, 'title').text = data['channel_title']
    ET.SubElement(channel, 'link').text = data['channel_link']
    ET.SubElement(channel, 'description').text = data['channel_description']
    ET.SubElement(channel, 'itunes:author').text = data['channel_author']
    
    # 팟캐스트 이미지 추가
    itunes_image = ET.SubElement(channel, 'itunes:image')
    itunes_image.set('href', data['channel_image'])

    # 에피소드 목록 추가
    for episode in data.get('episodes', []):
        url = "https://stuousk.github.io/podcast/" + episode['audio_file']

        item = ET.SubElement(channel, 'item')
        ET.SubElement(item, 'title').text = episode['title']
        ET.SubElement(item, 'description').text = episode['description']
        ET.SubElement(item, 'guid').text = url
        
        # 파일 정보 (enclosure)
        enclosure = ET.SubElement(item, 'enclosure')        
        enclosure.set('url', url)
        #enclosure.set('length', str(episode['audio_size']))

        current_audio_file = 'docs/' + episode['audio_file']
        #print("audio_file = ", current_audio_file)

        enclosure.set('length', str(os.path.getsize(current_audio_file)))
        
        enclosure.set('type', 'audio/mpeg')

        # 발행 날짜 형식 변환. 그냥 현재 시각을 사용한다.
        # pub_date_obj = datetime.strptime(episode['pub_date'], '%Y-%m-%dT%H:%M:%S%z')
        ET.SubElement(item, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')
        
        # ITunes 에피소드 정보
        #ET.SubElement(item, 'itunes:duration').text = episode['duration']
        ET.SubElement(item, 'itunes:duration').text = get_mp3_duration(current_audio_file)
        

    # XML을 보기 좋게 정렬하여 파일에 저장
    xml_string = ET.tostring(rss, encoding='utf-8')
    pretty_xml = minidom.parseString(xml_string).toprettyxml(indent="  ")

    with open(xml_file_path, 'w', encoding='utf-8') as file:
        file.write(pretty_xml)
        
    print(f"Success: Podcast feed generated at '{xml_file_path}'")

if __name__ == "__main__":
    # 스크립트 실행
    generate_podcast_feed('podcast.yaml', 'docs/feed.xml')