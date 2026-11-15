import html
from datetime import datetime

def format_date(date_str):
    if not date_str:
        return ""
    try:
        dt = datetime.fromisoformat(str(date_str).replace("Z", ""))
        months = ["ledna", "února", "března", "dubna", "května", "června", "července", "srpna", "září", "října", "listopadu", "prosince"]
        return f"{dt.day}. {months[dt.month - 1]} {dt.year}"
    except Exception:
        return str(date_str)[:10]

COMMON_CSS = """
:root {
  --bg-main: #0e1211;
  --bg-card: #151b19;
  --bg-card-hover: #1c2422;
  --bg-input: #101614;
  --border: #26332f;
  --border-focus: #4e7a68;
  --text-main: #f0f4f2;
  --text-muted: #95a59f;
  --accent: #4ade80;
  --accent-warm: #d97706;
  --accent-gold: #eab308;
  --accent-deep: #166534;
  --danger: #ef4444;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  background-color: var(--bg-main);
  color: var(--text-main);
  line-height: 1.65;
  font-size: 16px;
  -webkit-font-smoothing: antialiased;
}

a { color: inherit; text-decoration: none; transition: all 0.2s; }
a:hover { color: var(--accent); }

.container {
  max-width: 1180px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

/* Header & Nav */
header {
  position: sticky;
  top: 0;
  z-index: 50;
  background: rgba(14, 18, 17, 0.88);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
}

.nav-wrap {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 72px;
}

.logo-block {
  display: flex;
  flex-direction: column;
}

.logo-title {
  font-size: 1.35rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #fff;
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo-dot {
  width: 10px;
  height: 10px;
  background: var(--accent);
  border-radius: 50%;
  display: inline-block;
  box-shadow: 0 0 12px var(--accent);
}

.logo-subtitle {
  font-size: 0.72rem;
  color: var(--text-muted);
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 1.8rem;
  list-style: none;
}

.nav-links a {
  font-weight: 500;
  font-size: 0.95rem;
  color: var(--text-muted);
}

.nav-links a:hover, .nav-links a.active {
  color: #fff;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 0.65rem 1.3rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.92rem;
  cursor: pointer;
  border: 1px solid transparent;
  transition: all 0.2s;
  text-decoration: none;
}

.btn-primary {
  background: #1e3a2f;
  color: #86efac;
  border-color: #2e5948;
}
.btn-primary:hover {
  background: #274b3d;
  color: #bbf7d0;
  border-color: #4ade80;
  transform: translateY(-1px);
}

.btn-accent {
  background: #c2410c;
  color: #ffedd5;
  border-color: #ea580c;
}
.btn-accent:hover {
  background: #9a3412;
  color: #fff;
}

.btn-outline {
  background: transparent;
  border-color: var(--border);
  color: var(--text-main);
}
.btn-outline:hover {
  background: var(--bg-card);
  border-color: var(--text-muted);
  color: #fff;
}

.btn-danger {
  background: rgba(239, 68, 68, 0.15);
  border-color: rgba(239, 68, 68, 0.3);
  color: #fca5a5;
}
.btn-danger:hover {
  background: #ef4444;
  color: #fff;
}

.btn-sm {
  padding: 0.4rem 0.8rem;
  font-size: 0.82rem;
}

/* Mobile Nav Toggle */
.mobile-toggle {
  display: none;
  background: none;
  border: none;
  color: var(--text-main);
  font-size: 1.6rem;
  cursor: pointer;
}

/* Hero Section */
.hero {
  padding: 5rem 0 4rem;
  position: relative;
  overflow: hidden;
  border-bottom: 1px solid var(--border);
}

.hero::before {
  content: "";
  position: absolute;
  top: -150px;
  left: 50%;
  transform: translateX(-50%);
  width: 700px;
  height: 450px;
  background: radial-gradient(circle, rgba(30, 75, 50, 0.35) 0%, rgba(14, 18, 17, 0) 70%);
  pointer-events: none;
}

.badge-tag {
  display: inline-block;
  padding: 0.35rem 0.9rem;
  background: rgba(74, 222, 128, 0.1);
  border: 1px solid rgba(74, 222, 128, 0.25);
  color: var(--accent);
  border-radius: 999px;
  font-size: 0.82rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin-bottom: 1.5rem;
}

.hero-title {
  font-size: clamp(2.5rem, 5vw, 4.2rem);
  font-weight: 900;
  line-height: 1.1;
  letter-spacing: -0.02em;
  margin-bottom: 1.2rem;
  color: #fff;
}

.hero-subtitle {
  font-size: clamp(1.2rem, 2.5vw, 1.65rem);
  font-weight: 400;
  color: #d1ded8;
  margin-bottom: 1.5rem;
  line-height: 1.4;
  max-width: 850px;
}

.hero-desc {
  font-size: 1.1rem;
  color: var(--text-muted);
  max-width: 760px;
  margin-bottom: 2.2rem;
}

.hero-btns {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

/* Sections */
.section {
  padding: 5rem 0;
  border-bottom: 1px solid var(--border);
}

.section-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 3rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.section-label {
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--accent);
  font-weight: 700;
  margin-bottom: 0.4rem;
}

.section-title {
  font-size: 2.2rem;
  font-weight: 800;
  color: #fff;
  letter-spacing: -0.01em;
}

/* Pillars Grid */
.pillars-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1.5rem;
}

.pillar-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 2rem;
  transition: all 0.3s;
}

.pillar-card:hover {
  background: var(--bg-card-hover);
  border-color: var(--border-focus);
  transform: translateY(-3px);
}

.pillar-icon {
  font-size: 2rem;
  margin-bottom: 1.2rem;
  display: inline-block;
}

.pillar-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #fff;
  margin-bottom: 0.8rem;
}

.pillar-text {
  font-size: 0.95rem;
  color: var(--text-muted);
  line-height: 1.6;
}

/* Articles Grid */
.articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(330px, 1fr));
  gap: 2rem;
}

.article-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: all 0.3s;
}

.article-card:hover {
  background: var(--bg-card-hover);
  border-color: var(--border-focus);
  transform: translateY(-3px);
  box-shadow: 0 12px 24px rgba(0,0,0,0.3);
}

.article-img-wrap {
  width: 100%;
  height: 200px;
  overflow: hidden;
  background: #18221f;
  position: relative;
}

.article-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s;
}

.article-card:hover .article-img {
  transform: scale(1.04);
}

.article-body {
  padding: 1.8rem;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.article-meta {
  display: flex;
  gap: 12px;
  font-size: 0.82rem;
  color: var(--text-muted);
  margin-bottom: 0.8rem;
}

.article-tag {
  color: var(--accent);
  font-weight: 600;
}

.article-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #fff;
  line-height: 1.35;
  margin-bottom: 0.8rem;
}

.article-summary {
  font-size: 0.95rem;
  color: var(--text-muted);
  line-height: 1.55;
  margin-bottom: 1.5rem;
  flex-grow: 1;
}

.article-link {
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--accent);
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.article-link:hover {
  text-decoration: underline;
}

/* Gallery Grid */
.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1.5rem;
}

.gallery-item {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  aspect-ratio: 4/3;
  background: #18221f;
  border: 1px solid var(--border);
  cursor: pointer;
  transition: all 0.3s;
}

.gallery-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s;
}

.gallery-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.1) 60%);
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 1.2rem;
  opacity: 0.9;
  transition: opacity 0.3s;
}

.gallery-item:hover img {
  transform: scale(1.05);
}

.gallery-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: #fff;
}

.gallery-desc {
  font-size: 0.82rem;
  color: #d1ded8;
  margin-top: 4px;
}

/* Feature Spotlight (Pudlpointer) */
.spotlight {
  background: linear-gradient(135deg, #172620 0%, #121c18 100%);
  border: 1px solid #2d453b;
  border-radius: 16px;
  padding: 3rem;
  margin: 3rem 0;
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 3rem;
  align-items: center;
}

.spotlight-title {
  font-size: 2rem;
  font-weight: 800;
  color: #fff;
  margin-bottom: 1.2rem;
}

.spotlight-p {
  color: #cbdad3;
  font-size: 1.05rem;
  line-height: 1.7;
  margin-bottom: 1.5rem;
}

.spotlight-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.2rem;
  background: rgba(0,0,0,0.25);
  border: 1px solid #2d453b;
  border-radius: 12px;
  padding: 1.5rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
}

.stat-num {
  font-size: 1.3rem;
  font-weight: 800;
  color: var(--accent);
}

.stat-label {
  font-size: 0.8rem;
  color: var(--text-muted);
  text-transform: uppercase;
}

/* Article Reading View */
.article-header {
  padding: 4rem 0 2rem;
  border-bottom: 1px solid var(--border);
  margin-bottom: 3rem;
}

.article-full-title {
  font-size: clamp(2rem, 4vw, 3.2rem);
  font-weight: 900;
  line-height: 1.2;
  color: #fff;
  margin-bottom: 1rem;
}

.article-full-subtitle {
  font-size: 1.3rem;
  color: var(--accent);
  margin-bottom: 1.5rem;
  line-height: 1.4;
}

.article-full-content {
  max-width: 780px;
  margin: 0 auto 5rem;
  font-size: 1.15rem;
  line-height: 1.8;
  color: #d1ded8;
}

.article-full-content p {
  margin-bottom: 1.8rem;
}

.article-full-content p.lead {
  font-size: 1.3rem;
  font-weight: 500;
  color: #fff;
  border-left: 3px solid var(--accent);
  padding-left: 1.2rem;
  margin-bottom: 2.5rem;
}

.article-full-content h3 {
  font-size: 1.6rem;
  font-weight: 800;
  color: #fff;
  margin: 2.8rem 0 1.2rem;
}

.article-full-content ul {
  margin: 1.5rem 0 2rem 2rem;
}

.article-full-content li {
  margin-bottom: 0.6rem;
}

/* Admin Styles */
.admin-wrap {
  display: flex;
  min-height: calc(100vh - 72px);
}

.admin-sidebar {
  width: 260px;
  background: var(--bg-card);
  border-right: 1px solid var(--border);
  padding: 2rem 1.2rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.admin-sidebar-title {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--text-muted);
  letter-spacing: 0.1em;
  padding: 0 0.8rem;
  margin-bottom: 0.5rem;
}

.admin-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.92rem;
  color: var(--text-muted);
}

.admin-link:hover, .admin-link.active {
  background: var(--bg-card-hover);
  color: #fff;
}

.admin-link.active {
  background: #1b382d;
  color: #86efac;
}

.admin-content {
  flex-grow: 1;
  padding: 2.5rem;
  background: var(--bg-main);
  overflow-y: auto;
}

.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.admin-title {
  font-size: 1.8rem;
  font-weight: 800;
  color: #fff;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2.5rem;
}

.stat-box {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.5rem;
}

.stat-box-num {
  font-size: 2.4rem;
  font-weight: 800;
  color: var(--accent);
}

.stat-box-label {
  font-size: 0.9rem;
  color: var(--text-muted);
  margin-top: 4px;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
}

.data-table th, .data-table td {
  padding: 1rem 1.2rem;
  text-align: left;
  border-bottom: 1px solid var(--border);
}

.data-table th {
  background: #101614;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
}

.data-table tr:hover td {
  background: var(--bg-card-hover);
}

/* Forms */
.form-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 2rem;
  max-width: 800px;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  font-size: 0.9rem;
  font-weight: 600;
  color: #e2e8f0;
  margin-bottom: 0.5rem;
}

.form-input, .form-textarea, .form-select {
  width: 100%;
  padding: 0.75rem 1rem;
  background: var(--bg-input);
  border: 1px solid var(--border);
  border-radius: 8px;
  color: #fff;
  font-size: 0.95rem;
  font-family: inherit;
  transition: border-color 0.2s;
}

.form-input:focus, .form-textarea:focus, .form-select:focus {
  outline: none;
  border-color: var(--border-focus);
  box-shadow: 0 0 0 3px rgba(78, 122, 104, 0.2);
}

.form-hint {
  font-size: 0.82rem;
  color: var(--text-muted);
  margin-top: 0.4rem;
}

.alert {
  padding: 1rem 1.2rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  font-size: 0.95rem;
}

.alert-success {
  background: rgba(34, 197, 94, 0.15);
  border: 1px solid rgba(34, 197, 94, 0.3);
  color: #86efac;
}

.alert-error {
  background: rgba(239, 68, 68, 0.15);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #fca5a5;
}

/* Footer */
footer {
  background: #090c0b;
  border-top: 1px solid var(--border);
  padding: 4rem 0 2rem;
  color: var(--text-muted);
  font-size: 0.92rem;
}

.footer-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 3rem;
  margin-bottom: 3rem;
}

.footer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid var(--border);
  padding-top: 1.5rem;
  font-size: 0.85rem;
}

@media (max-width: 768px) {
  .nav-links { display: none; }
  .mobile-toggle { display: block; }
  .nav-links.open {
    display: flex;
    flex-direction: column;
    position: absolute;
    top: 72px;
    left: 0;
    right: 0;
    background: var(--bg-main);
    border-bottom: 1px solid var(--border);
    padding: 1.5rem;
    gap: 1.2rem;
  }
  .spotlight { grid-template-columns: 1fr; }
  .admin-wrap { flex-direction: column; }
  .admin-sidebar { width: 100%; border-right: none; border-bottom: 1px solid var(--border); }
  .footer-grid { grid-template-columns: 1fr; gap: 2rem; }
}
"""

def render_layout(title: str, content: str, current_path: str = "/", user: dict = None, settings: dict = None) -> str:
    settings = settings or {}
    site_title = html.escape(settings.get("site_title", "Pud a pohodlí"))
    site_sub = html.escape(settings.get("site_subtitle", "Pudlpointři, neurotyp pracovních psů ve světě povrchní kynologie"))
    
    admin_btn = ""
    if user:
        admin_btn = f"""
        <a href="/admin" class="btn btn-primary btn-sm">⚙️ Správa ({html.escape(user['display_name'])})</a>
        <a href="/admin/logout" class="btn btn-outline btn-sm">Odhlásit</a>
        """
    else:
        admin_btn = """<a href="/admin/login" class="btn btn-outline btn-sm">Správa webu</a>"""

    return f"""<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)} | {site_title}</title>
    <meta name="description" content="{html.escape(settings.get('site_description', ''))}">
    <style>{COMMON_CSS}</style>
</head>
<body>
    <header>
        <div class="container nav-wrap">
            <a href="/" class="logo-block">
                <span class="logo-title"><span class="logo-dot"></span>{site_title}</span>
                <span class="logo-subtitle">{site_sub}</span>
            </a>
            <button class="mobile-toggle" onclick="document.querySelector('.nav-links').classList.toggle('open')">☰</button>
            <ul class="nav-links">
                <li><a href="/" class="{'active' if current_path == '/' else ''}">Úvod</a></li>
                <li><a href="/manifest" class="{'active' if current_path == '/manifest' else ''}">Manifest</a></li>
                <li><a href="/pudlpointer" class="{'active' if current_path == '/pudlpointer' else ''}">O plemeni</a></li>
                <li><a href="/clanky" class="{'active' if current_path.startswith('/clanky') else ''}">Články & Úvahy</a></li>
                <li><a href="/galerie" class="{'active' if current_path == '/galerie' else ''}">Fotogalerie</a></li>
                <li><a href="/kontakt" class="{'active' if current_path == '/kontakt' else ''}">Kontakt</a></li>
                <li>{admin_btn}</li>
            </ul>
        </div>
    </header>

    <main>
        {content}
    </main>

    <footer>
        <div class="container">
            <div class="footer-grid">
                <div>
                    <h4 style="color:#fff; font-size:1.1rem; margin-bottom:0.8rem; font-weight:800;">{site_title}</h4>
                    <p style="margin-bottom:1rem; line-height:1.6; max-width:400px;">{site_sub}</p>
                    <p style="font-size:0.85rem; color:#6b7c75;">Nezávislá platforma věnovaná funkční kynologii, zachování pracovních vloh a otevřené diskuzi bez cenzury a populistických zkratek.</p>
                </div>
                <div>
                    <h5 style="color:#fff; font-size:0.9rem; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:1rem;">Navigace</h5>
                    <ul style="list-style:none; display:flex; flex-direction:column; gap:0.5rem;">
                        <li><a href="/manifest">Manifest: Pud & Pohodlí</a></li>
                        <li><a href="/pudlpointer">Plemeno Pudlpointer</a></li>
                        <li><a href="/clanky">Všechny články</a></li>
                        <li><a href="/galerie">Fotogalerie</a></li>
                        <li><a href="/kontakt">O autorech & Kontakt</a></li>
                    </ul>
                </div>
                <div>
                    <h5 style="color:#fff; font-size:0.9rem; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:1rem;">Administrace</h5>
                    <p style="font-size:0.85rem; margin-bottom:1rem;">Přístup pro autory a správce obsahu.</p>
                    <a href="/admin" class="btn btn-outline btn-sm">Vstup do redakce →</a>
                </div>
            </div>
            <div class="footer-bottom">
                <span>© {datetime.now().year} {site_title}. Všechna práva vyhrazena.</span>
                <span>Postaveno na míru pro autentickou pracovní kynologii</span>
            </div>
        </div>
    </footer>
</body>
</html>
"""

def render_home_page(settings: dict, articles: list, gallery: list) -> str:
    site_title = html.escape(settings.get("site_title", "Pud a pohodlí"))
    site_sub = html.escape(settings.get("site_subtitle", "Pudlpointři, neurotyp pracovních psů ve světě povrchní kynologie"))

    articles_html = ""
    for art in articles[:3]:
        cover = art["cover_image"] or "/static/img/sample-field.svg"
        articles_html += f"""
        <article class="article-card">
            <div class="article-img-wrap">
                <img src="{html.escape(cover)}" alt="{html.escape(art['title'])}" class="article-img">
            </div>
            <div class="article-body">
                <div class="article-meta">
                    <span class="article-tag">{html.escape(art['tags'].split(',')[0] if art['tags'] else 'Článek')}</span>
                    <span>•</span>
                    <span>{format_date(art['created_at'])}</span>
                </div>
                <h3 class="article-title">{html.escape(art['title'])}</h3>
                <p class="article-summary">{html.escape(art['summary'])}</p>
                <a href="/clanky/{art['slug']}" class="article-link">Číst celou úvahu →</a>
            </div>
        </article>
        """

    gallery_html = ""
    for item in gallery[:4]:
        gallery_html += f"""
        <div class="gallery-item">
            <img src="{html.escape(item['image_url'])}" alt="{html.escape(item['title'])}">
            <div class="gallery-overlay">
                <span style="color:var(--accent); font-size:0.75rem; font-weight:700; text-transform:uppercase;">{html.escape(item['category'] or 'Foto')}</span>
                <div class="gallery-title">{html.escape(item['title'])}</div>
                {f'<div class="gallery-desc">{html.escape(item["description"])}</div>' if item["description"] else ''}
            </div>
        </div>
        """

    return f"""
    <section class="hero">
        <div class="container">
            <span class="badge-tag">Biologie • Genetika • Skutečná praxe</span>
            <h1 class="hero-title">{site_title}</h1>
            <h2 class="hero-subtitle">{site_sub}</h2>
            <p class="hero-desc">
                Současná kynologie čelí vlně povrchního moralizování, kde se náročný neurotyp pracovního psa ořezává na míru modernímu lidskému komfortu. 
                Pudlpointer je pro nás symbolem rovnováhy: nekompromisní pracovní vlohy, tvrdost v terénu a přirozená inteligence, která nepotřebuje pozlátko.
            </p>
            <div class="hero-btns">
                <a href="/manifest" class="btn btn-primary">Číst náš manifest</a>
                <a href="/clanky" class="btn btn-outline">Otevřít články & úvahy</a>
            </div>
        </div>
    </section>

    <!-- Čtyři pilíře koncepce -->
    <section class="section">
        <div class="container">
            <div class="section-head">
                <div>
                    <div class="section-label">Koncept & Filozofie</div>
                    <h2 class="section-title">Proč odmítáme povrchní kynologii</h2>
                </div>
            </div>
            <div class="pillars-grid">
                <div class="pillar-card">
                    <span class="pillar-icon">🧬</span>
                    <h3 class="pillar-title">Náročný neurotyp</h3>
                    <p class="pillar-text">
                        Pracovní pes se nerodí jako prázdná tabule. Nese specifickou nervovou soustavu, vysoký vzruch (drive) a kořistnický pud, který nelze „odnaučit“ pamlskem, ale musí být pochopen a smysluplně využit.
                    </p>
                </div>
                <div class="pillar-card">
                    <span class="pillar-icon">⚡</span>
                    <h3 class="pillar-title">Pud vs. Pohodlí</h3>
                    <p class="pillar-text">
                        Civilizace směřuje k absenci diskomfortu. Když moderní člověk uzavře dravce do obýváku, často nazývá přirozené pudy agresí. Problém ale není v psovi, nýbrž v lidské neschopnosti unést realitu.
                    </p>
                </div>
                <div class="pillar-card">
                    <span class="pillar-icon">🎯</span>
                    <h3 class="pillar-title">Odmítnutí tabu</h3>
                    <p class="pillar-text">
                        Norování, ostrost na škodnou, chov striktně podle pracovních výkonů – témata, která internetoví teoretici snadno odsuzují, aniž by chápali biologickou a ekologickou podstatu věci.
                    </p>
                </div>
                <div class="pillar-card">
                    <span class="pillar-icon">🐕</span>
                    <h3 class="pillar-title">Pudlpointer jako etalon</h3>
                    <p class="pillar-text">
                        Geniální dílo barona Hegewalda. Plemeno, které vzniklo odmítnutím výstavního pozlátka ve prospěch funkčnosti, inteligence a neutuchající ochoty pracovat ve vodě i na souši.
                    </p>
                </div>
            </div>
        </div>
    </section>

    <!-- Spotlight Pudlpointer -->
    <section class="container">
        <div class="spotlight">
            <div>
                <span class="badge-tag" style="margin-bottom:0.8rem;">Plemeno s posláním</span>
                <h2 class="spotlight-title">Pudlpointer: Mistr rovnováhy</h2>
                <p class="spotlight-p">
                    Syntéza královského vodního pudla a anglického pointra. Žádné přešlechtění do anatomických bizarností, žádné ztráty funkčnosti. Pouze poctivá selekce na pevné nervy, excelentní nos a tvrdou pracovní chuť.
                </p>
                <a href="/pudlpointer" class="btn btn-outline">Prozkoumat profil plemene →</a>
            </div>
            <div class="spotlight-stats">
                <div class="stat-item">
                    <span class="stat-num">1881</span>
                    <span class="stat-label">Rok vzniku plemene</span>
                </div>
                <div class="stat-item">
                    <span class="stat-num">Všestrannost</span>
                    <span class="stat-label">Pole • Voda • Les</span>
                </div>
                <div class="stat-item">
                    <span class="stat-num">Pevné nervy</span>
                    <span class="stat-label">Vyrovnaný neurotyp</span>
                </div>
                <div class="stat-item">
                    <span class="stat-num">Bez kompromisů</span>
                    <span class="stat-label">Přísná selekce výkonu</span>
                </div>
            </div>
        </div>
    </section>

    <!-- Nejnovější články -->
    <section class="section">
        <div class="container">
            <div class="section-head">
                <div>
                    <div class="section-label">Odborné úvahy & Eseje</div>
                    <h2 class="section-title">Nejnovější texty</h2>
                </div>
                <a href="/clanky" class="btn btn-outline btn-sm">Zobrazit všechny články ({len(articles)}) →</a>
            </div>
            <div class="articles-grid">
                {articles_html}
            </div>
        </div>
    </section>

    <!-- Náhled galerie -->
    <section class="section" style="border-bottom:none;">
        <div class="container">
            <div class="section-head">
                <div>
                    <div class="section-label">Okamžiky z terénu</div>
                    <h2 class="section-title">Fotogalerie</h2>
                </div>
                <a href="/galerie" class="btn btn-outline btn-sm">Celá galerie →</a>
            </div>
            <div class="gallery-grid">
                {gallery_html}
            </div>
        </div>
    </section>
    """

def render_manifest_page() -> str:
    return """
    <div class="container" style="padding-top: 4rem; padding-bottom: 5rem;">
        <div style="max-width: 820px; margin: 0 auto;">
            <span class="badge-tag">Náš postoj</span>
            <h1 class="hero-title" style="margin-bottom: 1.5rem;">Manifest: Pud & Pohodlí</h1>
            <p style="font-size: 1.25rem; color: var(--accent); line-height: 1.5; margin-bottom: 3rem;">
                Proč kynologie 21. století potřebuje návrat k biologické pravdě a respektu k funkční selekci.
            </p>

            <div class="article-full-content" style="margin: 0; max-width: 100%;">
                <p class="lead">
                    Žijeme v době, která si podmanila vnější svět. Máme vyhřívané domy, aplikace na rozvoz jídla a neomezený komfort. 
                    Spolu s tímto pohodlím však lidská mysl získala nebezpečnou iluzi: pocit, že veškerá příroda je tvárná, 
                    že biologické pudy jsou přežitek a že každého tvora lze přetvořit k obrazu našeho vlastního mírumilovného zahálčení.
                </p>

                <h3>1. Pes není člověk ve zvířecím kožichu</h3>
                <p>
                    Největší tragédií moderního psa je jeho polidštění. Když zvířeti upřeme jeho druhovou a plemennou podstatu, 
                    nechováme se k němu s láskou – chováme se k němu s hlubokým sobectvím. Pracovní pes nebyl vytvořen pro to, 
                    aby suploval emocionální nedostatky člověka. Byl selektován po stovky generací k tomu, aby sledoval pachovou stopu, 
                    vystavoval zvěř, bojoval s překážkami v nepřístupném terénu a neochvějně plnil své biologické poslání.
                </p>

                <h3>2. Pokrytectví salonní kritiky</h3>
                <p>
                    V dnešní veřejné debatě je nesmírně snadné získat morální převahu. Stačí odsoudit norování, zkritizovat loveckou ostrost 
                    nebo prohlásit jakýkoliv projev dravého chování za „trauma a zkaženost“. Lidé, kteří tato prohlášení šíří, však často 
                    nemají ani ponětí o genetice, fungování neurotransmiterů v psím mozku ani o skutečných ekologických souvislostech.
                </p>
                <p>
                    Zatímco se moderní kynologie bouří proti tradičním disciplínám, v tichosti toleruje chov zvířat, která nemohou dýchat, 
                    jejichž klouby kolabují ve třech letech věku a jejichž nervová soustava je tak labilní, že propadají panice z pouhého šelestu listí. 
                    Toto je skutečná krutost – nikoliv zdravý pes pracující v lese.
                </p>

                <h3>3. Pudlpointer jako zhmotnění principu</h3>
                <p>
                    Pudlpointer pro nás není jen plemeno. Je to manifest sám o sobě. Když baron Hegewald v 19. století odmítl směr výstavních kruhů 
                    a zaměřil se na nekompromisní pracovní kvalitu, položil základ pro psa, který i dnes – v roce 2026 – představuje 
                    nedotčený diamant. Je to pes inteligentní, přemýšlivý, ale v práci tvrdý a neústupný.
                </p>

                <h3>4. Náš cíl</h3>
                <p>
                    Tento web vznikl proto, aby byl prostorem pro pravdu. Chceme sdílet zkušenosti z reálné praxe, otevírat témata, 
                    o kterých se na sociálních sítích mlčí ze strachu z lynče, a ukázat, že respekt k pracovnímu psovi začíná tam, 
                    kde končí lidská samolibost.
                </p>

                <div style="margin-top: 3rem; padding: 2rem; background: var(--bg-card); border-radius: 12px; border: 1px solid var(--border);">
                    <h4 style="color:#fff; margin-bottom: 0.5rem;">Chcete přispět svým pohledem?</h4>
                    <p style="color:var(--text-muted); font-size:0.95rem; margin-bottom: 1.2rem;">
                        Otevřená diskuze je vítána. Pokud máte zkušenosti s pracovní kynologií a chápete náš pohled, ozvěte se nám.
                    </p>
                    <a href="/kontakt" class="btn btn-primary btn-sm">Kontaktujte redakci</a>
                </div>
            </div>
        </div>
    </div>
    """

def render_pudelpointer_page() -> str:
    return """
    <div class="container" style="padding-top: 4rem; padding-bottom: 5rem;">
        <div style="max-width: 820px; margin: 0 auto;">
            <span class="badge-tag">Standard • Historie • Neurotyp</span>
            <h1 class="hero-title" style="margin-bottom: 1.5rem;">Plemeno Pudlpointer</h1>
            <p style="font-size: 1.25rem; color: var(--accent); line-height: 1.5; margin-bottom: 3rem;">
                Dokonalá fúze vody a větru: Proč toto lovecké plemeno odolalo módním vlnám a zachovalo si funkční mozek i tělo.
            </p>

            <div class="article-full-content" style="margin: 0; max-width: 100%;">
                <p class="lead">
                    Pudlpointer (FCI skupina 7, sekce 1.1) je jedinečný ohař. Nevznikl náhodou ani jako estetický experiment pro salónní obdivovatele. 
                    Byl vyšlechtěn s jasným záměrem: vytvořit ideálního všestranného loveckého psa schopného špičkové práce na poli, v lese i v hluboké vodě.
                </p>

                <h3>Geniální genetický tah: Královský pudl × Anglický pointer</h3>
                <p>
                    Dnešní veřejnost má pudla zafixovaného jako ostříhanou ozdobu francouzských promenád. Historicky však byl pudl (původně <em>Pudelhund</em>) 
                    mimořádně houževnatým vodním loveckým psem s fenomenální chutí přinášet a plavat i v ledovém rákosí. K tomu disponoval inteligencí, 
                    která mezi psími plemeny nemá obdoby.
                </p>
                <p>
                    Anglický pointer naproti tomu představoval absolutní špičku v rychlosti, jemnosti nosu a pevném vystavování pernaté zvěře na otevřených pláních. 
                    Spojením těchto dvou zdánlivě odlišných pólů vytvořil baron von Zedlitz psa, který spojil loveckou vášeň s neobyčejnou chápavostí a věrností vůdci.
                </p>

                <h3>Nervová soustava: Vyrovnanost a pracovní přepínač</h3>
                <p>
                    Co činí pudlpointra výjimečným z hlediska etologie a neurotypu?
                </p>
                <ul>
                    <li><strong>Vysoká chuť k práci bez hysterie:</strong> Na rozdíl od některých moderních plemen, která jsou přešlechtěna do permanentního stresového vzruchu, má pudlpointer pevnou centrální nervovou soustavu. V poli pracuje s maximálním nasazením, doma dokáže naprosto klidně odpočívat.</li>
                    <li><strong>Vrozená ochota k poslušnosti:</strong> Dědictví po pudlovi se projevuje silnou touhou po spolupráci s vůdcem (tzv. <em>will to please</em>), aniž by pes ztratil samostatný úsudek při práci na stopě.</li>
                    <li><strong>Tvrdost a odolnost:</strong> Hustá, hrubá srst s podsadou a vousatý čenich chrání psa před zraněním v nejtvrdším trní a ledové vodě.</li>
                </ul>

                <h3>Pro koho pudlpointer JE a pro koho NENÍ</h3>
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:1.5rem; margin: 2rem 0;">
                    <div style="background:var(--bg-card); padding:1.5rem; border-radius:10px; border-left:3px solid #22c55e;">
                        <h4 style="color:#86efac; margin-bottom:0.8rem;">Pudlpointer JE pro:</h4>
                        <ul style="font-size:0.95rem; margin:0 0 0 1.2rem; color:#cbdad3;">
                            <li>Aktivní myslivce a kynology hledající všestrannost</li>
                            <li>Lidi schopné dát psovi reálný úkol v přírodě</li>
                            <li>Vůdce, kteří chápou biologickou podstatu pudů</li>
                            <li>Ty, kdo ocení drsnou přírodní krásu a funkčnost</li>
                        </ul>
                    </div>
                    <div style="background:var(--bg-card); padding:1.5rem; border-radius:10px; border-left:3px solid #ef4444;">
                        <h4 style="color:#fca5a5; margin-bottom:0.8rem;">Pudlpointer NENÍ pro:</h4>
                        <ul style="font-size:0.95rem; margin:0 0 0 1.2rem; color:#cbdad3;">
                            <li>Lidi hledající nenáročného „městského společníka“</li>
                            <li>Ty, kdo chtějí psa zabavit jen občasným házením míčku</li>
                            <li>Zastánce čistě pasivního životního stylu</li>
                            <li>Lidi, kteří se štítí bahna, vody a syrové přírody</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """

def render_articles_list(articles: list) -> str:
    cards = ""
    for art in articles:
        cover = art["cover_image"] or "/static/img/sample-field.svg"
        cards += f"""
        <article class="article-card">
            <div class="article-img-wrap">
                <img src="{html.escape(cover)}" alt="{html.escape(art['title'])}" class="article-img">
            </div>
            <div class="article-body">
                <div class="article-meta">
                    <span class="article-tag">{html.escape(art['tags'].split(',')[0] if art['tags'] else 'Článek')}</span>
                    <span>•</span>
                    <span>{format_date(art['created_at'])}</span>
                </div>
                <h3 class="article-title">{html.escape(art['title'])}</h3>
                <p class="article-summary">{html.escape(art['summary'])}</p>
                <a href="/clanky/{art['slug']}" class="article-link">Číst celou úvahu →</a>
            </div>
        </article>
        """

    return f"""
    <div class="container" style="padding-top: 4rem; padding-bottom: 5rem;">
        <div class="section-head">
            <div>
                <div class="section-label">Archiv úvah a esejů</div>
                <h1 class="section-title">Články & Odborné texty</h1>
                <p style="color:var(--text-muted); margin-top:0.5rem; font-size:1.1rem; max-width:650px;">
                    Biologie, neurotyp, genetika a střet skutečné práce s moderními kynologickými mýty.
                </p>
            </div>
        </div>
        <div class="articles-grid">
            {cards}
        </div>
    </div>
    """

def render_article_detail(art: dict) -> str:
    cover_html = ""
    if art["cover_image"]:
        cover_html = f"""
        <div style="max-width: 900px; margin: 0 auto 3rem; border-radius: 12px; overflow: hidden; border: 1px solid var(--border); max-height: 480px;">
            <img src="{html.escape(art['cover_image'])}" alt="{html.escape(art['title'])}" style="width:100%; height:100%; object-fit:cover;">
        </div>
        """

    return f"""
    <article>
        <div class="container article-header">
            <div style="max-width: 820px; margin: 0 auto;">
                <div class="article-meta" style="margin-bottom: 1.2rem;">
                    <a href="/clanky" style="color:var(--accent); font-weight:700;">← Zpět na články</a>
                    <span>•</span>
                    <span class="article-tag">{html.escape(art['tags'] or 'Úvaha')}</span>
                    <span>•</span>
                    <span>{format_date(art['created_at'])}</span>
                </div>
                <h1 class="article-full-title">{html.escape(art['title'])}</h1>
                {f'<p class="article-full-subtitle">{html.escape(art["subtitle"])}</p>' if art["subtitle"] else ''}
            </div>
        </div>

        <div class="container">
            {cover_html}
            <div class="article-full-content">
                {art['content']}
            </div>
        </div>
    </article>
    """

def render_gallery_page(items: list) -> str:
    gallery_html = ""
    for item in items:
        gallery_html += f"""
        <div class="gallery-item">
            <img src="{html.escape(item['image_url'])}" alt="{html.escape(item['title'])}">
            <div class="gallery-overlay">
                <span style="color:var(--accent); font-size:0.75rem; font-weight:700; text-transform:uppercase;">{html.escape(item['category'] or 'Foto')}</span>
                <div class="gallery-title">{html.escape(item['title'])}</div>
                {f'<div class="gallery-desc">{html.escape(item["description"])}</div>' if item["description"] else ''}
            </div>
        </div>
        """

    return f"""
    <div class="container" style="padding-top: 4rem; padding-bottom: 5rem;">
        <div class="section-head">
            <div>
                <div class="section-label">Momenty ze života a výcviku</div>
                <h1 class="section-title">Fotogalerie</h1>
                <p style="color:var(--text-muted); margin-top:0.5rem; font-size:1.1rem; max-width:650px;">
                    Záběry z práce na poli, vodě a v lese. Autentické momenty bez aranžmá.
                </p>
            </div>
        </div>
        <div class="gallery-grid">
            {gallery_html}
        </div>
    </div>
    """

def render_contact_page(settings: dict) -> str:
    email = html.escape(settings.get("contact_email", "info@pudapohodli.cz"))
    bio = html.escape(settings.get("author_bio", ""))
    return f"""
    <div class="container" style="padding-top: 4rem; padding-bottom: 5rem;">
        <div style="max-width: 760px; margin: 0 auto;">
            <span class="badge-tag">Kdo jsme</span>
            <h1 class="hero-title" style="margin-bottom: 1.5rem;">O autorech & Kontakt</h1>
            <p style="font-size: 1.15rem; color: #cbdad3; line-height: 1.8; margin-bottom: 2.5rem;">
                {bio}
            </p>

            <div style="background:var(--bg-card); border:1px solid var(--border); border-radius:12px; padding:2.5rem; margin-bottom:2.5rem;">
                <h3 style="color:#fff; margin-bottom:1.2rem; font-size:1.3rem;">Spojte se s námi</h3>
                <p style="color:var(--text-muted); margin-bottom:1.5rem;">
                    Máte dotaz k plemeni pudlpointer, k chovu, výcviku nebo chcete nabídnout vlastní odborný text k publikaci? 
                    Napište nám přímo na e-mail:
                </p>
                <div style="font-size:1.3rem; font-weight:700; color:var(--accent); margin-bottom:1.5rem;">
                    📧 {email}
                </div>
                <p style="font-size:0.9rem; color:var(--text-muted);">
                    Rádi diskutujeme s lidmi, kteří mají praktické zkušenosti a nebojí se dívat na kynologii bez přetvářky.
                </p>
            </div>
        </div>
    </div>
    """

# ================= ADMIN TEMPLATES =================

def render_admin_shell(title: str, content: str, current_tab: str = "dashboard", user: dict = None, message: str = None, error: str = None) -> str:
    msg_html = f'<div class="alert alert-success">{html.escape(message)}</div>' if message else ""
    err_html = f'<div class="alert alert-error">{html.escape(error)}</div>' if error else ""

    return f"""<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)} | Redakce Pud a pohodlí</title>
    <style>{COMMON_CSS}</style>
</head>
<body>
    <header>
        <div class="container nav-wrap">
            <a href="/" class="logo-block">
                <span class="logo-title"><span class="logo-dot"></span>Pud a pohodlí</span>
                <span class="logo-subtitle">Administrace & Redakce</span>
            </a>
            <div style="display:flex; align-items:center; gap:1rem;">
                <a href="/" target="_blank" class="btn btn-outline btn-sm">Zobrazit web ↗</a>
                <span style="font-size:0.85rem; color:var(--text-muted);">Přihlášen: <strong style="color:#fff;">{html.escape(user['display_name'])}</strong></span>
                <a href="/admin/logout" class="btn btn-danger btn-sm">Odhlásit</a>
            </div>
        </div>
    </header>

    <div class="admin-wrap">
        <aside class="admin-sidebar">
            <div class="admin-sidebar-title">Správa obsahu</div>
            <a href="/admin" class="admin-link {'active' if current_tab == 'dashboard' else ''}">📊 Přehled</a>
            <a href="/admin/articles" class="admin-link {'active' if current_tab == 'articles' else ''}">📝 Články a texty</a>
            <a href="/admin/gallery" class="admin-link {'active' if current_tab == 'gallery' else ''}">🖼️ Fotogalerie</a>
            
            <div class="admin-sidebar-title" style="margin-top:1.5rem;">Nastavení</div>
            <a href="/admin/users" class="admin-link {'active' if current_tab == 'users' else ''}">👥 Správci & Uživatelé</a>
            <a href="/admin/settings" class="admin-link {'active' if current_tab == 'settings' else ''}">⚙️ Nastavení webu</a>
            <a href="/admin/account" class="admin-link {'active' if current_tab == 'account' else ''}">🔑 Změna hesla</a>
        </aside>

        <section class="admin-content">
            {msg_html}
            {err_html}
            {content}
        </section>
    </div>
</body>
</html>
"""

def render_admin_login(error: str = None) -> str:
    err_html = f'<div class="alert alert-error">{html.escape(error)}</div>' if error else ""
    return f"""<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Přihlášení do redakce | Pud a pohodlí</title>
    <style>{COMMON_CSS}</style>
</head>
<body style="display:flex; align-items:center; justify-content:center; min-height:100vh; padding:1.5rem;">
    <div class="form-card" style="width:100%; max-width:420px;">
        <div style="text-align:center; margin-bottom:2rem;">
            <div class="logo-dot" style="margin:0 auto 12px; display:block;"></div>
            <h1 style="font-size:1.6rem; color:#fff; font-weight:800;">Redakce</h1>
            <p style="color:var(--text-muted); font-size:0.9rem;">Pud a pohodlí – Správa obsahu</p>
        </div>
        {err_html}
        <form method="POST" action="/admin/login">
            <div class="form-group">
                <label class="form-label">Uživatelské jméno</label>
                <input type="text" name="username" class="form-input" required autofocus placeholder="např. admin">
            </div>
            <div class="form-group">
                <label class="form-label">Heslo</label>
                <input type="password" name="password" class="form-input" required placeholder="Vaše heslo">
            </div>
            <button type="submit" class="btn btn-primary" style="width:100%; padding:0.8rem; margin-top:1rem;">Přihlásit se do administrace</button>
        </form>
        <div style="text-align:center; margin-top:2rem;">
            <a href="/" style="font-size:0.85rem; color:var(--text-muted);">← Zpět na web</a>
        </div>
    </div>
</body>
</html>
"""

def render_admin_dashboard(stats: dict, recent_articles: list, recent_photos: list) -> str:
    articles_rows = ""
    for a in recent_articles:
        articles_rows += f"""
        <tr>
            <td><strong>{html.escape(a['title'])}</strong></td>
            <td><span class="badge-tag" style="margin:0; font-size:0.75rem;">{'Publikováno' if a['is_published'] else 'Koncept'}</span></td>
            <td>{format_date(a['created_at'])}</td>
            <td>
                <a href="/admin/articles/edit?id={a['id']}" class="btn btn-outline btn-sm">Upravit</a>
            </td>
        </tr>
        """

    return f"""
    <div class="admin-header">
        <div>
            <h1 class="admin-title">Přehled redakce</h1>
            <p style="color:var(--text-muted); font-size:0.95rem;">Vítejte v redakčním systému webu Pud a pohodlí.</p>
        </div>
        <div style="display:flex; gap:0.8rem;">
            <a href="/admin/articles/new" class="btn btn-primary">+ Nový článek</a>
            <a href="/admin/gallery" class="btn btn-outline">+ Nahrát fotku</a>
        </div>
    </div>

    <div class="stats-grid">
        <div class="stat-box">
            <div class="stat-box-num">{stats['articles_count']}</div>
            <div class="stat-box-label">Publikovaných článků</div>
        </div>
        <div class="stat-box">
            <div class="stat-box-num">{stats['photos_count']}</div>
            <div class="stat-box-label">Fotografií v galerii</div>
        </div>
        <div class="stat-box">
            <div class="stat-box-num">{stats['users_count']}</div>
            <div class="stat-box-label">Správců s přístupem</div>
        </div>
    </div>

    <div style="margin-top:2.5rem;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
            <h3 style="color:#fff; font-size:1.2rem;">Nedávné články</h3>
            <a href="/admin/articles" style="font-size:0.85rem; color:var(--accent);">Zobrazit všechny →</a>
        </div>
        <table class="data-table">
            <thead>
                <tr>
                    <th>Název</th>
                    <th>Stav</th>
                    <th>Datum</th>
                    <th>Akce</th>
                </tr>
            </thead>
            <tbody>
                {articles_rows if articles_rows else '<tr><td colspan="4" style="text-align:center; color:var(--text-muted);">Zatím žádné články</td></tr>'}
            </tbody>
        </table>
    </div>
    """

def render_admin_articles_list(articles: list) -> str:
    rows = ""
    for a in articles:
        rows += f"""
        <tr>
            <td>
                <div style="font-weight:700; color:#fff;">{html.escape(a['title'])}</div>
                <div style="font-size:0.8rem; color:var(--text-muted);">{html.escape(a['summary'][:90])}...</div>
            </td>
            <td><span class="badge-tag" style="margin:0; font-size:0.75rem;">{'Publikováno' if a['is_published'] else 'Koncept'}</span></td>
            <td>{html.escape(a['author_name'] or 'Správce')}</td>
            <td>{format_date(a['created_at'])}</td>
            <td style="white-space:nowrap;">
                <a href="/clanky/{a['slug']}" target="_blank" class="btn btn-outline btn-sm">Náhled</a>
                <a href="/admin/articles/edit?id={a['id']}" class="btn btn-primary btn-sm">Upravit</a>
                <a href="/admin/articles/delete?id={a['id']}" onclick="return confirm('Opravdu chcete smazat tento článek?')" class="btn btn-danger btn-sm">Smazat</a>
            </td>
        </tr>
        """

    return f"""
    <div class="admin-header">
        <div>
            <h1 class="admin-title">Správa článků a esejů</h1>
            <p style="color:var(--text-muted); font-size:0.95rem;">Zde můžete psát, upravovat a publikovat články.</p>
        </div>
        <a href="/admin/articles/new" class="btn btn-primary">+ Napsat nový článek</a>
    </div>

    <table class="data-table">
        <thead>
            <tr>
                <th style="width:45%;">Článek</th>
                <th>Stav</th>
                <th>Autor</th>
                <th>Datum</th>
                <th>Akce</th>
            </tr>
        </thead>
        <tbody>
            {rows if rows else '<tr><td colspan="5" style="text-align:center; color:var(--text-muted);">Zatím žádné články</td></tr>'}
        </tbody>
    </table>
    """

def render_admin_article_form(article: dict = None) -> str:
    is_edit = article is not None
    title = article["title"] if is_edit else ""
    subtitle = article["subtitle"] if is_edit else ""
    slug = article["slug"] if is_edit else ""
    summary = article["summary"] if is_edit else ""
    content = article["content"] if is_edit else ""
    tags = article["tags"] if is_edit else ""
    cover_image = article["cover_image"] if is_edit else ""
    is_published = article["is_published"] if is_edit else 1
    art_id = article["id"] if is_edit else ""

    action = f"/admin/articles/edit?id={art_id}" if is_edit else "/admin/articles/new"

    return f"""
    <div class="admin-header">
        <div>
            <h1 class="admin-title">{'Upravit článek' if is_edit else 'Nový článek'}</h1>
            <p style="color:var(--text-muted); font-size:0.95rem;">Vytvořte odborný text nebo esej.</p>
        </div>
        <a href="/admin/articles" class="btn btn-outline btn-sm">← Zpět na seznam</a>
    </div>

    <div class="form-card" style="max-width:900px;">
        <form method="POST" action="{action}" enctype="multipart/form-data">
            <div class="form-group">
                <label class="form-label">Hlavní název článku *</label>
                <input type="text" name="title" class="form-input" value="{html.escape(title)}" required placeholder="např. Neurotyp pracovního psa...">
            </div>

            <div class="form-group">
                <label class="form-label">Podtitul článku</label>
                <input type="text" name="subtitle" class="form-input" value="{html.escape(subtitle)}" placeholder="např. Biologická realita nervové soustavy...">
            </div>

            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:1.5rem;">
                <div class="form-group">
                    <label class="form-label">URL Slug (zkratka v adrese)</label>
                    <input type="text" name="slug" class="form-input" value="{html.escape(slug)}" placeholder="neurotyp-psa (nechte prázdné pro automatické vygenerování)">
                    <div class="form-hint">Zobrazí se jako adresa článku: /clanky/vas-slug</div>
                </div>
                <div class="form-group">
                    <label class="form-label">Štítky / Kategorie (oddělené čárkou)</label>
                    <input type="text" name="tags" class="form-input" value="{html.escape(tags)}" placeholder="Neurotyp, Etologie, Pudlpointer">
                </div>
            </div>

            <div class="form-group">
                <label class="form-label">Titulní fotografie</label>
                {f'<div style="margin-bottom:0.5rem; font-size:0.85rem; color:var(--accent);">Aktuální foto: {html.escape(cover_image)}</div>' if cover_image else ''}
                <input type="file" name="cover_file" class="form-input" accept="image/*">
                <div class="form-hint">Nebo zadejte přímou URL adresu obrázku:</div>
                <input type="text" name="cover_image" class="form-input" style="margin-top:0.4rem;" value="{html.escape(cover_image)}" placeholder="/static/img/sample-field.svg nebo https://...">
            </div>

            <div class="form-group">
                <label class="form-label">Stručný souhrn / Perex (1-2 věty) *</label>
                <textarea name="summary" class="form-textarea" rows="3" required placeholder="Krátký úvod, který se zobrazí v kartě článku...">{html.escape(summary)}</textarea>
            </div>

            <div class="form-group">
                <label class="form-label">Obsah článku (HTML nebo odstavce) *</label>
                <div class="form-hint" style="margin-bottom:0.5rem;">Můžete použít běžné odstavce nebo HTML značky jako &lt;h3&gt;, &lt;p&gt;, &lt;ul&gt;, &lt;li&gt;, &lt;strong&gt;.</div>
                <textarea name="content" class="form-textarea" rows="16" required style="font-family:monospace; font-size:0.9rem;">{html.escape(content)}</textarea>
            </div>

            <div class="form-group" style="display:flex; align-items:center; gap:0.8rem; background:var(--bg-input); padding:1rem; border-radius:8px; border:1px solid var(--border);">
                <input type="checkbox" id="is_published" name="is_published" value="1" {'checked' if is_published else ''} style="width:20px; height:20px;">
                <label for="is_published" style="color:#fff; font-weight:600; cursor:pointer;">Publikovat ihned na webu (pokud není zaškrtnuto, uloží se jako koncept)</label>
            </div>

            <div style="display:flex; gap:1rem; margin-top:2rem;">
                <button type="submit" class="btn btn-primary" style="padding:0.8rem 2rem;">Uložit článek</button>
                <a href="/admin/articles" class="btn btn-outline">Zrušit</a>
            </div>
        </form>
    </div>
    """

def render_admin_gallery(items: list) -> str:
    cards = ""
    for item in items:
        cards += f"""
        <div style="background:var(--bg-card); border:1px solid var(--border); border-radius:10px; overflow:hidden; display:flex; flex-direction:column;">
            <div style="height:170px; background:#18221f;">
                <img src="{html.escape(item['image_url'])}" style="width:100%; height:100%; object-fit:cover;">
            </div>
            <div style="padding:1rem; flex-grow:1; display:flex; flex-direction:column; justify-content:space-between;">
                <div>
                    <span class="badge-tag" style="margin:0 0 6px; font-size:0.7rem;">{html.escape(item['category'] or 'Obecné')}</span>
                    <h4 style="color:#fff; font-size:1rem; margin-bottom:4px;">{html.escape(item['title'])}</h4>
                    <p style="font-size:0.8rem; color:var(--text-muted);">{html.escape(item['description'] or '')}</p>
                </div>
                <div style="margin-top:1rem; padding-top:0.8rem; border-top:1px solid var(--border); display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-size:0.75rem; color:var(--text-muted);">{format_date(item['created_at'])}</span>
                    <a href="/admin/gallery/delete?id={item['id']}" onclick="return confirm('Smazat tuto fotografii?')" class="btn btn-danger btn-sm">Smazat</a>
                </div>
            </div>
        </div>
        """

    return f"""
    <div class="admin-header">
        <div>
            <h1 class="admin-title">Správa fotogalerie</h1>
            <p style="color:var(--text-muted); font-size:0.95rem;">Nahrávejte fotografie přímo z mobilu nebo počítače.</p>
        </div>
    </div>

    <!-- Upload form -->
    <div class="form-card" style="margin-bottom:3rem; max-width:850px;">
        <h3 style="color:#fff; font-size:1.2rem; margin-bottom:1.2rem;">📸 Nahrát novou fotografii</h3>
        <form method="POST" action="/admin/gallery/upload" enctype="multipart/form-data">
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:1.2rem;">
                <div class="form-group">
                    <label class="form-label">Vyberte fotografii ze zařízení (JPG, PNG, WEBP) *</label>
                    <input type="file" name="photo_file" class="form-input" accept="image/*" required>
                </div>
                <div class="form-group">
                    <label class="form-label">Název / Popisek *</label>
                    <input type="text" name="title" class="form-input" required placeholder="např. Pudlpointer na poli...">
                </div>
            </div>
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:1.2rem;">
                <div class="form-group">
                    <label class="form-label">Kategorie</label>
                    <input type="text" name="category" class="form-input" placeholder="např. Pole, Voda, Les, Trénink">
                </div>
                <div class="form-group">
                    <label class="form-label">Podrobnější popis (volitelné)</label>
                    <input type="text" name="description" class="form-input" placeholder="např. Podzimní zkoušky vloh...">
                </div>
            </div>
            <button type="submit" class="btn btn-primary" style="margin-top:0.5rem;">Nahrát fotku na web</button>
        </form>
    </div>

    <!-- Gallery items grid -->
    <h3 style="color:#fff; font-size:1.2rem; margin-bottom:1.2rem;">Všechny nahrané fotografie ({len(items)})</h3>
    <div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(260px, 1fr)); gap:1.5rem;">
        {cards if cards else '<p style="color:var(--text-muted);">Zatím žádné fotografie</p>'}
    </div>
    """

def render_admin_users(users: list) -> str:
    rows = ""
    for u in users:
        if u["username"] != "admin":
            user_esc = html.escape(u["username"])
            action_btn = f'<a href="/admin/users/delete?id={u["id"]}" onclick="return confirm(\'Opravdu smazat účet {user_esc}?\')" class="btn btn-danger btn-sm">Odebrat</a>'
        else:
            action_btn = '<span style="color:var(--text-muted); font-size:0.8rem;">Hlavní účet</span>'

        rows += f"""
        <tr>
            <td><strong style="color:#fff;">{html.escape(u['username'])}</strong></td>
            <td>{html.escape(u['display_name'])}</td>
            <td><span class="badge-tag" style="margin:0; font-size:0.75rem;">{html.escape(u['role'])}</span></td>
            <td>{format_date(u['created_at'])}</td>
            <td>
                {action_btn}
            </td>
        </tr>
        """

    return f"""
    <div class="admin-header">
        <div>
            <h1 class="admin-title">Správa uživatelů a spoluautorů</h1>
            <p style="color:var(--text-muted); font-size:0.95rem;">Zde můžete udělit přístup další osobě, aby mohla ze svého zařízení přidávat fotky a texty.</p>
        </div>
    </div>

    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:2.5rem; align-items:start;">
        <!-- Seznam uživatelů -->
        <div>
            <h3 style="color:#fff; font-size:1.2rem; margin-bottom:1rem;">Aktivní správci</h3>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Uživatel</th>
                        <th>Jméno</th>
                        <th>Role</th>
                        <th>Vytvořen</th>
                        <th>Akce</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>

        <!-- Formulář na přidání nového správce -->
        <div class="form-card">
            <h3 style="color:#fff; font-size:1.2rem; margin-bottom:1.2rem;">👤 Přidat nového správce / autora</h3>
            <p style="color:var(--text-muted); font-size:0.88rem; margin-bottom:1.5rem;">
                Vytvořte přihlašovací údaje pro kolegu nebo partnera. Bude se moci přihlásit ze svého mobilu nebo PC a rovnou vkládat obsah.
            </p>
            <form method="POST" action="/admin/users/new">
                <div class="form-group">
                    <label class="form-label">Uživatelské jméno (pro přihlášení) *</label>
                    <input type="text" name="username" class="form-input" required placeholder="např. karel, lenka">
                </div>
                <div class="form-group">
                    <label class="form-label">Zobrazované jméno (autor článků) *</label>
                    <input type="text" name="display_name" class="form-input" required placeholder="např. Karel Novák">
                </div>
                <div class="form-group">
                    <label class="form-label">Heslo pro nový účet *</label>
                    <input type="password" name="password" class="form-input" required placeholder="Bezpečné heslo">
                </div>
                <div class="form-group">
                    <label class="form-label">Oprávnění (Role)</label>
                    <select name="role" class="form-select">
                        <option value="admin">Správce (plná práva na články, fotky i uživatele)</option>
                        <option value="editor">Editor (může psát články a nahrávat fotky)</option>
                    </select>
                </div>
                <button type="submit" class="btn btn-primary" style="width:100%; margin-top:0.5rem;">Vytvořit účet správce</button>
            </form>
        </div>
    </div>
    """

def render_admin_settings(settings: dict) -> str:
    return f"""
    <div class="admin-header">
        <div>
            <h1 class="admin-title">Nastavení webu</h1>
            <p style="color:var(--text-muted); font-size:0.95rem;">Základní identita, texty a kontaktní údaje webu.</p>
        </div>
    </div>

    <div class="form-card" style="max-width:800px;">
        <form method="POST" action="/admin/settings">
            <div class="form-group">
                <label class="form-label">Hlavní název webu *</label>
                <input type="text" name="site_title" class="form-input" value="{html.escape(settings.get('site_title', 'Pud a pohodlí'))}" required>
            </div>

            <div class="form-group">
                <label class="form-label">Podtitul webu *</label>
                <input type="text" name="site_subtitle" class="form-input" value="{html.escape(settings.get('site_subtitle', ''))}" required>
            </div>

            <div class="form-group">
                <label class="form-label">Popis webu pro vyhledávače (SEO description)</label>
                <textarea name="site_description" class="form-textarea" rows="3">{html.escape(settings.get('site_description', ''))}</textarea>
            </div>

            <div class="form-group">
                <label class="form-label">O autorech (text zobrazený na stránce kontakt)</label>
                <textarea name="author_bio" class="form-textarea" rows="4">{html.escape(settings.get('author_bio', ''))}</textarea>
            </div>

            <div class="form-group">
                <label class="form-label">Kontaktní e-mail</label>
                <input type="email" name="contact_email" class="form-input" value="{html.escape(settings.get('contact_email', ''))}">
            </div>

            <button type="submit" class="btn btn-primary" style="margin-top:1rem; padding:0.8rem 2rem;">Uložit změny v nastavení</button>
        </form>
    </div>
    """

def render_admin_account() -> str:
    return """
    <div class="admin-header">
        <div>
            <h1 class="admin-title">Změna hesla</h1>
            <p style="color:var(--text-muted); font-size:0.95rem;">Změna přihlašovacího hesla k vašemu aktuálnímu účtu.</p>
        </div>
    </div>

    <div class="form-card" style="max-width:500px;">
        <form method="POST" action="/admin/account">
            <div class="form-group">
                <label class="form-label">Současné heslo *</label>
                <input type="password" name="current_password" class="form-input" required>
            </div>
            <div class="form-group">
                <label class="form-label">Nové heslo *</label>
                <input type="password" name="new_password" class="form-input" required minlength="6">
            </div>
            <div class="form-group">
                <label class="form-label">Potvrzení nového hesla *</label>
                <input type="password" name="confirm_password" class="form-input" required minlength="6">
            </div>
            <button type="submit" class="btn btn-primary" style="margin-top:1rem;">Změnit heslo</button>
        </form>
    </div>
    """
