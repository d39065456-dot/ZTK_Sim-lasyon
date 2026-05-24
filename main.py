import random
import json
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

# Tablet klavyesinin ekranı kapatmasını önleme ayarı
Window.softinput_mode = "below_target"

class ZTKApp(App):
    def build(self):
        self.title = "Ziraat Türkiye Kupası Simülasyonu"
        self.state = {"current_stage": "start", "data": {}}
        
        # Ana Arayüz (Tablet ekranına uygun dikey yerleşim)
        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Maç Sonuçları Gösterim Alanı (Kaydırılabilir)
        self.scroll = ScrollView(size_hint=(1, 0.75))
        self.log_label = Label(
            text="🏆 ZİRAAT TÜRKİYE KUPASI SİMÜLASYONU BAŞLIYOR...\n\n", 
            size_hint_y=None, 
            halign="left", 
            valign="top", 
            font_size='18sp'
        )
        self.log_label.bind(texture_size=self.log_label.setter('size'))
        self.scroll.add_widget(self.log_label)
        self.main_layout.add_widget(self.scroll)
        
        # Alt Panel: Skor Girişi ve Onay Butonu
        self.input_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.15), spacing=10)
        self.score_input = TextInput(hint_text="Skor girin (Örn: 2-1)", multiline=False, font_size='20sp', size_hint=(0.7, 1))
        self.submit_btn = Button(text="Onayla", size_hint=(0.3, 1), font_size='18sp', on_press=self.process_input)
        self.input_layout.add_widget(self.score_input)
        self.input_layout.add_widget(self.submit_btn)
        self.main_layout.add_widget(self.input_layout)
        
        # Turnuva Değişkenleri
        self.current_matches = []
        self.current_match_index = 0
        self.winners = []
        self.byes = []
        
        self.start_next_stage()
        return self.main_layout

    def log(self, text):
        self.log_label.text += text + "\n"
        self.scroll.scroll_y = 0

    def get_team_name(self, rank: int) -> str:
        # Kodundaki orijinal takımların birebir listesi
        rank_to_info = {
            1: "GALATASARAY A.Ş.", 2: "FENERBAHÇE A.Ş.", 3: "TRABZONSPOR A.Ş.", 4: "BEŞİKTAŞ A.Ş.",
            5: "RAMS BAŞAKŞEHİR FK", 6: "GÖZTEPE A.Ş.", 7: "SAMSUNSPOR A.Ş.", 8: "KOCAELİSPOR",
            9: "GAZİANTEP FK", 10: "CORENDON ALANYASPOR", 11: "ÇAYKUR RİZESPOR A.Ş.", 12: "TÜMOSAN KONYASPOR",
            13: "GENÇLERBİRLİĞİ", 14: "ANTALYASPOR", 15: "KASIMPAŞA A.Ş.", 16: "KAYSERİSPOR",
            17: "İKAS EYÜPSPOR", 18: "FATİH KARAGÜMRÜK", 19: "Erzurumspor FK", 20: "Amed Sportif",
            21: "Esenler Erokspor", 22: "Arca Çorum FK", 23: "Sipay Bodrum FK", 24: "Pendikspor",
            25: "Bandırmaspor", 26: "Ankara Keçiörengücü", 27: "Özbelsan Sivasspor", 28: "Iğdır FK",
            29: "Van Spor FK", 30: "Manisa FK", 31: "Boluspor", 32: "Ümraniyespor",
            33: "Sarıyerspor", 34: "İstanbulspor A.Ş.", 35: "Serik Spor", 36: "Sakaryaspor A.Ş.",
            37: "Atakaş Hatayspor", 38: "Adana Demirspor A.Ş.", 39: "Batman Petrol Spor", 40: "Bursaspor",
            41: "Muğlaspor Kulübü", 42: "Mardin 1969 Spor", 43: "Adana 01 FK", 44: "Aliağa Futbol A.Ş.",
            45: "Seza Çimento Elazığspor", 46: "Muş Spor Kulübü", 47: "Şanlıurfaspor", 48: "Kahramanmaraş İstiklal",
            49: "Sultan Su İnegölspor", 50: "Gebze Spor Kulübü", 51: "İskenderunspor A.Ş.", 52: "Isparta 32 Spor",
            53: "MKE Ankaragücü", 54: "Ankara Demirspor", 55: "Ankaraspor", 56: "Menemen FK",
            57: "24Erzincanspor", 58: "68 Aksaray Belediye", 59: "Beyoğlu Yeni Çarşı", 60: "1461 Trabzon FK",
            61: "GMG Kastamonuspor", 62: "Fethiyespor", 63: "Erbaaspor", 64: "Arnavutköy Belediyesi",
            65: "Karacabey Belediye", 66: "Kırklarelispor", 67: "Altınordu", 68: "Somaspor",
            69: "Beykoz Anadolu Spor", 70: "Yeni Mersin İdmanyurdu", 71: "Kepez Spor Futbol", 72: "Adanaspor A.Ş.",
            73: "Karaman FK", 74: "Yeni Malatyaspor", 75: "Bucaspor 1928", 76: "İnegöl Kafkas Spor",
            77: "12 Bingöl Spor", 78: "Sebat Gençlik Spor", 79: "Kütahyaspor", 80: "Çorlu Spor 1947",
            81: "Silifke Belediye Spor", 82: "52 Orduspor FK", 83: "Eskişehirspor Kulübü", 84: "Küçükçekmece Sinop",
            85: "Mazıdağı Fosfat Spor", 86: "Kdz. Ereğli Belediye", 87: "Karşıyaka", 88: "Bursa Yıldırım Spor",
            89: "Karaköprü Belediye", 90: "Yozgat Bld. Bozok", 91: "Ayvalıkücü Belediyespor", 92: "Etimesgut Spor",
            93: "Erciyes 38 Futbol", 94: "Fatsa Belediyespor", 95: "Balıkesirspor", 96: "Silivrispor",
            97: "Ağrı 1970 Spor Kulübü", 98: "Zonguldak Spor FK", 99: "Denizli İdmanyurdu", 100: "Yalova FK 77",
            101: "Osmaniyespor", 102: "Düzce Cam Düzcespor", 103: "Uşak Spor A.Ş.", 104: "Galata Spor Kulübü",
            105: "Niğde Belediyesi Spor", 106: "Pazarspor", 107: "Tire 2021 FK", 108: "Bulvarspor",
            109: "Malatya Yeşilyurt", 110: "Karabük İdmanyurdu", 111: "Alanya 1221 FK", 112: "Beykoz İshaklı Spor",
            113: "Kırıkkale FK", 114: "Orduspor 1967 A.Ş.", 115: "Eskişehir Anadolu Spor", 116: "İnkılap Futbol SK",
            117: "Kırşehir Futbol SK", 118: "Tokat Belediye Spor", 119: "Söke 1970 Spor Kulübü", 120: "Bursa Nilüfer A.Ş.",
            121: "Diyarbekir Spor A.Ş.", 122: "Amasyaspor FK", 123: "Altay", 124: "Çankaya Spor Kulübü",
            125: "Kilis 1984 A.Ş.", 126: "Artvin Hopaspor", 127: "Bornova 1877", 128: "Kestel Çilek Spor",
            129: "Kahramanmaraşspor", 130: "1926 Bulancakspor", 131: "Afyonspor Kulübü", 132: "Polatlı 1926 Spor",
            133: "Suvermez Kapadokya", 134: "Çayeli Spor Kulübü", 135: "İzmir Çoruhlu FK", 136: "Edirnespor",
            137: "Türk Metal 1963", 138: "Giresunspor", 139: "Nazilli Spor A.Ş.", 140: "Kahta 02 SK",
            141: "Bayburt İl Özel İdare", 142: "Bucak Bld. Oğuzhanspor", 143: "Gümüşhane Sportif", 144: "Siirtspor",
            145: "Dersim Spor", 146: "Serhat Ardahanspor", 147: "Söğütspor", 148: "Ezinespor",
            149: "Biga Spor", 150: "Yüksekova Belediyespor", 151: "Cizre Spor", 152: "Şırnak Petrol Spor",
            153: "Sinopspor", 154: "Bartınspor", 155: "Tatvan Spor", 156: "Çankırıspor", 157: "Kars 36 Spor"
        }
        return rank_to_info.get(rank, f"Takım {rank}")

    def start_next_stage(self):
        stage = self.state["current_stage"]
        if stage == "start":
            self.log("🔥 1. Tur (128-157) Başlıyor...")
            self.setup_knockout(list(range(128, 158)))
        elif stage == "qual2":
            self.log("🔥 2. Tur Başlıyor...")
            self.setup_knockout(list(range(72, 128)) + self.state["data"]["qual1_winners"])
        elif stage == "qual3":
            self.log("🔥 3. Tur Başlıyor...")
            self.setup_knockout(list(range(12, 72)) + self.state["data"]["qual2_winners"])
        elif stage == "playoff":
            self.log("🔥 Playoff Turu Başlıyor...")
            self.setup_knockout(list(range(6, 12)) + self.state["data"]["qual3_winners"])
        elif stage == "groups":
            self.log("🎉 GRUP AŞAMASI VE SONRASI GEÇİLDİ! Simülasyon tamamlandı.")
            self.submit_btn.disabled = True
            self.score_input.disabled = True

    def setup_knockout(self, participants):
        sorted_part = sorted(participants)
        self.winners = []
        self.byes = []
        
        if len(sorted_part) % 2 == 1:
            bye_rank = sorted_part.pop()
            self.byes.append(bye_rank)
            self.log(f"👋 {self.get_team_name(bye_rank)} maç yapmadan (BYE) üst tura çıktı.\n")
            
        half = len(sorted_part) // 2
        seeded = sorted_part[:half]
        unseeded = sorted_part[half:]
        random.shuffle(unseeded)
        
        self.current_matches = list(zip(seeded, unseeded))
        self.current_match_index = 0
        self.ask_next_match()

    def ask_next_match(self):
        if self.current_match_index < len(self.current_matches):
            home, away = self.current_matches[self.current_match_index]
            self.log(f"⚽ Eşleşme {self.current_match_index + 1}: {self.get_team_name(home)} vs {self.get_team_name(away)}")
        else:
            self.winners.extend(self.byes)
            stage = self.state["current_stage"]
            if stage == "start":
                self.state["data"]["qual1_winners"] = self.winners
                self.state["current_stage"] = "qual2"
            elif stage == "qual2":
                self.state["data"]["qual2_winners"] = self.winners
                self.state["current_stage"] = "qual3"
            elif stage == "qual3":
                self.state["data"]["qual3_winners"] = self.winners
                self.state["current_stage"] = "playoff"
            elif stage == "playoff":
                self.state["current_stage"] = "groups"
                
            self.log(f"✅ Aşama bitti! {len(self.winners)} takım üst tura çıktı.\n" + "="*40 + "\n")
            self.start_next_stage()

    def process_input(self, instance):
        text = self.score_input.text.strip()
        if not text:
            return
            
        for sep in ['-', ' ', ',', ';', '/', 'x']:
            text = text.replace(sep, ' ')
        parts = text.split()
        
        if len(parts) != 2:
            self.log("❌ Hatalı skor! '2-1' veya '2 1' gibi girin.")
            return
            
        try:
            h, a = int(parts[0]), int(parts[1])
            home, away = self.current_matches[self.current_match_index]
            
            if h > a:
                self.winners.append(home)
                self.log(f"🟢 Kazanan: {self.get_team_name(home)}\n")
            elif a > h:
                self.winners.append(away)
                self.log(f"🟢 Kazanan: {self.get_team_name(away)}\n")
            else:
                self.log("⚠️ Maç berabere bitemez! Penaltı/uzatma dahil kazanan skoru girin.")
                return
                
            self.score_input.text = ""
            self.current_match_index += 1
            self.ask_next_match()
        except ValueError:
            self.log("❌ Sadece sayı girin.")

if __name__ == "__main__":
    ZTKApp().run()
