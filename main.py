from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Not

from models import Kullanici, Not
from guvenlik import sifre_hashle

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Not Api")

class NotGirdisi(BaseModel):
    baslik: str
    icerik: str

class NotCikti(NotGirdisi):
    model_config = ConfigDict(from_attributes=True)
    id: int

class KullaniciGirdisi(BaseModel):
    kullanici_adi: str
    sifre: str

class KullaniciCikti(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    kullanici_adi: str

@app.get("/")
def anasayfa():
    return {"mesaj" : "Not Api çalışıyor"}


@app.post("/notlar", status_code=201, response_model=NotCikti)
def not_olustur(girdi: NotGirdisi, db: Session = Depends(get_db)):
    yeni_not = Not(**girdi.model_dump())
    db.add(yeni_not)
    db.commit()
    db.refresh(yeni_not)
    return yeni_not


@app.get("/notlar", response_model=list[NotCikti])
def notlari_listele(db: Session = Depends(get_db)):
    return db.scalars(select(Not)).all()


def not_bul(not_id: int, db: Session) -> Not:
    bulunan = db.get(Not, not_id)
    if bulunan is None:
        raise HTTPException(status_code=404, detail="Not bulunamadı")
    return bulunan



@app.get("/notlar/{not_id}", response_model=NotCikti)
def not_getir(not_id: int, db: Session = Depends(get_db)):
    return not_bul(not_id, db)


@app.put("/notlar/{not_id}", response_model=NotCikti)
def notu_guncelle(not_id: int, girdi: NotGirdisi, db: Session = Depends(get_db)):
    mevcut = not_bul(not_id, db)
    mevcut.baslik = girdi.baslik
    mevcut.icerik = girdi.icerik
    db.commit()
    db.refresh(mevcut)
    return mevcut


@app.delete("/notlar/{not_id}", status_code=204)
def not_sil(not_id: int, db: Session = Depends(get_db)):
    db.delete(not_bul(not_id, db))
    db.commit()


@app.post("/kayit", status_code=201, response_model=KullaniciCikti)
def kayit_ol(girdi: KullaniciGirdisi, db: Session = Depends(get_db)):
    mevcut = db.scalar(
        select(Kullanici).where(Kullanici.kullanici_adi == girdi.kullanici_adi)
    )
    if mevcut is not None:
        raise HTTPException(status_code=409, detail="Bu kullanıcı adı alınmış")

    yeni = Kullanici(
        kullanici_adi=girdi.kullanici_adi,
        sifre_hash=sifre_hashle(girdi.sifre),
    )
    db.add(yeni)
    db.commit()
    db.refresh(yeni)
    return yeni