from pwdlib import PasswordHash

sifre_hasher = PasswordHash.recommended()


def sifre_hashle(sifre: str) -> str:
    return sifre_hasher.hash(sifre)


def sifre_dogrula(sifre: str, sifre_hash: str) -> bool:
    return sifre_hasher.verify(sifre, sifre_hash)