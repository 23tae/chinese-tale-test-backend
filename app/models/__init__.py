from sqlalchemy.orm import relationship
from .character import Character
from .result_template import ResultTemplate

# 관계 설정을 여기서 한 번에 정의
Character.templates = relationship("ResultTemplate", back_populates="character")
ResultTemplate.character = relationship("Character", back_populates="templates")

# 모델들을 패키지 레벨로 노출
__all__ = ['Character', 'ResultTemplate']