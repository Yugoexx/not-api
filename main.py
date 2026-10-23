from fastapi import FastAPI

app = FastAPI(title="Not Api")

@app.get("/")
def anasayfa():
    return {"mesaj" : "Not Api çalışıyor"}
    