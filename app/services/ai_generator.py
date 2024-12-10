from sqlalchemy.orm import Session
from openai import AsyncOpenAI
from ..config import settings
from ..models.character import Character
from typing import Dict
from ..models.question import Question

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


async def generate_personalized_description(character_id: int, answers: Dict[int, int], db: Session) -> str:
    # 캐릭터 정보 조회
    character = db.query(Character).filter(Character.id == character_id).first()

    # 질문 정보 조회하여 답변과 매핑
    questions = db.query(Question).all()
    user_responses = []
    for question in questions:
        if question.id in answers:
            choice_index = answers[question.id]
            choice = question.choices[choice_index]
            user_responses.append(f"질문: {question.content}\n답변: {choice}")

    # 사용자 답변 요약
    answers_summary = "\n".join(user_responses)

    prompt = f"""
    캐릭터 '{character.name}'의 특성과 사용자의 답변을 바탕으로 개인화된 결과 설명을 생성해주세요.

    [캐릭터 정보]
    이름: {character.name}
    작품: {character.work}
    설명: {character.description}

    [사용자의 답변]
    {answers_summary}

    위 정보를 바탕으로 다음 내용이 포함된 설명을 생성해주세요:
    1. 캐릭터와 사용자의 공통점
    2. 현대적 맥락에서의 해석
    3. 캐릭터의 스토리를 통한 조언

    답변은 친근하고 공감되는 톤으로 작성해주세요.
    """

    response = await client.chat.completions.create(
        model="gpt-4.0-mini",
        messages=[
            {
                "role": "system",
                "content": "당신은 중국 고전문학 전문가입니다. 사용자의 답변을 분석하여 공감되고 통찰력 있는 조언을 제공합니다."
            },
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content