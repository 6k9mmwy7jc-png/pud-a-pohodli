# Pud a pohodlí
> **Podtitul:** *Pudlpointři, neurotyp pracovních psů ve světě povrchní kynologie*

Moderní prezentační web a redakční systém (CMS) postavený na míru pro autentickou pracovní kynologii, etologii a plemeno pudlpointer.

---

## 🌟 Klíčové vlastnosti

1. **Prezentační web na míru:**
   - **Úvodní stránka:** Hlavní myšlenka, 4 pilíře konceptu, profil plemene pudlpointer, nejnovější články a fotogalerie.
   - **Manifest:** Filozofické vymezení proti módním kynologickým dogmatům a obhajoba biologické pravdy.
   - **O plemeni Pudlpointer:** Historie barona Hegewalda, spojení pudla a pointra, neurotyp a pracovní přepínač.
   - **Články & Úvahy:** Archiv esejů a odborných textů s detailním čtenářským zobrazením.
   - **Fotogalerie:** Autentické momenty z pole, vody a lesa.
   - **O autorech & Kontakt:** Informace o týmu a kontaktní e-mail.

2. **Redakční systém (Admin CMS):**
   - **Přístup pro další lidi:** V sekci *Správa uživatelů* můžete jedním kliknutím vytvořit nový účet (jméno + heslo) pro kolegu, partnera či spoluautora.
   - **Mobilní i desktopové rozhraní:** Váš kolega může otevřít administraci přímo na svém mobilu (iPhone/Android) a nahrávat fotky z terénu nebo psát články.
   - **Správa článků:** Tvorba, úprava, mazání, koncepty / okamžité publikování, nahrávání titulních fotografií.
   - **Správa fotogalerie:** Přímé nahrávání fotografií (JPG, PNG, WEBP) s popiskem a kategorií.
   - **Nastavení webu:** Možnost kdykoliv měnit texty, podtitul, bio i e-mail bez zásahu do kódu.

3. **Technická čistota:**
   - Běží na čistém Pythonu 3 (standardní knihovna) + SQLite.
   - **Zero-dependency:** Nevyžaduje instalaci žádných externích balíčků (žádné pip konflikty).
   - Databáze SQLite a nahrané fotografie jsou uloženy lokálně ve složkách `data/` a `uploads/`.

---

## 🚀 Jak web spustit lokálně na vašem Macu

V Terminálu spusťte:

```bash
cd /Users/josefjursa/.gemini/antigravity/scratch/pud-a-pohodli
python3 app.py
```
Nebo jednoduše:
```bash
./run.sh
```

Web se spustí na adrese:
* **Veřejný web:** [http://localhost:8080](http://localhost:8080)
* **Administrace (redakce):** [http://localhost:8080/admin](http://localhost:8080/admin)

### Výchozí přihlašovací údaje:
* **Uživatel:** `admin`
* **Heslo:** `admin123`
*(Heslo si můžete po přihlášení kdykoliv změnit v sekci „Změna hesla“)*

---

## 👥 Jak udělit admin přístup dalšímu člověku

1. Přihlaste se do administrace na `http://localhost:8080/admin`.
2. V levém menu klikněte na **„Správci & Uživatelé“** (`/admin/users`).
3. V pravém formuláři zadejte:
   - Uživatelské jméno (např. `karel`)
   - Zobrazované jméno (např. `Karel Novák`)
   - Heslo
   - Roli (*Správce* nebo *Editor*)
4. Klikněte na **„Vytvořit účet správce“**.
5. Nyní se tento člověk může ze svého zařízení přihlásit a vkládat články a fotografie.

---

## 📱 Jak umožnit druhému člověku přístup z jeho telefonu/počítače

### Varianta A: Jste na stejné Wi-Fi síti (doma / na chatě)
1. Na Macu zjistěte svou lokální IP adresu (např. `192.168.1.50`).
2. Druhý člověk zadá do prohlížeče na svém mobilu:  
   `http://192.168.1.50:8080/admin`
3. Přihlásí se svými údaji a může ihned nahrávat fotky z mobilní galerie.

### Varianta B: Okamžitý přístup odkudkoliv přes bezplatný tunel (Cloudflare Tunnel)
Pokud chcete, aby se mohl přihlásit i z terénu přes mobilní data:
```bash
brew install cloudflared
cloudflared tunnel --url http://localhost:8080
```
Cloudflare vám vygeneruje zabezpečenou veřejnou adresu (např. `https://random-name.trycloudflare.com`), kterou pošlete kolegovi.

### Varianta C: Trvalé nasazení na internet (Hosting / VPS)
Jelikož je aplikace čistý Python + SQLite, můžete ji jedním kliknutím nasadit na:
- **Render.com** (zdarma, stačí nahrát na GitHub a spustit příkaz `python3 app.py`)
- **Railway.app** nebo **Fly.io**
- Vlastní VPS (Linux server za 3–5 € měsíčně) s vlastní doménou (např. `pudapohodli.cz`).

---

## 📂 Struktura projektu

```
pud-a-pohodli/
├── app.py              # Hlavní webový server a router
├── database.py         # SQLite databáze, migrace, šifrování hesel a seed článků
├── templates.py        # Responzivní HTML/CSS šablony webu i administrace
├── run.sh              # Spouštěcí skript
├── static/
│   └── img/            # Vektorové ilustrace (pole, voda, neurotyp, portrét)
├── uploads/            # Zde se ukládají fotky nahrané správci z mobilu/PC
└── data/
    └── database.sqlite # Databáze SQLite (články, fotky, uživatelé, nastavení)
```
