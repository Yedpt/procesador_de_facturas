from sqlalchemy import Column, Integer, String, DateTime, func, JSON, Boolean, Text, ForeignKey
from pgvector.sqlalchemy import Vector
from app.config.database import Base

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    status = Column(String, nullable=False, default="pending")

    # Trazabilidad y payloads
    source = Column(String, nullable=True)  # native | ocr
    is_scanned = Column(Boolean, default=False)
    raw_text = Column(Text, nullable=True)
    extracted_data = Column(JSON, nullable=True)
    validation = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

class InvoiceTrace(Base):
    __tablename__ = "invoice_traces"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, nullable=False)
    step = Column(String, nullable=False)          # ingest | ocr | extract | validate | persist
    status = Column(String, nullable=False)        # ok | error
    message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class InvoiceEmbedding(Base):
    __tablename__ = "invoice_embeddings"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    chunk_id = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(768), nullable=False)
    metadata_json = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())