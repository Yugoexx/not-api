from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Not Api")

class NotGirdisi(BaseModel):
    baslik: str
    icerik: str


notlar: list[dict] = []
sonraki_id = 1


@app.get("/")
def anasayfa():
    return {"mesaj" : "Not Api çalışıyor"}


@app.post("/notlar", status_code=201)
def not_olustur(girdi: NotGirdisi):
    global sonraki_id
    yeni_not = {"id": sonraki_id, **girdi.model_dump()}
    notlar.append(yeni_not)
    sonraki_id += 1
    return yeni_not


@app.get("/notlar")
def notlari_listele():
    return notlar


def not_bul(not_id: int) -> dict:
    for n in notlar:
        if n["id"] == not_id:
            return n
    raise HTTPException(status_code=404, detail="Not bulunamadı")


@app.get("/notar/{not_id}")
def not_getir(not_id: int):
    return not_bul(not_id)


@app.put("/notar/{not_id}")
def notlari_güncelle(not_id: int, girdi: NotGirdisi):
    mevcut = not_bul(not_id)
    mevcut.update(girdi.model_dump())
    return mevcut

@app.delete("/notar/{not_id}", status_code=204)
def not_sil(not_id: int):
    notlar.remove(not_bul(not_id))