import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from pwdlib import PasswordHash

load_dotenv()

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
TOKEN_OMRU_DAKIKA = 30

sifre_hasher = PasswordHash.recommended()

def sifre_hashle(sifre: str) -> str:
    return sifre_hasher.hash(sifre)


def sifre_dogrula(sifre: str, sifre_hash: str) -> bool:
    return sifre_hasher.verify(sifre, sifre_hash)

def token_olustur(kullanici_id: int) -> str:
    bitis = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_OMRU_DAKIKA)
    veri = {"sub": str(kullanici_id), "exp": bitis}
    return jwt.encode(veri, SECRET_KEY, algorithm=ALGORITHM)