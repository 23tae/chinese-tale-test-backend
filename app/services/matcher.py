from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..models.character import Character
from ..models.question import Question
from ..models.result_template import ResultTemplate
from ..utils.get_josa import get_josa

from typing import Dict
import math


def calculate_trait_scores(answers: Dict[int, int], db: Session) -> Dict[str, float]:
    # 특성별 점수와 응답 수를 저장할 딕셔너리
    trait_scores = {
        "courage": 0,
        "loyalty": 0,
        "wisdom": 0,
        "justice": 0,
        "compassion": 0,
        "determination": 0
    }
    trait_counts = dict.fromkeys(trait_scores.keys(), 0)

    # 선택지별 가중치 (1번 선택지가 해당 특성을 가장 강하게 반영)
    choice_weights = {1: 1.0, 2: 0.7, 3: 0.4, 4: 0.1}

    # 각 답변에 대해 특성 점수 계산
    for question_id, choice in answers.items():
        question = db.query(Question).filter(Question.id == question_id).first()
        if question:
            trait = question.trait_type
            if trait in trait_scores:
                trait_scores[trait] += choice_weights.get(choice, 0.0)
                trait_counts[trait] += 1

    # 각 특성의 평균 점수 계산 (0-5 스케일로 정규화)
    normalized_scores = {}
    for trait in trait_scores:
        if trait_counts[trait] > 0:
            score = (trait_scores[trait] / trait_counts[trait]) * 5
            normalized_scores[trait] = round(score, 2)
        else:
            normalized_scores[trait] = 0.0

    return normalized_scores


def calculate_matching_score(user_traits: Dict[str, float], character_traits: Dict[str, float]) -> float:
    """
    코사인 유사도를 사용하여 사용자와 캐릭터 간의 매칭 점수를 계산합니다.

    Parameters:
        user_traits: 사용자의 특성 점수
        character_traits: 캐릭터의 특성 점수

    Returns:
        0-100 사이의 매칭 점수
    """
    dot_product = 0.0
    user_magnitude = 0.0
    character_magnitude = 0.0

    for trait in user_traits:
        user_value = user_traits[trait]
        character_value = float(character_traits.get(trait, 0))

        dot_product += user_value * character_value
        user_magnitude += user_value ** 2
        character_magnitude += character_value ** 2

    # 0으로 나누는 것을 방지
    if user_magnitude == 0 or character_magnitude == 0:
        return 0.0

    # 코사인 유사도 계산
    similarity = dot_product / (math.sqrt(user_magnitude) * math.sqrt(character_magnitude))

    # -1에서 1 사이의 값을 0-100 스케일로 변환
    score = (similarity + 1) * 50

    return round(score, 1)


def match_character(answers: Dict[int, int], db: Session):
    """
    사용자의 답변을 바탕으로 가장 잘 맞는 캐릭터를 찾습니다.

    Parameters:
        answers: 사용자의 답변
        db: 데이터베이스 세션
    """
    # 사용자의 특성 점수 계산
    user_traits = calculate_trait_scores(answers, db)

    # 모든 캐릭터와의 매칭 점수를 계산
    characters = db.query(Character, ResultTemplate)\
        .outerjoin(ResultTemplate, and_(
            Character.id == ResultTemplate.character_id,
            ResultTemplate.template_type.in_(['basic', 'modern', 'advice'])
        ))\
        .all()

    character_templates = {}
    for character, template in characters:
        if character.id not in character_templates:
            character_templates[character.id] = {
                'character': character,
                'templates': {},
                'score': 0  # 초기화
            }
        if template:  # template이 None이 아닌 경우에만
            character_templates[character.id]['templates'][template.template_type] = template


    matches = []
    for char_id, data in character_templates.items():
        score = calculate_matching_score(user_traits, data['character'].traits)
        data['score'] = score
        matches.append(data)

    matches.sort(key=lambda x: x['score'], reverse=True)
    best_match = matches[0]

    # 사용자의 가장 두드러진 특성 찾기
    top_traits = sorted(user_traits.items(), key=lambda x: x[1], reverse=True)[:2]

    # 특성 이름을 한글로 변환
    trait_names = {
        "courage": "용기",
        "loyalty": "충성",
        "wisdom": "지혜",
        "justice": "정의",
        "compassion": "연민",
        "determination": "의지"
    }

    # 사용자 특성 기반 설명 생성
    trait_description = f"당신은 {trait_names[top_traits[0][0]]}{get_josa(trait_names[top_traits[0][0]], ('과', '와'))} {trait_names[top_traits[1][0]]}{get_josa(trait_names[top_traits[1][0]], ('이', '가'))} 특히 돋보이는 사람입니다."

    # 각 타입별 템플릿 내용 가져오기
    templates = best_match['templates']
    basic_description = templates.get('basic').content if 'basic' in templates else best_match['character'].description
    modern_interpretation = templates.get('modern').content if 'modern' in templates else None
    advice = templates.get('advice').content if 'advice' in templates else None

    # 설명 조합
    full_description = f"{trait_description} {basic_description}"

    return {
        "character": {
            "id": best_match['character'].id,
            "name": best_match['character'].name,
            "work": best_match['character'].work,
            "description": best_match['character'].description,
            "image_url": best_match['character'].image_url,
            "media_url": best_match['character'].media_url,
        },
        "description": full_description,
        "modern_interpretation": modern_interpretation,
        "advice": advice,
    }
