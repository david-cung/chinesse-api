import sys
import os
import re
sys.path.append('.')

from sqlalchemy.orm import Session
from database.database import SessionLocal
from models import user, character, progress, unit, review, quiz, sentence
from models.lesson import Lesson, Vocabulary, VocabularyExample

def parse_example(legacy_example: str):
    """
    Parses legacy example strings into structured data.
    Format 1: "Chinese (pinyin) - Translation"
    Format 2: "Chinese - Translation"
    Format 3: "Chinese"
    """
    if not legacy_example:
        return None
    
    # Try to extract pinyin between parentheses
    pinyin_match = re.search(r'\(([^)]+)\)', legacy_example)
    pinyin = pinyin_match.group(1) if pinyin_match else None
    
    # Remove pinyin part from search for translation
    clean_text = re.sub(r'\([^)]+\)', '', legacy_example).strip()
    
    # Split by '-' to get translation
    parts = clean_text.split('-', 1)
    sentence = parts[0].strip()
    translation = parts[1].strip() if len(parts) > 1 else None
    
    return {
        "sentence": sentence,
        "pinyin": pinyin,
        "translation": translation
    }

def migrate_examples():
    db = SessionLocal()
    try:
        print("🚀 Starting Vocabulary Example Migration...")
        
        vocabularies = db.query(Vocabulary).all()
        migrated_count = 0
        skipped_count = 0
        
        for vocab in vocabularies:
            # Check if has legacy example AND no new examples
            if vocab.example and len(vocab.examples) == 0:
                # Basic parsing (could be improved with LLM or specific regex if needed)
                # But for now, let's use the simple parser
                ex_data = parse_example(vocab.example)
                
                if ex_data and ex_data["sentence"]:
                    new_ex = VocabularyExample(
                        vocabulary_id=vocab.id,
                        sentence=ex_data["sentence"],
                        pinyin=ex_data["pinyin"],
                        translation=ex_data["translation"],
                        order=1
                    )
                    db.add(new_ex)
                    migrated_count += 1
                    # print(f"   ✅ Migrated for '{vocab.word}': {ex_data['sentence']}")
            else:
                skipped_count += 1
        
        db.commit()
        print(f"\n✨ Migration Completed!")
        print(f"   - Migrated: {migrated_count} items")
        print(f"   - Skipped: {skipped_count} items (already has examples or no legacy data)")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error during migration: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    migrate_examples()
