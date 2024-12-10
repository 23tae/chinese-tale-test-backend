from typing import Dict

def normalize_scores(scores: Dict[str, float]) -> Dict[str, float]:
    """점수를 0-1 범위로 정규화"""
    max_score = max(scores.values())
    if max_score == 0:
        return scores
    return {k: v/max_score for k, v in scores.items()}

def validate_answers(answers: Dict[int, int]) -> bool:
    """사용자 답변 유효성 검사"""
    if not answers:
        return False
    return all(isinstance(q, int) and isinstance(a, int) for q, a in answers.items())