"""
EONIX Preference Store — User preferences CRUD.
"""
from typing import Dict, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from .db import Preference


def get_preference(db: Session, key: str, default: Optional[str] = None) -> Optional[str]:
    pref = db.query(Preference).filter(Preference.key == key).first()
    return pref.value if pref else default


def set_preference(db: Session, key: str, value: str, source: str = "user") -> Preference:
    pref = db.query(Preference).filter(Preference.key == key).first()
    if pref:
        pref.value = value
        pref.source = source
        pref.updated_at = datetime.utcnow()
    else:
        pref = Preference(key=key, value=value, source=source)
        db.add(pref)
    db.commit()
    db.refresh(pref)
    return pref


def get_all_preferences(db: Session) -> Dict[str, str]:
    prefs = db.query(Preference).all()
    return {p.key: p.value for p in prefs}


def delete_preference(db: Session, key: str) -> bool:
    pref = db.query(Preference).filter(Preference.key == key).first()
    if not pref:
        return False
    db.delete(pref)
    db.commit()
    return True
