# API Specification

## Endpoints

### 1. 질문 목록 조회

```http
GET /questions
```

테스트를 위한 전체 질문 목록을 반환합니다.

#### Response

```typescript
[
  {
    "id": number,
    "content": string,      // 질문 내용
    "choices": string[],    // 선택지 목록
    "trait_type": string    // 성격 특성 유형
  }
]
```

**Example Response:**
```json
[
  {
    "id": 1,
    "content": "친구가 어려움에 처했을 때 당신은?",
    "choices": [
      "즉시 도움을 준다",
      "상황을 파악하고 도움을 준다",
      "함께 해결책을 찾아본다",
      "조언을 해준다"
    ],
    "trait_type": "loyalty"
  }
]
```

### 2. 답변 분석 및 캐릭터 매칭

```http
POST /analyze
```

사용자의 답변을 분석하여 가장 닮은 캐릭터를 찾아줍니다.

#### Request Body

```typescript
{
  "answers": {
    [key: string]: number  // 질문 ID: 선택한 답변 인덱스
  }
}
```

**Example Request:**
```json
{
  "answers": {
    "1": 2,
    "2": 1,
    "3": 3
  }
}
```

#### Response

```typescript
{
  "character": {
    "id": number,
    "name": string,        // 캐릭터 이름
    "work": string,        // 등장 작품
    "description": string, // 캐릭터 설명
    "image_url": string,   // 캐릭터 이미지 URL
    "media_url": string    // 관련 미디어 URL
  },
  "description": string,           // 매칭 설명
  "modern_interpretation": string, // 현대적 해석
  "advice": string                 // 조언
}
```

**Example Response:**
```json
{
  "character": {
    "id": 1,
    "name": "화목란",
    "work": "목란사",
    "description": "아버지를 대신해 전쟁에 나간 여성 영웅",
    "image_url": "https://...",
    "media_url": "https://..."
  },
  "description": "당신은 화목란처럼 충성심이 강하고 결단력이 있는 성격입니다.",
  "modern_interpretation": "현대 사회에서 당신은 책임감과 용기를 바탕으로...",
  "advice": "때로는 자신의 한계를 시험해보는 것도 좋습니다..."
}
```
