from typing import Optional, List
from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from app.database.engine import get_session
from app.database.models import Pegawai, TemplateDokumen, Surat, PesertaSurat, NomorCounter


class PegawaiRepo:
    @staticmethod
    def get_all(search: str = "", komisi: str = "") -> list[Pegawai]:
        session = get_session()
        try:
            q = session.query(Pegawai)
            if search:
                q = q.filter(
                    or_(
                        Pegawai.nama.ilike(f"%{search}%"),
                        Pegawai.nip.ilike(f"%{search}%"),
                        Pegawai.jabatan.ilike(f"%{search}%"),
                    )
                )
            if komisi:
                q = q.filter(Pegawai.komisi == komisi)
            return q.order_by(Pegawai.nama).all()
        finally:
            session.close()

    @staticmethod
    def get_by_id(pid: int) -> Optional[Pegawai]:
        session = get_session()
        try:
            return session.query(Pegawai).filter(Pegawai.id == pid).first()
        finally:
            session.close()

    @staticmethod
    def create(data: dict) -> Pegawai:
        session = get_session()
        try:
            p = Pegawai(**data)
            session.add(p)
            session.commit()
            session.refresh(p)
            return p
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def update(pid: int, data: dict) -> Optional[Pegawai]:
        session = get_session()
        try:
            p = session.query(Pegawai).filter(Pegawai.id == pid).first()
            if not p:
                return None
            for k, v in data.items():
                setattr(p, k, v)
            session.commit()
            session.refresh(p)
            return p
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def delete(pid: int) -> bool:
        session = get_session()
        try:
            p = session.query(Pegawai).filter(Pegawai.id == pid).first()
            if not p:
                return False
            session.delete(p)
            session.commit()
            return True
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def bulk_create(pegawai_list: list[dict]) -> list[Pegawai]:
        session = get_session()
        try:
            objs = [Pegawai(**d) for d in pegawai_list]
            session.add_all(objs)
            session.commit()
            for o in objs:
                session.refresh(o)
            return objs
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def count() -> int:
        session = get_session()
        try:
            return session.query(Pegawai).count()
        finally:
            session.close()


class TemplateRepo:
    @staticmethod
    def get_all() -> list[TemplateDokumen]:
        session = get_session()
        try:
            return session.query(TemplateDokumen).order_by(TemplateDokumen.created_at.desc()).all()
        finally:
            session.close()

    @staticmethod
    def get_by_id(tid: int) -> Optional[TemplateDokumen]:
        session = get_session()
        try:
            return session.query(TemplateDokumen).filter(TemplateDokumen.id == tid).first()
        finally:
            session.close()

    @staticmethod
    def create(data: dict) -> TemplateDokumen:
        session = get_session()
        try:
            t = TemplateDokumen(**data)
            session.add(t)
            session.commit()
            session.refresh(t)
            return t
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def delete(tid: int) -> bool:
        session = get_session()
        try:
            t = session.query(TemplateDokumen).filter(TemplateDokumen.id == tid).first()
            if not t:
                return False
            session.delete(t)
            session.commit()
            return True
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def count() -> int:
        session = get_session()
        try:
            return session.query(TemplateDokumen).count()
        finally:
            session.close()


class SuratRepo:
    @staticmethod
    def get_all(limit: int = 50) -> list[Surat]:
        session = get_session()
        try:
            return (
                session.query(Surat)
                .options(joinedload(Surat.template), joinedload(Surat.peserta))
                .order_by(Surat.created_at.desc())
                .limit(limit)
                .all()
            )
        finally:
            session.close()

    @staticmethod
    def get_by_id(sid: int) -> Optional[Surat]:
        session = get_session()
        try:
            return session.query(Surat).filter(Surat.id == sid).first()
        finally:
            session.close()

    @staticmethod
    def get_by_nomor(nomor_surat: str) -> Optional[Surat]:
        session = get_session()
        try:
            return session.query(Surat).filter(Surat.nomor_surat == nomor_surat).first()
        finally:
            session.close()

    @staticmethod
    def create(data: dict) -> Surat:
        session = get_session()
        try:
            s = Surat(**data)
            session.add(s)
            session.commit()
            session.refresh(s)
            return s
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def delete(sid: int) -> bool:
        session = get_session()
        try:
            s = session.query(Surat).filter(Surat.id == sid).first()
            if not s:
                return False
            session.delete(s)
            session.commit()
            return True
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def count() -> int:
        session = get_session()
        try:
            return session.query(Surat).count()
        finally:
            session.close()

    @staticmethod
    def count_today() -> int:
        from datetime import datetime, timedelta
        session = get_session()
        try:
            today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            return session.query(Surat).filter(Surat.created_at >= today_start).count()
        finally:
            session.close()


class PesertaSuratRepo:
    @staticmethod
    def create(data: dict) -> PesertaSurat:
        session = get_session()
        try:
            p = PesertaSurat(**data)
            session.add(p)
            session.commit()
            session.refresh(p)
            return p
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def bulk_create(peserta_list: list[dict]) -> list[PesertaSurat]:
        session = get_session()
        try:
            objs = [PesertaSurat(**d) for d in peserta_list]
            session.add_all(objs)
            session.commit()
            return objs
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def get_by_surat(surat_id: int) -> list[PesertaSurat]:
        session = get_session()
        try:
            return (
                session.query(PesertaSurat)
                .filter(PesertaSurat.surat_id == surat_id)
                .order_by(PesertaSurat.nomor_urut)
                .all()
            )
        finally:
            session.close()


class NomorCounterRepo:
    @staticmethod
    def get_next(kode: str, tahun: int) -> int:
        session = get_session()
        try:
            return NomorCounter.get_next(session, kode, tahun)
        finally:
            session.close()
