from fastapi import FastAPI

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
    sonrak_id += 1
    return yeni_not


@app.get("/notlar")
def notlari_listele():
    return notlar
