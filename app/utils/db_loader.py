import csv
import json
from ..database import SessionLocal
from ..models.character import Character
from ..models.result_template import ResultTemplate
from ..models.question import Question
from pathlib import Path

def load_characters_from_csv():
    file_path = Path(__file__).parent.parent / "data" / "characters.csv"
    db = SessionLocal()
    try:
        # 먼저 테이블이 비어있는지 확인
        existing_count = db.query(Character).count()
        if existing_count > 0:
            print("Characters already exist in database. Skipping load.")
            return

        # 테이블이 비어있다면 데이터 로드
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                character = Character(
                    name=row['name'],
                    work=row['work'],
                    description=row['description'],
                    in_story=row['in_story'],
                    traits=json.loads(row['traits'].replace("'", '"')),
                    image_url=row.get('image_url'),
                    media_url=row.get('media_url'),
                )
                db.add(character)
            db.commit()
            print("Characters loaded successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error loading characters: {e}")
    finally:
        db.close()


def load_templates_from_csv():
    file_path = Path(__file__).parent.parent / "data" / "result_templates.csv"
    db = SessionLocal()
    try:
        # 먼저 테이블이 비어있는지 확인
        existing_count = db.query(ResultTemplate).count()
        if existing_count > 0:
            print("Templates already exist in database. Skipping load.")
            return

        # character_id가 실제로 존재하는지 확인하기 위한 모든 캐릭터 ID 가져오기
        existing_character_ids = {id[0] for id in db.query(Character.id).all()}

        # 테이블이 비어있다면 데이터 로드
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                character_id = int(row['character_id'])

                # character_id가 존재하는지 확인
                if character_id not in existing_character_ids:
                    print(f"Warning: Character ID {character_id} does not exist. Skipping template.")
                    continue

                template = ResultTemplate(
                    character_id=character_id,
                    template_type=row['template_type'],
                    content=row['content']
                )
                db.add(template)

            db.commit()
            print("Templates loaded successfully!")

    except FileNotFoundError:
        print(f"Error: Template CSV file not found at {file_path}")
    except csv.Error as e:
        print(f"Error reading CSV file: {e}")
    except Exception as e:
        db.rollback()
        print(f"Error loading templates: {e}")
    finally:
        db.close()


def load_questions_from_csv():
    file_path = Path(__file__).parent.parent / "data" / "questions.csv"
    db = SessionLocal()
    try:
        # 먼저 테이블이 비어있는지 확인
        existing_count = db.query(Question).count()
        if existing_count > 0:
            print("Questions already exist in database. Skipping load.")
            return

        # 테이블이 비어있다면 데이터 로드
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                character = Question(
                    content=row['content'],
                    choices=json.loads(row['choices'].replace("'", '"')),
                    trait_type=row['trait_type'],
                )
                db.add(character)
            db.commit()
            print("Questions loaded successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error loading characters: {e}")
    finally:
        db.close()


def init_db():
    load_characters_from_csv()  # 먼저 캐릭터 데이터 로드
    load_templates_from_csv()
    load_questions_from_csv()
