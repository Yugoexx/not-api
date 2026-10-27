def kayit_ve_giris(client, kullanici_adi="ahmet", sifre="test-sifre-123"):
    client.post("/kayit", json={"kullanici_adi": kullanici_adi, "sifre": sifre})
    cevap = client.post(
        "/giris", data={"username": kullanici_adi, "password": sifre}
    )
    token = cevap.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_anasayfa(client):
    cevap = client.get("/")
    assert cevap.status_code == 200


def test_kayit_basarili_ve_sifre_donmez(client):
    cevap = client.post(
        "/kayit", json={"kullanici_adi": "ahmet", "sifre": "test-sifre-123"}
    )
    assert cevap.status_code == 201
    assert cevap.json()["kullanici_adi"] == "ahmet"
    assert "sifre" not in cevap.json()
    assert "sifre_hash" not in cevap.json()


def test_ayni_kullanici_adi_409_verir(client):
    veri = {"kullanici_adi": "ahmet", "sifre": "test-sifre-123"}
    client.post("/kayit", json=veri)
    cevap = client.post("/kayit", json=veri)
    assert cevap.status_code == 409


def test_yanlis_sifre_401_verir(client):
    client.post("/kayit", json={"kullanici_adi": "ahmet", "sifre": "dogru-sifre"})
    cevap = client.post(
        "/giris", data={"username": "ahmet", "password": "yanlis-sifre"}
    )
    assert cevap.status_code == 401


def test_notlar_tokensiz_401_verir(client):
    cevap = client.get("/notlar")
    assert cevap.status_code == 401


def test_not_olustur_ve_listele(client):
    basliklar = kayit_ve_giris(client)
    olustur = client.post(
        "/notlar",
        json={"baslik": "Alisveris", "icerik": "Sut, ekmek"},
        headers=basliklar,
    )
    assert olustur.status_code == 201

    liste = client.get("/notlar", headers=basliklar)
    assert liste.status_code == 200
    assert len(liste.json()) == 1
    assert liste.json()[0]["baslik"] == "Alisveris"


def test_baskasinin_notuna_erisilemez(client):
    ahmet = kayit_ve_giris(client, "ahmet", "ahmet-sifre-1")
    baska = kayit_ve_giris(client, "baska", "baska-sifre-1")

    olustur = client.post(
        "/notlar",
        json={"baslik": "Gizli", "icerik": "Sadece ahmet gorebilir"},
        headers=ahmet,
    )
    not_id = olustur.json()["id"]

    assert client.get(f"/notlar/{not_id}", headers=baska).status_code == 404
    assert client.delete(f"/notlar/{not_id}", headers=baska).status_code == 404
    assert client.get("/notlar", headers=baska).json() == []