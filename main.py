import random
import json
import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.core.window import Window

# Pencere boyutunu masaüstü için sabitleyelim
Window.size = (800, 700)

SAVE_FILE = "ziraat_turkiye_kupasi_state.json"

# === TAKIM VERİLERİ ===
RANK_TO_INFO = {
    1: {"name": "GALATASARAY A.Ş."}, 2: {"name": "FENERBAHÇE A.Ş."},
    3: {"name": "TRABZONSPOR A.Ş."}, 4: {"name": "BEŞİKTAŞ A.Ş."},
    5: {"name": "RAMS BAŞAKŞEHİR FUTBOL KULÜBÜ"}, 6: {"name": "GÖZTEPE A.Ş."},
    7: {"name": "SAMSUNSPOR A.Ş."}, 8: {"name": "KOCAELİSPOR"},
    9: {"name": "GAZİANTEP FUTBOL KULÜBÜ A.Ş."}, 10: {"name": "CORENDON ALANYASPOR"},
    11: {"name": "ÇAYKUR RİZESPOR A.Ş."}, 12: {"name": "TÜMOSAN KONYASPOR"},
    13: {"name": "NATURA DÜNYASI GENÇLERBİRLİĞİ"}, 14: {"name": "HESAP.COM ANTALYASPOR"},
    15: {"name": "KASIMPAŞA A.Ş."}, 16: {"name": "ZECORNER KAYSERİSPOR"},
    17: {"name": "İKAS EYÜPSPOR"}, 18: {"name": "MISIRLI.COM.TR FATİH KARAGÜMRÜK"},
    19: {"name": "Erzurumspor FK"}, 20: {"name": "Amed Sportif Faaliyetler"},
    21: {"name": "Esenler Erokspor"}, 22: {"name": "Arca Çorum FK"},
    23: {"name": "Sipay Bodrum FK"}, 24: {"name": "Atko Grup Pendikspor Futbol A.Ş."},
    25: {"name": "Bandırmaspor"}, 26: {"name": "Emre Gökdemir İnşaat Ankara Keçiörengücü"},
    27: {"name": "Özbelsan Sivasspor"}, 28: {"name": "Alagöz Holding Iğdır FK"},
    29: {"name": "İmaj Altyapı Van Spor Futbol Kulübü"}, 30: {"name": "Manisa Futbol Kulübü"},
    31: {"name": "Boluspor"}, 32: {"name": "Eminevim Ümraniyespor"},
    33: {"name": "SMS Grup Sarıyerspor"}, 34: {"name": "İstanbulspor A.Ş."},
    35: {"name": "Serik Spor Futbol A.Ş."}, 36: {"name": "Sakaryaspor A.Ş."},
    37: {"name": "Atakaş Hatayspor"}, 38: {"name": "Adana Demirspor A.Ş."},
    39: {"name": "Batman Petrol Spor A.Ş."}, 40: {"name": "Bursaspor"},
    41: {"name": "Muğlaspor Kulübü"}, 42: {"name": "Mardin 1969 Spor"},
    43: {"name": "Adana 01 Futbol Kulübü SK"}, 44: {"name": "Aliağa Futbol A.Ş."},
    45: {"name": "Seza Çimento Elazığspor"}, 46: {"name": "Muş Spor Kulübü"},
    47: {"name": "Kızılkaya Tarım Şanlıurfaspor"}, 48: {"name": "Akedaş Kahramanmaraş İstiklal Spor"},
    49: {"name": "Sultan Su İnegölspor"}, 50: {"name": "Güzide Gebze Spor Kulübü"},
    51: {"name": "İskenderunspor A.Ş."}, 52: {"name": "ISBAŞ Isparta 32 Spor Kulübü"},
    53: {"name": "MKE Ankaragücü"}, 54: {"name": "Ankara Demirspor"},
    55: {"name": "Sincan Belediyesi Ankaraspor"}, 56: {"name": "Menemen Futbol Kulübü"},
    57: {"name": "Anagold 24Erzincanspor"}, 58: {"name": "Kuzeyboru 68 Aksaray Belediye Spor"},
    59: {"name": "Beyoğlu Yeni Çarşı Spor Faaliyetleri A.Ş."}, 60: {"name": "KCT 1461 Trabzon FK"},
    61: {"name": "GMG Kastamonuspor"}, 62: {"name": "Fethiyespor"},
    63: {"name": "Merkür Jet Erbaaspor"}, 64: {"name": "Arkent Arnavutköy Belediyesi Futbol SK"},
    65: {"name": "Karacabey Belediye Spor A.Ş."}, 66: {"name": "Granny's Waffles Kırklarelispor"},
    67: {"name": "Altınordu"}, 68: {"name": "Somaspor"},
    69: {"name": "Beykoz Anadolu Spor A.Ş."}, 70: {"name": "Turkish Oil Yeni Mersin İdmanyurdu Futbol A.Ş."},
    71: {"name": "Kepez Spor Futbol A.Ş."}, 72: {"name": "Adanaspor A.Ş."},
    73: {"name": "Karaman Futbol Kulübü"}, 74: {"name": "Yeni Malatyaspor"},
    75: {"name": "Bucaspor 1928"}, 76: {"name": "İnegöl Kafkas Spor Kulübü"},
    77: {"name": "12 Bingöl Spor"}, 78: {"name": "Sebat Gençlik Spor"},
    79: {"name": "Kütahyaspor Futbol Spor Kulübü"}, 80: {"name": "Çorlu Spor 1947"},
    81: {"name": "Silifke Belediye Spor"}, 82: {"name": "52 Orduspor FK"},
    83: {"name": "Eskişehirspor Kulübü"}, 84: {"name": "Küçükçekmece Sinop Spor A.Ş."},
    85: {"name": "Eti Gübre Mazıdağı Fosfat Spor"}, 86: {"name": "Kdz. Ereğli Belediye Spor"},
    87: {"name": "Karşıyaka"}, 88: {"name": "Bursa Yıldırım Spor Kulübü"},
    89: {"name": "Karaköprü Belediye Spor"}, 90: {"name": "Yozgat Belediyesi Bozok Spor"},
    91: {"name": "Ayvalıkgücü Belediyespor"}, 92: {"name": "Karalar İnşaat Etimesgut Spor Kulübü"},
    93: {"name": "Erciyes 38 Futbol Spor Kulübü"}, 94: {"name": "Fatsa Belediyespor"},
    95: {"name": "Nev Sağlık Grubu Balıkesirspor"}, 96: {"name": "Silivrispor"},
    97: {"name": "Cinegold Ağrı 1970 Spor Kulübü"}, 98: {"name": "TCH Group Zonguldak Spor Futbol Kulübü A.Ş."},
    99: {"name": "Denizli İdmanyurdu 1959 Spor Kulübü"}, 100: {"name": "Yalova FK 77 Spor Kulübü"},
    101: {"name": "MDGroup Osmaniyespor"}, 102: {"name": "Düzce Cam Düzcespor"},
    103: {"name": "Oktaş Uşak Spor A.Ş."}, 104: {"name": "Galata Spor Kulübü"},
    105: {"name": "Niğde Belediyesi Spor"}, 106: {"name": "Pazarspor"},
    107: {"name": "Tire 2021 Futbol Kulübü"}, 108: {"name": "Bulvarspor"},
    109: {"name": "Malatya Yeşilyurt Spor Kulübü"}, 110: {"name": "Karabük İdmanyurdu Spor"},
    111: {"name": "Alanya 1221 Futbol Spor Kulübü"}, 112: {"name": "Beykoz İshaklı Spor Faaliyetleri A.Ş."},
    113: {"name": "Kirikkale FK Spor Kulübü"}, 114: {"name": "Orduspor 1967 A.Ş."},
    115: {"name": "Eskişehir Anadolu Spor Faaliyetleri A.Ş."}, 116: {"name": "İnkılap Futbol Spor Kulübü"},
    117: {"name": "Ejderoğlu Kırşehir Futbol Spor Kulübü"}, 118: {"name": "Tokat Belediye Spor Kulübü"},
    119: {"name": "Söke 1970 Spor Kulübü"}, 120: {"name": "Bursa Nilüfer Futbol A.Ş."},
    121: {"name": "Diyarbekir Spor A.Ş."}, 122: {"name": "Amasyaspor FK"},
    123: {"name": "Altay"}, 124: {"name": "Astor Enerji Çankaya Spor Kulübü"},
    125: {"name": "Kilis 1984 A.Ş."}, 126: {"name": "Artvin Hopaspor"},
    127: {"name": "Bornova 1877 Sportif Yatırımlar A.Ş."}, 128: {"name": "Kestel Çilek Spor Kulübü"},
    129: {"name": "Karpedo Dondurma Kahramanmaraşspor"}, 130: {"name": "1926 Bulancakspor"},
    131: {"name": "Afyonspor Kulübü"}, 132: {"name": "Polatlı 1926 Spor Kulübü"},
    133: {"name": "Suvermez Kapadokya Spor"}, 134: {"name": "Çayeli Spor Kulübü"},
    135: {"name": "İzmir Çoruhlu Futbol Kulübü A.Ş."}, 136: {"name": "Edirnespor"},
    137: {"name": "Hacettepe A.Ş. Türk Metal 1963 Spor"}, 138: {"name": "Giresunspor"},
    139: {"name": "Nazilli Spor A.Ş."}, 140: {"name": "Kahta 02 ak"},
    141: {"name": "Bayburt il özel idaresi"}, 142: {"name": "Bucak belediye oğuzhanspor"},
    143: {"name": "Gümüşhane sportif"}, 144: {"name": "Siirtspor"},
    145: {"name": "Dersim Spor"}, 146: {"name": "Serhat Ardahanspor"},
    147: {"name": "Söğütspor"}, 148: {"name": "Ezinespor"},
    149: {"name": "Biga Spor"}, 150: {"name": "Yüksekova belediyespor"},
    151: {"name": "Cizre Spor"}, 152: {"name": "Şırnak petrol Spor"},
    153: {"name": "Sinopspor"}, 154: {"name": "Bartınspor"},
    155: {"name": "Tatvan Spor"}, 156: {"name": "Çankırıspor"},
    157: {"name": "Kars 36 spor"}
}

def get_team_str(rank: int) -> str:
    info = RANK_TO_INFO.get(rank)
    return info["name"] if info else f"Takım {rank}"

def parse_score(text: str) -> tuple[int, int]:
    for sep in ['-', ',', ';', '/', '\\', '|', 'x', 'X', '\t', ':']:
        text = text.replace(sep, ' ')
    parts = text.strip().split()
    if len(parts) == 2:
        return int(parts[0]), int(parts[1])
    raise ValueError("Skor anlaşılamadı")

# === DEVAM / YENİ BAŞLAMA EKRANI ===
class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        
        title = Label(text="🏆 ZİRAAT TÜRKİYE KUPASI\nSİMÜLASYONU", font_size='28sp', halign='center', size_hint_y=0.3)
        layout.add_widget(title)
        
        if os.path.exists(SAVE_FILE):
            btn_continue = Button(text="Kaldığın Yerden Devam Et", background_color=(0.2, 0.6, 0.2, 1), font_size='18sp')
            btn_continue.bind(on_press=self.continue_tournament)
            layout.add_widget(btn_continue)
            
        btn_new = Button(text="Yeni Baştan Turnuva Başlat", background_color=(0.7, 0.2, 0.2, 1), font_size='18sp')
        btn_new.bind(on_press=self.new_tournament)
        layout.add_widget(btn_new)
        
        self.add_widget(layout)
        
    def continue_tournament(self, instance):
        self.manager.current = 'game'
        self.manager.get_screen('game').load_and_run()

    def new_tournament(self, instance):
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)
        self.manager.current = 'game'
        self.manager.get_screen('game').start_new()

# === ANA OYUN / TUR EKRANI ===
class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.state = {"current_stage": "start", "data": {}}
        
        # Ana Düzen
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Üst Başlık Bilgisi
        self.stage_label = Label(text="Aşama: Başlangıç", font_size='20sp', bold=True, size_hint_y=0.1)
        self.main_layout.add_widget(self.stage_label)
        
        # Dinamik İçerik Alanı (Kaydırılabilir)
        self.scroll = ScrollView(size_hint_y=0.8)
        self.content_grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.content_grid.bind(minimum_height=self.content_grid.setter('height'))
        self.scroll.add_widget(self.content_grid)
        self.main_layout.add_widget(self.scroll)
        
        # Alt Buton Alanı
        self.btn_action = Button(text="Devam Et", size_hint_y=0.1, background_color=(0.1, 0.5, 0.8, 1))
        self.btn_action.bind(on_press=self.on_action_click)
        self.main_layout.add_widget(self.btn_action)
        
        self.add_widget(self.main_layout)
        
        # Geçici veri saklayıcılar
        self.inputs = {}
        self.current_matches = []
        self.byes = []
        self.group_fixtures = []
        self.group_stats = {}

    def save_state(self):
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.state, f, ensure_ascii=False, indent=4)

    def start_new(self):
        self.state = {"current_stage": "start", "data": {}}
        self.process_stage()

    def load_and_run(self):
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                self.state = json.load(f)
        self.process_stage()

    def process_stage(self):
        self.content_grid.clear_widgets()
        self.inputs.clear()
        stage = self.state["current_stage"]
        
        if stage == "start":
            self.stage_label.text = "1. Tur (128-157)"
            self.setup_knockout(list(range(128, 158)), is_double=False)
        elif stage == "qual2":
            self.stage_label.text = "2. Tur"
            self.setup_knockout(list(range(72, 128)) + self.state["data"]["qual1_winners"], is_double=False)
        elif stage == "qual3":
            self.stage_label.text = "3. Tur"
            self.setup_knockout(list(range(12, 72)) + self.state["data"]["qual2_winners"], is_double=False)
        elif stage == "playoff":
            self.stage_label.text = "Playoff Turu"
            self.setup_knockout(list(range(6, 12)) + self.state["data"]["qual3_winners"], is_double=False)
        elif stage == "groups":
            self.stage_label.text = "Grup Aşaması (8 Grup - 6'şar Maç)"
            self.setup_groups()
        elif stage == "last16":
            self.stage_label.text = "Son 16 Turu"
            self.setup_last16()
        elif stage == "quarter":
            self.stage_label.text = "Çeyrek Final (Çift Maç)"
            self.setup_knockout(self.state["data"]["last16_winners"], is_double=True)
        elif stage == "semi":
            self.stage_label.text = "Yarı Final (Çift Maç)"
            self.setup_semi()
        elif stage == "final":
            self.stage_label.text = "🏆 BÜYÜK FİNAL 🏆"
            self.setup_final()
        elif stage == "completed":
            self.stage_label.text = "Turnuva Tamamlandı!"
            self.show_winner_screen()

    # === ELEME TURU KURULUMU ===
    def setup_knockout(self, participants, is_double=False):
        sorted_part = sorted(participants)
        self.byes = []
        if len(sorted_part) % 2 == 1:
            bye_team = sorted_part.pop()
            self.byes.append(bye_team)
            lbl_bye = Label(text=f"👋 {get_team_str(bye_team)} bu turu BAY geçti.", size_hint_y=None, height=40, color=(1, 0.8, 0, 1))
            self.content_grid.add_widget(lbl_bye)

        half = len(sorted_part) // 2
        seeded = sorted_part[:half]
        unseeded = sorted_part[half:]
        random.shuffle(unseeded)
        
        self.current_matches = list(zip(seeded, unseeded))
        self.btn_action.text = "Skorları Onayla ve İlerle"

        for idx, (home, away) in enumerate(self.current_matches, 1):
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
            
            lbl = Label(text=f"{get_team_str(home)} - {get_team_str(away)}", halign='right', size_hint_x=0.6)
            
            if is_double:
                inp1 = TextInput(hint_text="1. Maç", multiline=False, size_hint_x=0.2)
                inp2 = TextInput(hint_text="2. Maç", multiline=False, size_hint_x=0.2)
                box.add_widget(lbl)
                box.add_widget(inp1)
                box.add_widget(inp2)
                self.inputs[idx] = (inp1, inp2)
            else:
                inp = TextInput(hint_text="Skor (Örn: 2-1)", multiline=False, size_hint_x=0.4)
                box.add_widget(lbl)
                box.add_widget(inp)
                self.inputs[idx] = inp
                
            self.content_grid.add_widget(box)

    # === ELEME TURU KONTROLÜ VE KAYIT ===
    def check_knockout_results(self, is_double=False):
        winners = []
        pending_penalties = []

        for idx, (home, away) in enumerate(self.current_matches, 1):
            try:
                if is_double:
                    inp1, inp2 = self.inputs[idx]
                    h1, a1 = parse_score(inp1.text)
                    h2, a2 = parse_score(inp2.text)
                    # ilk maç home sahasında, ikinci maç away sahasında varsayımıyla toplam skor
                    agg_home = h1 + a2
                    agg_away = a1 + h2
                else:
                    inp = self.inputs[idx]
                    agg_home, agg_away = parse_score(inp.text)

                if agg_home > agg_away:
                    winners.append(home)
                elif agg_away > agg_home:
                    winners.append(away)
                else:
                    # Beraberlik durumunda penaltı kararı için listeye ekle
                    pending_penalties.append((home, away))
            except:
                self.show_popup("Hata", "Lütfen tüm skorları doğru formatta (Örn: 2-1 veya 2 1) giriniz.")
                return

        winners.extend(self.byes)

        if pending_penalties:
            self.ask_penalties(pending_penalties, winners, is_double)
        else:
            self.save_and_next_stage(winners)

    def ask_penalties(self, remaining, winners, is_double):
        if not remaining:
            self.save_and_next_stage(winners)
            return
        
        home, away = remaining[0]
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=f"{get_team_str(home)} - {get_team_str(away)}\nMaç berabere bitti! Penaltılarla kim kazandı?"))
        
        popup = Popup(title="Penaltı Atışları", content=content, size_hint=(0.6, 0.4), auto_dismiss=False)
        
        btn_home = Button(text=get_team_str(home))
        btn_away = Button(text=get_team_str(away))
        
        def choose_home(inst):
            winners.append(home)
            popup.dismiss()
            self.ask_penalties(remaining[1:], winners, is_double)
            
        def choose_away(inst):
            winners.append(away)
            popup.dismiss()
            self.ask_penalties(remaining[1:], winners, is_double)

        btn_home.bind(on_press=choose_home)
        btn_away.bind(on_press=choose_away)
        content.add_widget(btn_home)
        content.add_widget(btn_away)
        popup.open()

    def save_and_next_stage(self, winners):
        stage = self.state["current_stage"]
        if stage == "start":
            self.state["data"]["qual1_winners"] = winners
            self.state["current_stage"] = "qual2"
        elif stage == "qual2":
            self.state["data"]["qual2_winners"] = winners
            self.state["current_stage"] = "qual3"
        elif stage == "qual3":
            self.state["data"]["qual3_winners"] = winners
            self.state["current_stage"] = "playoff"
        elif stage == "playoff":
            self.state["data"]["playoff_winners"] = winners
            self.state["current_stage"] = "groups"
        elif stage == "last16":
            self.state["data"]["last16_winners"] = winners
            self.state["current_stage"] = "quarter"
        elif stage == "quarter":
            self.state["data"]["quarter_winners"] = winners
            self.state["current_stage"] = "semi"
        
        self.save_state()
        self.process_stage()

    # === GRUP AŞAMASI KURULUMU ===
    def setup_groups(self):
        direct = list(range(1, 6))
        all_teams = sorted(direct + self.state["data"]["playoff_winners"])
        
        pots = [all_teams[i*8:(i+1)*8] for i in range(4)]
        for p in pots[1:]:
            random.shuffle(p)

        self.group_fixtures = []
        self.group_stats = {}
        self.btn_action.text = "Grup Sonuçlarını Hesapla ve Son 16'ya Geç"

        for g_idx in range(8):
            group_letter = chr(65 + g_idx)
            group_ranks = [pots[0][g_idx], pots[1][g_idx], pots[2][g_idx], pots[3][g_idx]]
            
            lbl_g = Label(text=f"📊 GRUP {group_letter}", font_size='18sp', bold=True, size_hint_y=None, height=40, color=(0.1, 0.7, 0.8, 1))
            self.content_grid.add_widget(lbl_g)
            
            for r in group_ranks:
                self.group_stats[r] = {"points": 0, "gf": 0, "ga": 0, "group": group_letter}

            # Fikstür oluşturma (İç saha - Deplasman çift devreli)
            match_id = 0
            for i in range(4):
                for j in range(4):
                    if i != j:
                        home, away = group_ranks[i], group_ranks[j]
                        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=45, spacing=5)
                        lbl_m = Label(text=f"   {get_team_str(home)} - {get_team_str(away)}", size_hint_x=0.7, halign='left')
                        inp = TextInput(hint_text="Skor", multiline=False, size_hint_x=0.3)
                        box.add_widget(lbl_m)
                        box.add_widget(inp)
                        self.content_grid.add_widget(box)
                        
                        self.group_fixtures.append({
                            "group": group_letter, "home": home, "away": away, "input": inp
                        })

    def check_group_results(self):
        # İstatistikleri sıfırla
        for r in self.group_stats:
            self.group_stats[r] = {"points": 0, "gf": 0, "ga": 0, "group": self.group_stats[r]["group"]}

        for f in self.group_fixtures:
            try:
                hs, as_ = parse_score(f["input"].text)
                home, away = f["home"], f["away"]
                
                self.group_stats[home]["gf"] += hs
                self.group_stats[home]["ga"] += as_
                self.group_stats[away]["gf"] += as_
                self.group_stats[away]["ga"] += hs
                
                if hs > as_:
                    self.group_stats[home]["points"] += 3
                elif as_ > hs:
                    self.group_stats[away]["points"] += 3
                else:
                    self.group_stats[home]["points"] += 1
                    self.group_stats[away]["points"] += 1
            except:
                self.show_popup("Hata", "Lütfen tüm grup maç skorlarını doğru giriniz.")
                return

        # Grupları kendi içinde sırala
        results = []
        for g_idx in range(8):
            group_letter = chr(65 + g_idx)
            teams_in_group = [r for r, s in self.group_stats.items() if s["group"] == group_letter]
            
            standings = sorted(teams_in_group, 
                               key=lambda x: (-self.group_stats[x]["points"], 
                                             -(self.group_stats[x]["gf"] - self.group_stats[x]["ga"]), 
                                             -self.group_stats[x]["gf"]))
            results.append({
                "group": group_letter,
                "first": standings[0],
                "second": standings[1]
            })

        self.state["data"]["group_results"] = results
        self.state["current_stage"] = "last16"
        self.save_state()
        self.process_stage()

    # === SON 16 TURU ===
    def setup_last16(self):
        group_results = self.state["data"]["group_results"]
        pairings = []
        for i in range(0, 8, 2):
            g1 = group_results[i]
            g2 = group_results[i + 1]
            pairings.append((g1["first"], g2["second"]))
            pairings.append((g2["first"], g1["second"]))
            
        self.current_matches = pairings
        self.btn_action.text = "Skorları Onayla ve Çeyrek Finale Geç"
        self.byes = []

        for idx, (home, away) in enumerate(self.current_matches, 1):
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
            lbl = Label(text=f"{get_team_str(home)} vs {get_team_str(away)}", size_hint_x=0.6)
            inp = TextInput(hint_text="Skor", multiline=False, size_hint_x=0.4)
            box.add_widget(lbl)
            box.add_widget(inp)
            self.content_grid.add_widget(box)
            self.inputs[idx] = inp

    # === YARI FİNAL ===
    def setup_semi(self):
        q = self.state["data"]["quarter_winners"]
        self.current_matches = [(q[0], q[1]), (q[2], q[3])]
        self.btn_action.text = "Skorları Onayla ve Finale Geç"
        self.byes = []

        for idx, (home, away) in enumerate(self.current_matches, 1):
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
            lbl = Label(text=f"{get_team_str(home)} vs {get_team_str(away)}", size_hint_x=0.6)
            inp1 = TextInput(hint_text="1. Maç", multiline=False, size_hint_x=0.2)
            inp2 = TextInput(hint_text="2. Maç", multiline=False, size_hint_x=0.2)
            box.add_widget(lbl)
            box.add_widget(inp1)
            box.add_widget(inp2)
            self.content_grid.add_widget(box)
            self.inputs[idx] = (inp1, inp2)

    def check_semi_results(self):
        winners = []
        pending_penalties = []
        for idx, (home, away) in enumerate(self.current_matches, 1):
            try:
                inp1, inp2 = self.inputs[idx]
                h1, a1 = parse_score(inp1.text)
                h2, a2 = parse_score(inp2.text)
                agg_home = h1 + a2
                agg_away = a1 + h2
                if agg_home > agg_away:
                    winners.append(home)
                elif agg_away > agg_home:
                    winners.append(away)
                else:
                    pending_penalties.append((home, away))
            except:
                self.show_popup("Hata", "Skorları doğru giriniz.")
                return
        
        if pending_penalties:
            self.ask_semi_penalties(pending_penalties, winners)
        else:
            self.save_semi_and_next(winners)

    def ask_semi_penalties(self, remaining, winners):
        if not remaining:
            self.save_semi_and_next(winners)
            return
        home, away = remaining[0]
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=f"{get_team_str(home)} - {get_team_str(away)}\nPenaltılarla kim kazandı?"))
        popup = Popup(title="Penaltılar", content=content, size_hint=(0.6, 0.4), auto_dismiss=False)
        
        b1 = Button(text=get_team_str(home))
        b2 = Button(text=get_team_str(away))
        b1.bind(on_press=lambda x: [winners.append(home), popup.dismiss(), self.ask_semi_penalties(remaining[1:], winners)])
        b2.bind(on_press=lambda x: [winners.append(away), popup.dismiss(), self.ask_semi_penalties(remaining[1:], winners)])
        content.add_widget(b1)
        content.add_widget(b2)
        popup.open()

    def save_semi_and_next(self, winners):
        self.state["data"]["semi_winners"] = winners
        self.state["current_stage"] = "final"
        self.save_state()
        self.process_stage()

    # === FİNAL ===
    def setup_final(self):
        f1, f2 = self.state["data"]["semi_winners"]
        self.current_matches = [(f1, f2)]
        self.btn_action.text = "Şampiyonu Belirle!"
        self.byes = []

        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=10)
        lbl = Label(text=f"🏆 {get_team_str(f1)} - {get_team_str(f2)} 🏆", font_size='18sp', size_hint_x=0.6)
        inp = TextInput(hint_text="Skor", multiline=False, size_hint_x=0.4)
        box.add_widget(lbl)
        box.add_widget(inp)
        self.content_grid.add_widget(box)
        self.inputs[1] = inp

    def check_final_results(self):
        try:
            h, a = parse_score(self.inputs[1].text)
            f1, f2 = self.current_matches[0]
            if h > a:
                self.show_winner_popup(f1)
            elif a > h:
                self.show_winner_popup(f2)
            else:
                # Final beraberlik penaltı seçimi
                content = BoxLayout(orientation='vertical', padding=10, spacing=10)
                content.add_widget(Label(text="Kupa penaltılara kaldı! Kim Kazandı?"))
                popup = Popup(title="Şampiyonluk Penaltıları", content=content, size_hint=(0.6, 0.4), auto_dismiss=False)
                b1 = Button(text=get_team_str(f1))
                b2 = Button(text=get_team_str(f2))
                b1.bind(on_press=lambda x: [popup.dismiss(), self.show_winner_popup(f1)])
                b2.bind(on_press=lambda x: [popup.dismiss(), self.show_winner_popup(f2)])
                content.add_widget(b1)
                content.add_widget(b2)
                popup.open()
        except:
            self.show_popup("Hata", "Lütfen geçerli bir final skoru girin.")

    def show_winner_popup(self, winner):
        self.state["data"]["cup_winner"] = winner
        self.state["current_stage"] = "completed"
        self.save_state()
        self.process_stage()

    # === ŞAMPİYONLUK EKRANI ===
    def show_winner_screen(self):
        winner = self.state["data"].get("cup_winner", 0)
        lbl_champ = Label(text=f"🎉 TEBRİKLER 🎉\n\n🏆 ZİRAAT TÜRKİYE KUPASI ŞAMPİYONU 🏆\n\n🥇 {get_team_str(winner)} 🥇", 
                          font_size='24sp', halign='center', color=(1, 0.8, 0, 1))
        self.content_grid.add_widget(lbl_champ)
        self.btn_action.text = "Yeniden Başlat"

    # === ALT BUTON TETİKLEYİCİSİ ===
    def on_action_click(self, instance):
        stage = self.state["current_stage"]
        if stage in ["start", "qual2", "qual3", "playoff", "last16"]:
            self.check_knockout_results(is_double=False)
        elif stage == "groups":
            self.check_group_results()
        elif stage == "quarter":
            self.check_knockout_results(is_double=True)
        elif stage == "semi":
            self.check_semi_results()
        elif stage == "final":
            self.check_final_results()
        elif stage == "completed":
            if os.path.exists(SAVE_FILE):
                os.remove(SAVE_FILE)
            self.manager.current = 'start'

    # === POPUP UYARILARI ===
    def show_popup(self, title, text):
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text=text))
        btn = Button(text="Kapat", size_hint_y=0.3)
        content.add_widget(btn)
        popup = Popup(title=title, content=content, size_hint=(0.6, 0.4))
        btn.bind(on_press=popup.dismiss)
        popup.open()

# === SCREEN MANAGER ===
class TournamentApp(App):
    def build(self):
        self.title = "Ziraat Türkiye Kupası Simülasyonu"
        sm = ScreenManager()
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(GameScreen(name='game'))
        return sm

if __name__ == "__main__":
    TournamentApp().run()