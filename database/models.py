from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(200), nullable=False)
    nip = Column(String(100), unique=True, nullable=False)
    pangkat_gol = Column(String(100), nullable=True)
    jabatan = Column(String(200), nullable=True)
    instansi = Column(String(200), nullable=True)
    komisi = Column(String(100), nullable=True)
    no_hp = Column(String(50), nullable=True)
    status = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(200), nullable=False)
    filename = Column(String(300), nullable=False)
    description = Column(String(500), nullable=True)
    placeholders = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class DocumentHistory(Base):
    __tablename__ = "document_history"

    id = Column(Integer, primary_key=True, index=True)
    dokumen_nama = Column(String(250), nullable=False)
    kategori = Column(String(100), nullable=False)
    path_docx = Column(String(500), nullable=False)
    path_pdf = Column(String(500), nullable=True)
    tanggal_generate = Column(DateTime, default=datetime.utcnow)
    data_json = Column(Text, nullable=True)
