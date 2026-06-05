from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database.engine import Base


class Pegawai(Base):
    __tablename__ = "pegawai"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nama = Column(String(255), nullable=False, index=True)
    nip = Column(String(20), unique=True, nullable=False, index=True)
    jabatan = Column(String(255), nullable=False, default="")
    pangkat_gol = Column(String(50), default="")
    instansi = Column(String(255), default="DPRD Kota Salatiga")
    komisi = Column(String(10), default="")
    no_hp = Column(String(20), default="")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    peserta_surat = relationship("PesertaSurat", back_populates="pegawai", cascade="all, delete-orphan")

    @property
    def display_name(self):
        return f"{self.nama} ({self.nip[-4:]})"

    def to_dict(self):
        return {
            "id": self.id,
            "nama": self.nama,
            "nip": self.nip,
            "jabatan": self.jabatan,
            "pangkat_gol": self.pangkat_gol,
            "instansi": self.instansi,
            "komisi": self.komisi,
            "no_hp": self.no_hp,
        }


class TemplateDokumen(Base):
    __tablename__ = "template_dokumen"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nama = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    deskripsi = Column(Text, default="")
    placeholders = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.now)

    surat = relationship("Surat", back_populates="template")

    def to_dict(self):
        return {
            "id": self.id,
            "nama": self.nama,
            "file_path": self.file_path,
            "deskripsi": self.deskripsi,
            "placeholders": self.placeholders or [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Surat(Base):
    __tablename__ = "surat"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nomor_surat = Column(String(100), nullable=False, unique=True)
    kode_surat = Column(String(20), nullable=False, default="")
    tanggal = Column(DateTime, default=datetime.now)
    template_id = Column(Integer, ForeignKey("template_dokumen.id"), nullable=True)
    data_json = Column(JSON, default=dict)
    file_path = Column(String(512), default="")
    created_at = Column(DateTime, default=datetime.now)

    template = relationship("TemplateDokumen", back_populates="surat")
    peserta = relationship("PesertaSurat", back_populates="surat", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "nomor_surat": self.nomor_surat,
            "kode_surat": self.kode_surat,
            "tanggal": self.tanggal.isoformat() if self.tanggal else None,
            "template_id": self.template_id,
            "file_path": self.file_path,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "peserta_count": len(self.peserta) if self.peserta else 0,
        }


class PesertaSurat(Base):
    __tablename__ = "peserta_surat"

    id = Column(Integer, primary_key=True, autoincrement=True)
    surat_id = Column(Integer, ForeignKey("surat.id", ondelete="CASCADE"), nullable=False)
    pegawai_id = Column(Integer, ForeignKey("pegawai.id", ondelete="CASCADE"), nullable=False)
    nomor_urut = Column(Integer, default=0)

    surat = relationship("Surat", back_populates="peserta")
    pegawai = relationship("Pegawai", back_populates="peserta_surat")

    def to_dict(self):
        return {
            "id": self.id,
            "surat_id": self.surat_id,
            "pegawai_id": self.pegawai_id,
            "nomor_urut": self.nomor_urut,
            "nama": self.pegawai.nama if self.pegawai else "",
            "nip": self.pegawai.nip if self.pegawai else "",
            "jabatan": self.pegawai.jabatan if self.pegawai else "",
            "pangkat_gol": self.pegawai.pangkat_gol if self.pegawai else "",
        }


class NomorCounter(Base):
    __tablename__ = "nomor_counter"

    id = Column(Integer, primary_key=True, autoincrement=True)
    kode_surat = Column(String(20), nullable=False)
    tahun = Column(Integer, nullable=False)
    counter = Column(Integer, default=0)

    @classmethod
    def get_next(cls, session, kode: str, tahun: int) -> int:
        from sqlalchemy import func
        counter = session.query(cls).filter_by(kode_surat=kode, tahun=tahun).with_for_update().first()
        if counter is None:
            counter = cls(kode_surat=kode, tahun=tahun, counter=1)
            session.add(counter)
        else:
            counter.counter += 1
        session.flush()
        return counter.counter
