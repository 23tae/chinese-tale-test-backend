# 🎭 나와 닮은 중국 고전 속 인물 찾기 API 서버

## 📖 소개

FastAPI로 구현된 RESTful API 서버입니다. 사용자의 성격과 중국 고전 문학 작품 속 캐릭터를 매칭해주는 서비스를 제공합니다.

### ⚡️ 주요 기능

- 성격 테스트 질문 목록 제공
- 사용자 답변 기반 캐릭터 매칭
- 16개 중국 고전 캐릭터 데이터베이스
- 개인화된 결과 메시지 생성

## 🛠 기술 스택

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Deployment**: Railway
- **Documentation**: Swagger UI

## 🏃‍♂️ 로컬 실행 방법

1. 가상환경 설정
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. 의존성 설치
```bash
pip install -r requirements.txt
```

3. 환경변수 설정
`.env` 파일 생성:
```env
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=sinotale
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=password
```

4. 서버 실행
```bash
uvicorn app.main:app --reload
```

서버가 실행되면 다음 URL에서 API 문서를 확인할 수 있습니다:
- Swagger UI: http://localhost:8000/docs

## 📂 프로젝트 구조

```
app/
├── api
│   ├── __init__.py
│   ├── analysis.py
│   └── questions.py
├── config.py
├── data
│   ├── characters.csv
│   ├── questions.csv
│   └── result_templates.csv
├── database.py
├── main.py
├── models
│   ├── __init__.py
│   ├── answer.py
│   ├── character.py
│   ├── question.py
│   └── result_template.py
├── schemas
│   ├── __init__.py
│   ├── character.py
│   ├── question.py
│   └── response.py
├── services
│   ├── __init__.py
│   └── matcher.py
└── utils
    ├── __init__.py
    ├── db_loader.py
    ├── get_josa.py
    └── helpers.py
```

## 📊 데이터베이스 구조

### Characters
- 16개의 중국 고전 캐릭터 정보
- 성격 특성 점수 (용기, 충성도, 지혜 등)
- 캐릭터 설명 및 배경 스토리

### Questions
- 성격 테스트 질문 목록
- 각 질문별 선택지
- 특성 연관 정보

### Result Templates
- 결과 템플릿 메시지
- 캐릭터별 맞춤 설명


## 📝 API 문서

- API 스펙 문서: [api-spec.md](docs/api-spec.md)
