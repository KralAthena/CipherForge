import os
import random
import string

class TersCevirici:
    def ters_cevir(self, metin: str) -> str:
        return metin[::-1]

class SezarSifresi:
    def sifrele(self, metin: str, key: int) -> str:
        key = key % 26
        sonuc = ""
        for harf in metin:
            if harf.isalpha():
                baslangic = 65 if harf.isupper() else 97
                yeni = (ord(harf) - baslangic + key) % 26
                sonuc += chr(yeni + baslangic)
            else:
                sonuc += harf
        return sonuc

    def sifre_coz(self, metin: str, key: int) -> str:
        key = key % 26
        sonuc = ""
        for harf in metin:
            if harf.isalpha():
                baslangic = 65 if harf.isupper() else 97
                yeni = (ord(harf) - baslangic - key) % 26
                sonuc += chr(yeni + baslangic)
            else:
                sonuc += harf
        return sonuc

class VigenereSifresi:
    def sifrele(self, metin: str, anahtar_kelime: str) -> str:
        sonuc = []
        anahtar_kelime = anahtar_kelime.upper()
        anahtar_uzunlugu = len(anahtar_kelime)
        anahtar_index = 0
        for harf in metin:
            if harf.isalpha():
                baslangic = 65 if harf.isupper() else 97
                kaydirma = ord(anahtar_kelime[anahtar_index % anahtar_uzunlugu]) - 65
                yeni_harf = chr((ord(harf) - baslangic + kaydirma) % 26 + baslangic)
                sonuc.append(yeni_harf)
                anahtar_index += 1
            else:
                sonuc.append(harf)
        return "".join(sonuc)

    def sifre_coz(self, metin: str, anahtar_kelime: str) -> str:
        sonuc = []
        anahtar_kelime = anahtar_kelime.upper()
        anahtar_uzunlugu = len(anahtar_kelime)
        anahtar_index = 0
        for harf in metin:
            if harf.isalpha():
                baslangic = 65 if harf.isupper() else 97
                kaydirma = ord(anahtar_kelime[anahtar_index % anahtar_uzunlugu]) - 65
                yeni_harf = chr((ord(harf) - baslangic - kaydirma) % 26 + baslangic)
                sonuc.append(yeni_harf)
                anahtar_index += 1
            else:
                sonuc.append(harf)
        return "".join(sonuc)

class SifreCozucu:
    def brute_force(self, sifreli_metin: str) -> None:
        print(f"\n[+] Ele Geçirilen Şifreli Metin: {sifreli_metin}")
        print("-" * 65)
        print(f"{'Key'.ljust(6)} | {'Ters Metin (Sezar Çözülmüş)'.ljust(27)} | {'Düz Metin (Tam Çözülmüş)'}")
        print("-" * 65)
        ters_nesne = TersCevirici()
        sezar_nesne = SezarSifresi()
        for key in range(26):
            ters_hali = sezar_nesne.sifre_coz(sifreli_metin, key)
            duz_hali = ters_nesne.ters_cevir(ters_hali)
            print(f"Key {str(key).ljust(2)} | {ters_hali.ljust(27)} | {duz_hali}")
        print("-" * 65)

class SifreOlusturucu:
    def uret(self, uzunluk: int = 16) -> str:
        karakterler = string.ascii_letters + string.digits + "!@#$%^&*"
        return "".join(random.choice(karakterler) for _ in range(uzunluk))

class DosyaIslemleri:
    @staticmethod
    def dosya_oku(dosya_yolu: str) -> str:
        if not os.path.exists(dosya_yolu):
            print(f"[HATA] Dosya bulunamadı: {dosya_yolu}")
            return ""
        with open(dosya_yolu, "r", encoding="utf-8") as f:
            return f.read()
            
    @staticmethod
    def dosya_yaz(dosya_yolu: str, metin: str):
        with open(dosya_yolu, "w", encoding="utf-8") as f:
            f.write(metin)
        print(f"[BAŞARILI] İşlem tamamlandı. Dosya kaydedildi: {dosya_yolu}")

def main():
    while True:
        print("\n" + "="*55)
        print("    CIPHERFORGE - GELİŞMİŞ ŞİFRELEME VE GÜVENLİK SUİTİ")
        print("="*55)
        print("1. Klasik Sezar & Ters Çevirme (Şifrele/Çöz)")
        print("2. Vigenère Şifreleme (Gelişmiş)")
        print("3. Kaba Kuvvet (Brute-Force) Sezar Kırıcı")
        print("4. Güçlü Şifre Üretici (Password Generator)")
        print("5. Dosya Şifreleme Modülü (File I/O)")
        print("0. Çıkış")
        print("="*55)
        secim = input("Lütfen işleminizi seçiniz (0-5): ")

        if secim == "0":
            print("Çıkış yapılıyor... CipherForge güvenli günler diler.")
            break
        elif secim == "1":
            metin = input("Metni giriniz: ")
            try:
                anahtar = int(input("Öteleme anahtarı (0-25): "))
            except ValueError:
                print("[HATA] Anahtar sadece sayı olmalıdır!")
                continue
            islem = input("İşlem Seçin - Şifrele (1) / Çöz (2): ")
            t = TersCevirici()
            s = SezarSifresi()
            if islem == "1":
                print(f"[SONUÇ] Şifreli Metin: {s.sifrele(t.ters_cevir(metin), anahtar)}")
            elif islem == "2":
                print(f"[SONUÇ] Düz Metin: {t.ters_cevir(s.sifre_coz(metin, anahtar))}")
        elif secim == "2":
            metin = input("Metni giriniz: ")
            anahtar = input("Anahtar Kelime: ")
            islem = input("İşlem Seçin - Şifrele (1) / Çöz (2): ")
            v = VigenereSifresi()
            if islem == "1":
                print(f"[SONUÇ] Şifreli Metin: {v.sifrele(metin, anahtar)}")
            elif islem == "2":
                print(f"[SONUÇ] Düz Metin: {v.sifre_coz(metin, anahtar)}")
        elif secim == "3":
            sifreli = input("Şifreli metni giriniz: ")
            SifreCozucu().brute_force(sifreli)
        elif secim == "4":
            uzunluk_str = input("Şifre uzunluğu (Varsayılan 16): ")
            uzunluk = int(uzunluk_str) if uzunluk_str.isdigit() else 16
            print(f"\n[+] GÜVENLİ PAROLANIZ: {SifreOlusturucu().uret(uzunluk)}")
        elif secim == "5":
            dosya_yolu = input("\nOkunacak dosya adı: ")
            veri = DosyaIslemleri.dosya_oku(dosya_yolu)
            if not veri:
                continue
            print("\nYöntem: 1(Sezar) 2(Vigenère)")
            yontem = input("Seçiminiz: ")
            islem = input("Şifrele (1) / Çöz (2): ")
            if yontem == "1":
                try:
                    anahtar = int(input("Öteleme anahtarı: "))
                except ValueError:
                    continue
                t = TersCevirici()
                s = SezarSifresi()
                sonuc = s.sifrele(t.ters_cevir(veri), anahtar) if islem == "1" else t.ters_cevir(s.sifre_coz(veri, anahtar))
            elif yontem == "2":
                anahtar_kelime = input("Anahtar kelime: ")
                v = VigenereSifresi()
                sonuc = v.sifrele(veri, anahtar_kelime) if islem == "1" else v.sifre_coz(veri, anahtar_kelime)
            else:
                continue
            cikis_yolu = input("Kaydedilecek dosya adı: ")
            DosyaIslemleri.dosya_yaz(cikis_yolu, sonuc)
        else:
            print("[HATA] Geçersiz seçim.")

if __name__ == "__main__":
    main()