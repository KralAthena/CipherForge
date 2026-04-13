import os
import random
import string
import hashlib
from tkinter import filedialog, messagebox

try:
    import customtkinter as ctk
except ImportError:
    exit()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TersCevirici:
    def ters_cevir(self, metin): 
        return metin[::-1]

class SezarSifresi:
    def sifrele(self, metin, key):
        sonuc = ""
        for harf in metin:
            if harf.isalpha():
                baslangic = 65 if harf.isupper() else 97
                sonuc += chr((ord(harf) - baslangic + key) % 26 + baslangic)
            else:
                sonuc += harf
        return sonuc
        
    def sifre_coz(self, metin, key):
        sonuc = ""
        for harf in metin:
            if harf.isalpha():
                baslangic = 65 if harf.isupper() else 97
                sonuc += chr((ord(harf) - baslangic - key) % 26 + baslangic)
            else:
                sonuc += harf
        return sonuc

class VigenereSifresi:
    def sifrele(self, metin, anahtar):
        sonuc, anahtar, i = [], anahtar.upper(), 0
        if not anahtar: 
            return metin
            
        for harf in metin:
            if harf.isalpha():
                bas = 65 if harf.isupper() else 97
                k = ord(anahtar[i % len(anahtar)]) - 65
                sonuc.append(chr((ord(harf) - bas + k) % 26 + bas))
                i += 1
            else: 
                sonuc.append(harf)
        return "".join(sonuc)
        
    def sifre_coz(self, metin, anahtar):
        sonuc, anahtar, i = [], anahtar.upper(), 0
        if not anahtar: 
            return metin
            
        for harf in metin:
            if harf.isalpha():
                bas = 65 if harf.isupper() else 97
                k = ord(anahtar[i % len(anahtar)]) - 65
                sonuc.append(chr((ord(harf) - bas - k) % 26 + bas))
                i += 1
            else: 
                sonuc.append(harf)
        return "".join(sonuc)

class CipherForgeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CipherForge - Şifreleme ve Güvenlik Aracı")
        self.geometry("750x650")
        self.resizable(False, False)
        
        self.ust_baslik = ctk.CTkLabel(self, text="CipherForge v3.0", font=ctk.CTkFont(size=26, weight="bold"))
        self.ust_baslik.pack(pady=15)
        
        self.sekmeler = ctk.CTkTabview(self, width=700, height=520)
        self.sekmeler.pack(padx=20, pady=10)
        
        self.sekmeler.add("Metin Şifreleme")
        self.sekmeler.add("Şifre Kırıcı")
        self.sekmeler.add("Dosya Şifreleme")
        self.sekmeler.add("Parola Üretici")
        
        self.islem_sekmesini_kur()
        self.kiri_sekmesini_kur()
        self.dosya_sekmesini_kur()
        self.parola_sekmesini_kur()
        
    def islem_sekmesini_kur(self):
        tab = self.sekmeler.tab("Metin Şifreleme")
        
        self.algoritma_sec = ctk.CTkOptionMenu(tab, values=["Sezar & Ters Çevir", "Vigenère Şifreleme", "SHA-256 (Özet)"], width=500, height=35)
        self.algoritma_sec.pack(pady=10)
        self.algoritma_sec.set("Vigenère Şifreleme")
        
        self.giris_metni = ctk.CTkEntry(tab, placeholder_text="Şifrelenecek veya çözülecek metni girin...", width=500, height=40)
        self.giris_metni.pack(pady=10)
        
        self.anahtar_girisi = ctk.CTkEntry(tab, placeholder_text="Anahtar kelime ya da sayı girin...", width=500, height=40)
        self.anahtar_girisi.pack(pady=10)
        
        buton_alani = ctk.CTkFrame(tab, fg_color="transparent")
        buton_alani.pack(pady=10)
        
        ctk.CTkButton(buton_alani, text="Şifrele", command=lambda: self.sifreleme_islemi("sifrele"), fg_color="#28a745", hover_color="#218838", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=15)
        ctk.CTkButton(buton_alani, text="Şifre Çöz", command=lambda: self.sifreleme_islemi("coz"), fg_color="#dc3545", hover_color="#c82333", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, padx=15)
        
        self.sonuc_ekrani = ctk.CTkTextbox(tab, width=500, height=180, font=ctk.CTkFont(size=14))
        self.sonuc_ekrani.pack(pady=10)
        
    def sifreleme_islemi(self, islem_turu):
        secilen_algoritma = self.algoritma_sec.get()
        metin = self.giris_metni.get()
        anahtar_degeri = self.anahtar_girisi.get()
        
        if not metin:
            messagebox.showerror("Hata", "Lütfen bir metin girin!")
            return
            
        if secilen_algoritma == "SHA-256 (Özet)":
            if islem_turu == "coz":
                sonuc = "SHA-256 algoritmaları geriye çözülemez, bu işlem sadece metni tek yönlü özetlemek içindir."
            else:
                sonuc = hashlib.sha256(metin.encode('utf-8')).hexdigest()
                
        elif secilen_algoritma == "Sezar & Ters Çevir":
            try:
                sayisal_anahtar = int(anahtar_degeri) if anahtar_degeri else 0
            except ValueError:
                messagebox.showerror("Hata", "Sezar şifrelemesinde anahtar mutlaka sayı olmalıdır!")
                return
                
            t_objesi = TersCevirici()
            s_objesi = SezarSifresi()
            
            if islem_turu == "sifrele":
                sonuc = s_objesi.sifrele(t_objesi.ters_cevir(metin), sayisal_anahtar)
            else:
                sonuc = t_objesi.ters_cevir(s_objesi.sifre_coz(metin, sayisal_anahtar))
        else:
            v_objesi = VigenereSifresi()
            if not anahtar_degeri:
                messagebox.showwarning("Uyarı", "Vigenère için bir anahtar kelime girmelisiniz.")
                return
            if islem_turu == "sifrele":
                sonuc = v_objesi.sifrele(metin, anahtar_degeri)
            else:
                sonuc = v_objesi.sifre_coz(metin, anahtar_degeri)
                
        self.sonuc_ekrani.delete("0.0", "end")
        self.sonuc_ekrani.insert("0.0", sonuc)

    def kiri_sekmesini_kur(self):
        tab = self.sekmeler.tab("Şifre Kırıcı")
        
        ctk.CTkLabel(tab, text="Kırılacak Sezar şifreli metni aşağıya yapıştırın:", font=ctk.CTkFont(size=14)).pack(pady=10)
        
        self.kirilacak_metin = ctk.CTkEntry(tab, width=500, height=40)
        self.kirilacak_metin.pack(pady=5)
        
        ctk.CTkButton(tab, text="Tarama Başlat (Brute-Force)", command=self.kirici_calistir, fg_color="#ff8c00", hover_color="#e07b00", height=40).pack(pady=15)
        
        self.kirilan_sonuclar = ctk.CTkTextbox(tab, width=600, height=270, font=ctk.CTkFont(family="Courier", size=13))
        self.kirilan_sonuclar.pack(pady=5)
        
    def kirici_calistir(self):
        sifreli = self.kirilacak_metin.get()
        if not sifreli:
            return
            
        self.kirilan_sonuclar.delete("0.0", "end")
        
        t_obj = TersCevirici()
        s_obj = SezarSifresi()
        
        rapor = "KABA KUVVET SONUÇLARI:\n------------------------------------------------------------\n"
        for deneme in range(26):
            cozulmus = t_obj.ters_cevir(s_obj.sifre_coz(sifreli, deneme))
            rapor += f"Anahtar {str(deneme).ljust(2)} | Sonuç: {cozulmus}\n"
            
        self.kirilan_sonuclar.insert("0.0", rapor)

    def dosya_sekmesini_kur(self):
        tab = self.sekmeler.tab("Dosya Şifreleme")
        
        ctk.CTkLabel(tab, text="İşlem yapmak istediğiniz metin belgesini seçin:", font=ctk.CTkFont(size=13)).pack(pady=(20, 5))
        
        self.dosya_yolu_kutusu = ctk.CTkEntry(tab, width=500, height=35)
        self.dosya_yolu_kutusu.pack(pady=5)
        
        ctk.CTkButton(tab, text="Gözat...", command=self.dosya_arayici, fg_color="#343a40", hover_color="#23272b").pack(pady=5)
        
        self.dosya_algoritmasi = ctk.CTkOptionMenu(tab, values=["Sezar", "Vigenère"], width=250)
        self.dosya_algoritmasi.pack(pady=(20, 5))
        
        self.dosya_anahtari = ctk.CTkEntry(tab, placeholder_text="Dosya kilidi için anahtar...", width=250)
        self.dosya_anahtari.pack(pady=5)
        
        butonlar = ctk.CTkFrame(tab, fg_color="transparent")
        butonlar.pack(pady=20)
        
        ctk.CTkButton(butonlar, text="Dosyayı Şifrele", command=lambda: self.dosya_kaydet("sifrele")).grid(row=0, column=0, padx=10)
        ctk.CTkButton(butonlar, text="Dosyayı Çöz", command=lambda: self.dosya_kaydet("coz"), fg_color="#dc3545").grid(row=0, column=1, padx=10)
        
        self.dosya_bildirim = ctk.CTkLabel(tab, text="", font=ctk.CTkFont(weight="bold"))
        self.dosya_bildirim.pack()

    def dosya_arayici(self):
        secilen_dosya = filedialog.askopenfilename(title="Dosya Seç", filetypes=[("Metin Dosyaları", "*.txt"), ("Tüm Dosyalar", "*.*")])
        if secilen_dosya:
            self.dosya_yolu_kutusu.delete("0", "end")
            self.dosya_yolu_kutusu.insert("0", secilen_dosya)

    def dosya_kaydet(self, yon):
        yol = self.dosya_yolu_kutusu.get()
        if not os.path.exists(yol):
            self.dosya_bildirim.configure(text="Dosya yolu geçersiz veya boş!", text_color="red")
            return
            
        try:
            with open(yol, "r", encoding="utf-8") as f:
                icerik = f.read()
        except:
            self.dosya_bildirim.configure(text="Dosya okunamadı, formatı hatalı olabilir.", text_color="red")
            return
            
        alg = self.dosya_algoritmasi.get()
        ak = self.dosya_anahtari.get()
        
        if alg == "Sezar":
            s_obj, t_obj = SezarSifresi(), TersCevirici()
            k = int(ak) if ak.isdigit() else 0
            yeni_icerik = s_obj.sifrele(t_obj.ters_cevir(icerik), k) if yon == "sifrele" else t_obj.ters_cevir(s_obj.sifre_coz(icerik, k))
        else:
            v_obj = VigenereSifresi()
            yeni_icerik = v_obj.sifrele(icerik, ak) if yon == "sifrele" else v_obj.sifre_coz(icerik, ak)
            
        yeni_dosya_yolu = yol + (".sifreli.txt" if yon=="sifrele" else ".cozuldu.txt")
        try:
            with open(yeni_dosya_yolu, "w", encoding="utf-8") as f:
                f.write(yeni_icerik)
            self.dosya_bildirim.configure(text=f"İşlem tamam!\nKaydedilen yer: {yeni_dosya_yolu}", text_color="#28a745")
        except:
            self.dosya_bildirim.configure(text="Dosya yazılırken bir hata oluştu.", text_color="red")

    def parola_sekmesini_kur(self):
        tab = self.sekmeler.tab("Parola Üretici")
        
        self.slider_metni = ctk.CTkLabel(tab, text="16 Karakter Uzunluk", font=ctk.CTkFont(size=18, weight="bold"))
        self.slider_metni.pack(pady=(40, 10))
        
        self.parola_slider = ctk.CTkSlider(tab, from_=8, to=128, number_of_steps=120, command=lambda v: self.slider_metni.configure(text=f"{int(v)} Karakter Uzunluk"))
        self.parola_slider.set(16)
        self.parola_slider.pack(fill="x", padx=100)
        
        ctk.CTkButton(tab, text="Rastgele Güvenli Parola Üret", command=self.parola_yarat, height=45, fg_color="#17a2b8", hover_color="#138496").pack(pady=30)
        
        self.uretilen_parola_kutusu = ctk.CTkEntry(tab, width=600, justify="center", font=ctk.CTkFont(size=22, weight="bold"))
        self.uretilen_parola_kutusu.pack(pady=10)

    def parola_yarat(self):
        uzunluk = int(self.parola_slider.get())
        rastgele_karakterler = string.ascii_letters + string.digits + "!@#$%^&*-=_+"
        kilit = "".join(random.choice(rastgele_karakterler) for _ in range(uzunluk))
        
        self.uretilen_parola_kutusu.delete(0, "end")
        self.uretilen_parola_kutusu.insert(0, kilit)

if __name__ == "__main__":
    uygulama = CipherForgeApp()
    uygulama.mainloop()
