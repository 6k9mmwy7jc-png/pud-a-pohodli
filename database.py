import sqlite3
import hashlib
import secrets
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "database.sqlite")

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password: str, salt: str = None) -> tuple:
    if not salt:
        salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000).hex()
    return hashed, salt

def verify_password(password: str, hashed: str, salt: str) -> bool:
    test_hash, _ = hash_password(password, salt)
    return secrets.compare_digest(test_hash, hashed)

def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        salt TEXT NOT NULL,
        display_name TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'editor',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        token TEXT PRIMARY KEY,
        user_id INTEGER NOT NULL,
        expires_at TIMESTAMP NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        slug TEXT UNIQUE NOT NULL,
        subtitle TEXT,
        cover_image TEXT,
        summary TEXT NOT NULL,
        content TEXT NOT NULL,
        tags TEXT DEFAULT '',
        is_published INTEGER DEFAULT 1,
        video_url TEXT DEFAULT '',
        author_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (author_id) REFERENCES users (id)
    );
    """)

    try:
        c.execute("ALTER TABLE articles ADD COLUMN video_url TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass

    c.execute("""
    CREATE TABLE IF NOT EXISTS gallery (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        image_url TEXT NOT NULL,
        category TEXT DEFAULT 'Obecné',
        uploaded_by INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (uploaded_by) REFERENCES users (id)
    );
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    );
    """)

    conn.commit()

    # Seed default settings
    default_settings = {
        "site_title": "Pud a pohodlí",
        "site_subtitle": "Pudlpointři, neurotyp pracovních psů ve světě povrchní kynologie",
        "site_description": "Autentický pohled na biologii, genetiku a pracovní vlohy psů v kontrastu s moderním pohodlím a zjednodušujícími trendy.",
        "author_bio": "Tým chovatelů, kynologů a milovníků poctivé práce, pro které pes není lidský doplněk ani plyšák, ale plnohodnotná biologická bytost s geneticky danými potřebami a pudy.",
        "contact_email": "info@pudapohodli.cz",
        "instagram": "https://instagram.com",
    }

    for k, v in default_settings.items():
        c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", (k, v))

    # Seed default admin if no users exist
    c.execute("SELECT COUNT(*) as count FROM users")
    if c.fetchone()["count"] == 0:
        h, s = hash_password("admin123")
        c.execute("""
        INSERT INTO users (username, password_hash, salt, display_name, role)
        VALUES (?, ?, ?, ?, ?)
        """, ("admin", h, s, "Hlavní správce", "admin"))
        admin_id = c.lastrowid

        # Seed initial articles written with high journalistic and cynological value
        articles = [
            (
                "Neurotyp pracovního psa: Proč selekce na drive neodpouští civilizační zkratky",
                "neurotyp-pracovniho-psa",
                "Biologická realita nervové soustavy, kterou nelze přeprat humanizací ani pamlskem",
                "",
                "V moderní společnosti se ze psa stalo zrcadlo lidských emocí. Jenže pes se silnou nervovou soustavou, selektovaný po generace na kořistnický pud a neústupnost, funguje podle úplně jiných zákonitostí.",
                """<p class="lead">V moderní společnosti se ze psa stal sociální doplněk a zrcadlo lidských emocí. Jenže pes se silnou nervovou soustavou, selektovaný po generace na nekompromisní kořistnický pud, chuť pracovat v nepříznivých podmínkách a ochotu překonávat bolest, funguje podle úplně jiných zákonitostí než salonní společník.</p>

<h3>Střet dvou světů: Pud versus civilizační komfort</h3>
<p>Dnešní civilizace staví na pohodlí, bezpečí a eliminaci veškerých diskomfortů. To je přirozený lidský vývoj. Problém nastává v okamžiku, kdy toto měřítko nekriticky aplikujeme na zvířata, konkrétně na pracovní plemena psů. Kynologie se vlivem sociálních sítí posunula do roviny povrchních dogmat: vše musí být za každých okolností „pozitivní“, jakýkoliv projev pudu je nálepkován jako agrese nebo trauma, a potřeba psa pracovat bývá redukována na házení míčku v městském parku.</p>

<p>Jenže biologická selekce nefunguje podle internetových trendů. Pracovní pes – ať už mluvíme o ohařích jako je pudlpointer, tvrdých teriérech nebo pracovních německých ovčácích – nese specifický <strong>neurotyp</strong>. Vyznačuje se:</p>
<ul>
    <li>Vysokým vzruchem a rychlým přechodem do akce (tzv. drive).</li>
    <li>Silnou genetickou fixací na kořist, stopu nebo obranu teritoria.</li>
    <li>Potřebou mentálního a fyzického vybití, které simuluje reálný úkol, nikoliv prázdnou zábavu.</li>
</ul>

<h3>Když chybí práce, přichází frustrace</h3>
<p>Pokud takového psa zavřete do sterilního prostředí moderního bytu a budete s ním zacházet jako s lidským dítětem, nezbavíte ho pudů. Pouze mu vezmete ventil. Pes s pracovním neurotypem v takových podmínkách netrpí „špatnou výchovou“ – trpí frustrací z nevyužití svého biologického potenciálu. A právě odtud pramení většina problémů, které dnešní poradci chování řeší donekonečna omílanými metodami, aniž by pochopili kořen věci.</p>

<p>Pudlpointer a jemu podobná plemena vznikla proto, aby pracovala v rákosí, na poli a v lese. Jsou to psi schopni samostatného rozhodování i absolutní poslušnosti ve chvíli nejvyššího vzrušení. To z nich nedělá zbraně ani nebezpečná zvířata – dělá to z nich špičkové partnery pro ty, kdo rozumí jejich podstatě a nesnaží se je ořezat na míru modernímu pohodlí.</p>""",
                "Neurotyp, Etologie, Pracovní psi",
                1,
                admin_id
            ),
            (
                "Když se pud stane tabu: Norování, ostrost a pokrytectví dnešního náhledu",
                "kdyz-se-pud-stane-tabu-norovani",
                "Proč je tak snadné odsoudit to, co neznáme, a nahradit znalosti předsudky",
                "",
                "Norování a lovecká ostrost patří mezi témata, na která má každý názor, málokdo však viděl reálnou práci a biologický kontext. Jak se vyrovnat s vlnou povrchního moralizování?",
                """<p class="lead">Stačí zmínit slovo „norování“, „ostrost na škodnou“ nebo „chov podle pracovních zkoušek“ a na internetu se strhne bouře. Lidé, kteří v životě neviděli lišku jinak než v dokumentu na Netflixu a jejichž pes zná les jen z vyasfaltované cesty, okamžitě vynášejí etické soudy.</p>

<h3>Povrchní témata pro snadný potlesk</h3>
<p>Proč jsou tato témata tak vděčná? Protože jsou polarizující a nevyžadují hlubší odbornou znalost. Je velice jednoduché napsat emotivní příspěvek o tom, jak je práce loveckých psů krutá a zbytečná v 21. století. Tím si autor zajistí tisíce lajků od lidí, kteří svět přírody vnímají z bezpečí vytopeného obýváku.</p>

<p>Ztrácí se však to podstatné: <strong>biologická a ekologická realita</strong>. Regulace zvěře, ochrana přírody, zdravotní stav populací volně žijících zvířat i samotná etologie psovitých šelem jsou komplexní disciplíny. Pes nebyl domestikován proto, aby ležel na hedvábném polštáři. Tisíce let byl selektován jako nepostradatelný spolupracovník člověka v boji o přežití.</p>

<h3>Ostrost není zloba</h3>
<p>V moderní laické kynologii se fatálně zaměňuje <em>nervní agresivita</em> s <em>pracovní ostrostí</em>. Vyrovnaný, tvrdý pracovní pes je doma miláčkem rodiny a spolehlivým parťákem dětí, protože má pevnou nervovou soustavu. Naopak labilní zvíře z chovu, kde se hledí pouze na exteriér a líbivost (často doprovázenou zdravotními defekty), reaguje na sebemenší podnět hystericky.</p>

<p>Kritizovat loveckou a pracovní kynologii bez porozumění selekci je jako kritizovat chirurga za to, že používá skalpel. Cílem tohoto projektu je nazývat věci pravými jmény a nebát se otevřít témata, kterým se dnešní politicky korektní kynologie raději vyhýbá.</p>""",
                "Norování, Lovecká kynologie, Selekce",
                1,
                admin_id
            ),
            (
                "Pudlpointer: Geniální syntéza inteligence pudla a nekompromisnosti pointra",
                "pudlpointer-genialni-synteza",
                "Historie plemene, které vzniklo odmítnutím chovatelské marnivosti ve prospěch výkonu",
                "",
                "Když na konci 19. století baron von Zedlitz (Hegewald) tvořil pudlpointra, měl jedinou vizi: vytvořit všestranného psa s mimořádnou inteligencí a nezdolnou chutí k práci. Jak toto dědictví obstojí dnes?",
                """<p class="lead">Zatímco většina plemen 19. století směřovala k uzavírání plemenných knih a honbě za exteriérovou krásou, u zrodu pudlpointra stála ryze pragmatická myšlenka: spojit génia vody a učenlivosti s králem pole a větru.</p>

<h3>Vize barona Hegewalda</h3>
<p>Baron von Zedlitz (známý pod pseudonymem Hegewald) byl znechucen tím, jak se z loveckých psů stávají salonní ozdoby. Chtěl ohaře, který bude ochotně pracovat ve studené vodě, bude mít vynikající nos pointra, ale zároveň mimořádnou chápavost a vazbu na vůdce, kterou disponoval původní královský pudl (který byl sám historicky vodním loveckým psem).</p>

<p>Pudlpointer není módní kříženec ani designový pes. Je to jedno z nejstarších a nejpřísněji selektovaných všestranných plemen ohařů. V jeho standardu dodnes hraje prim funkčnost: drsná, přiléhavá srst chránící před trním a chladem, pecný fundament a především hlava – bystrá, soustředěná, s typickým vousem.</p>

<h3>Proč právě pudlpointer v dnešním světě?</h3>
<p>Pudlpointer je ztělesněním toho, co dnešní kynologii chybí: <strong>vyváženost a absence přehánění</strong>. Není přešlechtěný do anatomických extrémů. Netrpí deformacemi lebky ani kloubů způsobenými líbivým vzhledem pro výstavní kruhy. Je to pes zdravý, funkční a neuvěřitelně oddaný – za předpokladu, že dostane to, k čemu byl stvořen: smysluplnou práci a pevné, spravedlivé vedení.</p>""",
                "Pudlpointer, Historie plemene, Standard",
                1,
                admin_id
            )
        ]

        for title, slug, subtitle, cover_image, summary, content, tags, is_pub, auth in articles:
            c.execute("""
            INSERT INTO articles (title, slug, subtitle, cover_image, summary, content, tags, is_published, author_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (title, slug, subtitle, cover_image, summary, content, tags, is_pub, auth))

        # Seed sample gallery placeholders
        gallery_items = [
            ("Pudlpointer v poli", "Vystavování koroptví na podzimním strništi. Plné soustředění a pevný bod.", "/static/img/sample-field.svg", "Pole a vystavování", admin_id),
            ("Práce na vodě", "Ochota jít do rákosí za každého počasí – dědictví původního vodního pudla.", "/static/img/sample-water.svg", "Voda a přinášení", admin_id),
            ("Klid na stanovišti", "Vyrovnaná nervová soustava: Schopnost okamžitého odpočinku po vysokém výkonu.", "/static/img/sample-rest.svg", "Neurotyp v praxi", admin_id),
            ("Portrét v rákosí", "Typický vous, bystrý výraz a drsná srst odolná vůči jakémukoliv porostu.", "/static/img/sample-portrait.svg", "Exteriér a standard", admin_id),
        ]

        for title, desc, img, cat, auth in gallery_items:
            c.execute("""
            INSERT INTO gallery (title, description, image_url, category, uploaded_by)
            VALUES (?, ?, ?, ?, ?)
            """, (title, desc, img, cat, auth))

    conn.commit()
    conn.close()

# Session handling
def create_session(user_id: int) -> str:
    token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(days=14)
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO sessions (token, user_id, expires_at) VALUES (?, ?, ?)", (token, user_id, expires_at))
    conn.commit()
    conn.close()
    return token

def get_user_by_session(token: str):
    if not token:
        return None
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT u.id, u.username, u.display_name, u.role, s.expires_at
        FROM sessions s
        JOIN users u ON s.user_id = u.id
        WHERE s.token = ?
    """, (token,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    expires_at = datetime.fromisoformat(row["expires_at"])
    if expires_at < datetime.utcnow():
        delete_session(token)
        return None
    return dict(row)

def delete_session(token: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM sessions WHERE token = ?", (token,))
    conn.commit()
    conn.close()

# Settings helpers
def get_settings():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT key, value FROM settings")
    settings = {row["key"]: row["value"] for row in c.fetchall()}
    conn.close()
    return settings

def update_settings(data: dict):
    conn = get_connection()
    c = conn.cursor()
    for k, v in data.items():
        c.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (k, v))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
