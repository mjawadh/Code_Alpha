import os
import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

# --- Base configuration ---
Base = declarative_base()

class TranslationCache(Base):
    __tablename__ = 'translations'
    id = Column(Integer, primary_key=True)
    source_text = Column(Text, nullable=False)
    translated_text = Column(Text, nullable=False)
    src_lang = Column(String(10), nullable=False)
    tgt_lang = Column(String(10), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

_cache_db_handler_instance = None

def _get_cache_db_handler():
    global _cache_db_handler_instance
    if _cache_db_handler_instance is None:
        _cache_db_handler_instance = CacheDBHandler()
    return _cache_db_handler_instance

def fetch_cached_translation(src_lang, tgt_lang, text):
    """Module-level cache fetcher for translation."""
    handler = _get_cache_db_handler()
    return handler.get_cached_translation(text, src_lang, tgt_lang)

def store_translation(src_lang, tgt_lang, text, translation):
    """Module-level cache storer for translation."""
    handler = _get_cache_db_handler()
    handler.add_translation(text, translation, src_lang, tgt_lang)

class CacheDBHandler:
    def __init__(self, db_path="cache/translation_cache.db", max_rows=1000, max_age_days=7):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.max_rows = max_rows
        self.max_age_days = max_age_days
        self.engine = create_engine(f"sqlite:///{db_path}", echo=False, connect_args={"check_same_thread": False})
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        """Create the translations table if it does not exist."""
        Base.metadata.create_all(self.engine)

    def _cleanup_old_entries(self, session):
        """Remove old or excess entries (both time- and size-based)."""
        try:
            cutoff = datetime.datetime.utcnow() - datetime.timedelta(days=self.max_age_days)
            session.query(TranslationCache).filter(TranslationCache.created_at < cutoff).delete()
            session.commit()

            # Size-based cleanup: keep only latest N rows
            total_rows = session.query(TranslationCache).count()
            if total_rows > self.max_rows:
                excess = total_rows - self.max_rows
                subq = session.query(TranslationCache.id).order_by(TranslationCache.created_at.asc()).limit(excess).subquery()
                session.query(TranslationCache).filter(TranslationCache.id.in_(subq)).delete(synchronize_session=False)
                session.commit()
        except SQLAlchemyError as e:
            print(f"[Cache Warning] Cleanup failed: {e}")

    def get_cached_translation(self, text, src_lang, tgt_lang):
        """Retrieve translation if cached."""
        with self.Session() as session:
            result = (
                session.query(TranslationCache)
                .filter_by(source_text=text, src_lang=src_lang, tgt_lang=tgt_lang)
                .order_by(TranslationCache.created_at.desc())
                .first()
            )
            return result.translated_text if result else None

    def add_translation(self, text, translation, src_lang, tgt_lang):
        """Insert translation into cache."""
        with self.Session() as session:
            try:
                new_entry = TranslationCache(
                    source_text=text,
                    translated_text=translation,
                    src_lang=src_lang,
                    tgt_lang=tgt_lang,
                )
                session.add(new_entry)
                session.commit()
                self._cleanup_old_entries(session)
            except SQLAlchemyError as e:
                print(f"[Cache Error] Failed to insert: {e}")
