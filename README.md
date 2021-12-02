# 마스크 추천 사이트
## 개발 환경

- Windows 10
- Flask 2.0.2


## 소개

- data_analysis_env
    - 데이터 수집, 분석과 관련된 코드
- Docker_image
    - 도커 환경
- flask_env
    - 웹서버 구동과 관련된 코드

## 동작 방식

- data_analysis_env
    - 디렉토리 내에 mask_crawling.py를 실행합니다.
    - 이후 결과는 mask_data_final.csv 파일로 저장, 출력됩니다.
    - 디렉토리 내에 TF-IDF분석.ipynb를 통해 review_keyword.csv 도출
- flask_env
    - 디렉토리 내에 app.py를 실행합니다.
