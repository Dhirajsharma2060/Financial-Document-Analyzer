from sqlalchemy import Column, Integer, String, Text, DateTime
from db import Base
from datetime import datetime,timezone

class AnalysisResult(Base):
    __tablename__ = "analysis_results"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(String, index=True)
    query = Column(Text)
    file_processed = Column(String)
    analysis = Column(Text)
    result=Column(Text)
    file_id = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))