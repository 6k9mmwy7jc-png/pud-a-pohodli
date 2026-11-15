import http.server
import urllib.parse
import os
import sys
import mimetypes
import cgi
import re
import secrets
from http import cookies
from datetime import datetime

import database
import templates

PORT = int(os.environ.get("PORT", 8080))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
STATIC_DIR = os.path.join(BASE_DIR, "static")

os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

def slugify(text: str) -> str:
    # Basic Czech char conversion
    char_map = {
        'á': 'a', 'č': 'c', 'ď': 'd', 'é': 'e', 'ě': 'e', 'í': 'i', 'ň': 'n',
        'ó': 'o', 'ř': 'r', 'š': 's', 'ť': 't', 'ú': 'u', 'ů': 'u', 'ý': 'y', 'ž': 'z',
        'Á': 'a', 'Č': 'c', 'Ď': 'd', 'É': 'e', 'Ě': 'e', 'Í': 'i', 'Ň': 'n',
        'Ó': 'o', 'Ř': 'r', 'Š': 's', 'Ť': 't', 'Ú': 'u', 'Ů': 'u', 'Ý': 'y', 'Ž': 'z'
    }
    for k, v in char_map.items():
        text = text.replace(k, v)
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text).strip('-')
    return text or "clanek"

class CMSRequestHandler(http.server.BaseHTTPRequestHandler):

    def get_cookie(self, name: str):
        cookie_header = self.headers.get("Cookie")
        if not cookie_header:
            return None
        c = cookies.SimpleCookie()
        try:
            c.load(cookie_header)
            if name in c:
                return c[name].value
        except Exception:
            pass
        return None

    def get_current_user(self):
        token = self.get_cookie("session_token")
        if not token:
            return None
        return database.get_user_by_session(token)

    def send_html(self, html_content: str, status: int = 200, set_cookies: list = None):
        body = html_content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        if set_cookies:
            for sc in set_cookies:
                self.send_header("Set-Cookie", sc)
        self.end_headers()
        self.wfile.write(body)

    def send_redirect(self, location: str, set_cookies: list = None):
        self.send_response(303)
        self.send_header("Location", location)
        if set_cookies:
            for sc in set_cookies:
                self.send_header("Set-Cookie", sc)
        self.end_headers()

    def serve_file(self, full_path: str):
        if not os.path.exists(full_path) or os.path.isdir(full_path):
            self.send_error(404, "File Not Found")
            return
        
        mime_type, _ = mimetypes.guess_type(full_path)
        if not mime_type:
            mime_type = "application/octet-stream"

        file_size = os.path.getsize(full_path)
        self.send_response(200)
        self.send_header("Content-Type", mime_type)
        self.send_header("Content-Length", str(file_size))
        self.send_header("Cache-Control", "public, max-age=86400")
        self.end_headers()

        with open(full_path, "rb") as f:
            while chunk := f.read(65536):
                self.wfile.write(chunk)

    def parse_form_data(self):
        content_type = self.headers.get("Content-Type", "")
        if "multipart/form-data" in content_type:
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    "REQUEST_METHOD": "POST",
                    "CONTENT_TYPE": content_type,
                }
            )
            data = {}
            files = {}
            for key in form.keys():
                item = form[key]
                if item.filename:
                    files[key] = item
                else:
                    data[key] = item.value
            return data, files
        else:
            length = int(self.headers.get("Content-Length", 0))
            raw_data = self.rfile.read(length).decode("utf-8")
            parsed = urllib.parse.parse_qs(raw_data)
            data = {k: v[0] for k, v in parsed.items()}
            return data, {}

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query = urllib.parse.parse_qs(parsed_url.query)

        # Static files
        if path.startswith("/static/"):
            rel_path = path[8:]
            full_path = os.path.join(STATIC_DIR, rel_path)
            self.serve_file(full_path)
            return

        # Uploaded files
        if path.startswith("/uploads/"):
            rel_path = path[9:]
            full_path = os.path.join(UPLOADS_DIR, rel_path)
            self.serve_file(full_path)
            return

        settings = database.get_settings()
        user = self.get_current_user()

        # ================= PUBLIC ROUTES =================
        if path == "/":
            conn = database.get_connection()
            c = conn.cursor()
            c.execute("SELECT * FROM articles WHERE is_published = 1 ORDER BY created_at DESC")
            articles = [dict(r) for r in c.fetchall()]
            c.execute("SELECT * FROM gallery ORDER BY created_at DESC LIMIT 8")
            gallery = [dict(r) for r in c.fetchall()]
            conn.close()

            content = templates.render_home_page(settings, articles, gallery)
            html_out = templates.render_layout("Úvod", content, current_path="/", user=user, settings=settings)
            self.send_html(html_out)
            return

        elif path == "/manifest":
            content = templates.render_manifest_page()
            html_out = templates.render_layout("Manifest", content, current_path="/manifest", user=user, settings=settings)
            self.send_html(html_out)
            return

        elif path == "/pudlpointer":
            content = templates.render_pudelpointer_page()
            html_out = templates.render_layout("O plemeni Pudlpointer", content, current_path="/pudlpointer", user=user, settings=settings)
            self.send_html(html_out)
            return

        elif path == "/clanky":
            conn = database.get_connection()
            c = conn.cursor()
            c.execute("SELECT * FROM articles WHERE is_published = 1 ORDER BY created_at DESC")
            articles = [dict(r) for r in c.fetchall()]
            conn.close()

            content = templates.render_articles_list(articles)
            html_out = templates.render_layout("Články a úvahy", content, current_path="/clanky", user=user, settings=settings)
            self.send_html(html_out)
            return

        elif path.startswith("/clanky/"):
            slug = path[8:].strip("/")
            conn = database.get_connection()
            c = conn.cursor()
            c.execute("SELECT * FROM articles WHERE slug = ?", (slug,))
            art = c.fetchone()
            conn.close()

            if not art:
                self.send_html(templates.render_layout("Článek nenalezen", "<div class='container' style='padding:5rem 0;'><h2>Článek nebyl nalezen.</h2><p><a href='/clanky'>← Zpět na články</a></p></div>", settings=settings), status=404)
                return

            content = templates.render_article_detail(dict(art))
            html_out = templates.render_layout(art["title"], content, current_path="/clanky", user=user, settings=settings)
            self.send_html(html_out)
            return

        elif path == "/galerie":
            conn = database.get_connection()
            c = conn.cursor()
            c.execute("SELECT * FROM gallery ORDER BY created_at DESC")
            items = [dict(r) for r in c.fetchall()]
            conn.close()

            content = templates.render_gallery_page(items)
            html_out = templates.render_layout("Fotogalerie", content, current_path="/galerie", user=user, settings=settings)
            self.send_html(html_out)
            return

        elif path == "/kontakt":
            content = templates.render_contact_page(settings)
            html_out = templates.render_layout("Kontakt & O autorech", content, current_path="/kontakt", user=user, settings=settings)
            self.send_html(html_out)
            return

        # ================= ADMIN ROUTES =================
        elif path == "/admin/login":
            if user:
                self.send_redirect("/admin")
                return
            self.send_html(templates.render_admin_login())
            return

        elif path == "/admin/logout":
            token = self.get_cookie("session_token")
            if token:
                database.delete_session(token)
            cookie_clear = "session_token=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT"
            self.send_redirect("/admin/login", set_cookies=[cookie_clear])
            return

        # Protected admin area
        if path.startswith("/admin"):
            if not user:
                self.send_redirect("/admin/login")
                return

            msg = query.get("msg", [None])[0]
            err = query.get("err", [None])[0]

            if path in ["/admin", "/admin/dashboard"]:
                conn = database.get_connection()
                c = conn.cursor()
                c.execute("SELECT COUNT(*) as c FROM articles")
                art_count = c.fetchone()["c"]
                c.execute("SELECT COUNT(*) as c FROM gallery")
                photo_count = c.fetchone()["c"]
                c.execute("SELECT COUNT(*) as c FROM users")
                users_count = c.fetchone()["c"]

                c.execute("SELECT * FROM articles ORDER BY created_at DESC LIMIT 5")
                recent_articles = [dict(r) for r in c.fetchall()]
                conn.close()

                stats = {
                    "articles_count": art_count,
                    "photos_count": photo_count,
                    "users_count": users_count
                }
                content = templates.render_admin_dashboard(stats, recent_articles, [])
                html_out = templates.render_admin_shell("Přehled", content, current_tab="dashboard", user=user, message=msg, error=err)
                self.send_html(html_out)
                return

            elif path == "/admin/articles":
                conn = database.get_connection()
                c = conn.cursor()
                c.execute("""
                    SELECT a.*, u.display_name as author_name 
                    FROM articles a
                    LEFT JOIN users u ON a.author_id = u.id
                    ORDER BY a.created_at DESC
                """)
                articles = [dict(r) for r in c.fetchall()]
                conn.close()

                content = templates.render_admin_articles_list(articles)
                html_out = templates.render_admin_shell("Články", content, current_tab="articles", user=user, message=msg, error=err)
                self.send_html(html_out)
                return

            elif path == "/admin/articles/new":
                content = templates.render_admin_article_form()
                html_out = templates.render_admin_shell("Nový článek", content, current_tab="articles", user=user, message=msg, error=err)
                self.send_html(html_out)
                return

            elif path == "/admin/articles/edit":
                art_id = query.get("id", [None])[0]
                if not art_id:
                    self.send_redirect("/admin/articles")
                    return
                conn = database.get_connection()
                c = conn.cursor()
                c.execute("SELECT * FROM articles WHERE id = ?", (art_id,))
                art = c.fetchone()
                conn.close()
                if not art:
                    self.send_redirect("/admin/articles?err=Clanek+nenalezen")
                    return
                content = templates.render_admin_article_form(dict(art))
                html_out = templates.render_admin_shell("Upravit článek", content, current_tab="articles", user=user, message=msg, error=err)
                self.send_html(html_out)
                return

            elif path == "/admin/articles/delete":
                art_id = query.get("id", [None])[0]
                if art_id:
                    conn = database.get_connection()
                    c = conn.cursor()
                    c.execute("DELETE FROM articles WHERE id = ?", (art_id,))
                    conn.commit()
                    conn.close()
                self.send_redirect("/admin/articles?msg=Clanek+byl+smazan")
                return

            elif path == "/admin/gallery":
                conn = database.get_connection()
                c = conn.cursor()
                c.execute("SELECT * FROM gallery ORDER BY created_at DESC")
                items = [dict(r) for r in c.fetchall()]
                conn.close()

                content = templates.render_admin_gallery(items)
                html_out = templates.render_admin_shell("Galerie", content, current_tab="gallery", user=user, message=msg, error=err)
                self.send_html(html_out)
                return

            elif path == "/admin/gallery/delete":
                photo_id = query.get("id", [None])[0]
                if photo_id:
                    conn = database.get_connection()
                    c = conn.cursor()
                    c.execute("DELETE FROM gallery WHERE id = ?", (photo_id,))
                    conn.commit()
                    conn.close()
                self.send_redirect("/admin/gallery?msg=Fotografie+byla+smazana")
                return

            elif path == "/admin/users":
                conn = database.get_connection()
                c = conn.cursor()
                c.execute("SELECT id, username, display_name, role, created_at FROM users ORDER BY id ASC")
                users = [dict(r) for r in c.fetchall()]
                conn.close()

                content = templates.render_admin_users(users)
                html_out = templates.render_admin_shell("Správci", content, current_tab="users", user=user, message=msg, error=err)
                self.send_html(html_out)
                return

            elif path == "/admin/users/delete":
                user_id = query.get("id", [None])[0]
                if user_id:
                    conn = database.get_connection()
                    c = conn.cursor()
                    # Cannot delete user id 1 or main admin
                    c.execute("SELECT username FROM users WHERE id = ?", (user_id,))
                    target = c.fetchone()
                    if target and target["username"] != "admin":
                        c.execute("DELETE FROM users WHERE id = ?", (user_id,))
                        conn.commit()
                    conn.close()
                self.send_redirect("/admin/users?msg=Uzivatel+byl+odebran")
                return

            elif path == "/admin/settings":
                content = templates.render_admin_settings(settings)
                html_out = templates.render_admin_shell("Nastavení webu", content, current_tab="settings", user=user, message=msg, error=err)
                self.send_html(html_out)
                return

            elif path == "/admin/account":
                content = templates.render_admin_account()
                html_out = templates.render_admin_shell("Změna hesla", content, current_tab="account", user=user, message=msg, error=err)
                self.send_html(html_out)
                return

        # 404
        self.send_html(templates.render_layout("Stránka nenalezena", "<div class='container' style='padding:5rem 0;'><h2>404 - Stránka nenalezena</h2><p><a href='/'>← Zpět na úvod</a></p></div>", settings=settings), status=404)

    def do_POST(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query = urllib.parse.parse_qs(parsed_url.query)

        data, files = self.parse_form_data()
        user = self.get_current_user()

        # Login
        if path == "/admin/login":
            username = data.get("username", "").strip()
            password = data.get("password", "").strip()

            conn = database.get_connection()
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE username = ?", (username,))
            user_row = c.fetchone()
            conn.close()

            if user_row and database.verify_password(password, user_row["password_hash"], user_row["salt"]):
                token = database.create_session(user_row["id"])
                cookie_set = f"session_token={token}; Path=/; HttpOnly; SameSite=Lax; Max-Age={14 * 86400}"
                self.send_redirect("/admin", set_cookies=[cookie_set])
                return
            else:
                self.send_html(templates.render_admin_login(error="Neplatné uživatelské jméno nebo heslo."))
                return

        # All other POST routes require login
        if not user:
            self.send_redirect("/admin/login")
            return

        # Create new article
        if path == "/admin/articles/new":
            title = data.get("title", "").strip()
            subtitle = data.get("subtitle", "").strip()
            slug = data.get("slug", "").strip() or slugify(title)
            summary = data.get("summary", "").strip()
            content = data.get("content", "").strip()
            tags = data.get("tags", "").strip()
            is_published = 1 if data.get("is_published") else 0
            cover_image = data.get("cover_image", "").strip()

            # Handle file upload if provided
            if "cover_file" in files and files["cover_file"].filename:
                file_item = files["cover_file"]
                ext = os.path.splitext(file_item.filename)[1].lower()
                filename = f"cover_{int(datetime.now().timestamp())}_{secrets.token_hex(4)}{ext}"
                target_path = os.path.join(UPLOADS_DIR, filename)
                with open(target_path, "wb") as f:
                    f.write(file_item.file.read())
                cover_image = f"/uploads/{filename}"

            conn = database.get_connection()
            c = conn.cursor()
            # Ensure unique slug
            c.execute("SELECT id FROM articles WHERE slug = ?", (slug,))
            if c.fetchone():
                slug = f"{slug}-{int(datetime.now().timestamp()) % 1000}"

            c.execute("""
                INSERT INTO articles (title, slug, subtitle, cover_image, summary, content, tags, is_published, author_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (title, slug, subtitle, cover_image, summary, content, tags, is_published, user["id"]))
            conn.commit()
            conn.close()

            self.send_redirect("/admin/articles?msg=Clanek+byl+uspesne+vytvoren")
            return

        # Edit article
        elif path == "/admin/articles/edit":
            art_id = query.get("id", [None])[0]
            if not art_id:
                self.send_redirect("/admin/articles")
                return

            title = data.get("title", "").strip()
            subtitle = data.get("subtitle", "").strip()
            slug = data.get("slug", "").strip() or slugify(title)
            summary = data.get("summary", "").strip()
            content = data.get("content", "").strip()
            tags = data.get("tags", "").strip()
            is_published = 1 if data.get("is_published") else 0
            cover_image = data.get("cover_image", "").strip()

            if "cover_file" in files and files["cover_file"].filename:
                file_item = files["cover_file"]
                ext = os.path.splitext(file_item.filename)[1].lower()
                filename = f"cover_{int(datetime.now().timestamp())}_{secrets.token_hex(4)}{ext}"
                target_path = os.path.join(UPLOADS_DIR, filename)
                with open(target_path, "wb") as f:
                    f.write(file_item.file.read())
                cover_image = f"/uploads/{filename}"

            conn = database.get_connection()
            c = conn.cursor()
            c.execute("""
                UPDATE articles 
                SET title = ?, slug = ?, subtitle = ?, cover_image = ?, summary = ?, content = ?, tags = ?, is_published = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (title, slug, subtitle, cover_image, summary, content, tags, is_published, art_id))
            conn.commit()
            conn.close()

            self.send_redirect("/admin/articles?msg=Zmeny+v+clanku+byly+ulozeny")
            return

        # Upload gallery photo
        elif path == "/admin/gallery/upload":
            title = data.get("title", "").strip() or "Fotografie"
            category = data.get("category", "").strip() or "Obecné"
            description = data.get("description", "").strip()

            image_url = ""
            if "photo_file" in files and files["photo_file"].filename:
                file_item = files["photo_file"]
                ext = os.path.splitext(file_item.filename)[1].lower()
                if ext not in [".jpg", ".jpeg", ".png", ".webp", ".gif"]:
                    ext = ".jpg"
                filename = f"photo_{int(datetime.now().timestamp())}_{secrets.token_hex(4)}{ext}"
                target_path = os.path.join(UPLOADS_DIR, filename)
                with open(target_path, "wb") as f:
                    f.write(file_item.file.read())
                image_url = f"/uploads/{filename}"

            if image_url:
                conn = database.get_connection()
                c = conn.cursor()
                c.execute("""
                    INSERT INTO gallery (title, description, image_url, category, uploaded_by)
                    VALUES (?, ?, ?, ?, ?)
                """, (title, description, image_url, category, user["id"]))
                conn.commit()
                conn.close()
                self.send_redirect("/admin/gallery?msg=Fotografie+byla+uspesne+nahrana")
            else:
                self.send_redirect("/admin/gallery?err=Nebyl+vybran+zadny+soubor")
            return

        # Create new admin user
        elif path == "/admin/users/new":
            new_username = data.get("username", "").strip().lower()
            display_name = data.get("display_name", "").strip()
            new_password = data.get("password", "").strip()
            role = data.get("role", "editor")

            if not new_username or not new_password or not display_name:
                self.send_redirect("/admin/users?err=Vyplnte+vsechna+pole")
                return

            conn = database.get_connection()
            c = conn.cursor()
            c.execute("SELECT id FROM users WHERE username = ?", (new_username,))
            if c.fetchone():
                conn.close()
                self.send_redirect("/admin/users?err=Uzivatelske+jmeno+jiz+existuje")
                return

            h, s = database.hash_password(new_password)
            c.execute("""
                INSERT INTO users (username, password_hash, salt, display_name, role)
                VALUES (?, ?, ?, ?, ?)
            """, (new_username, h, s, display_name, role))
            conn.commit()
            conn.close()

            self.send_redirect(f"/admin/users?msg=Spravce+{new_username}+byl+uspesne+vytvoren")
            return

        # Update settings
        elif path == "/admin/settings":
            updates = {
                "site_title": data.get("site_title", "").strip(),
                "site_subtitle": data.get("site_subtitle", "").strip(),
                "site_description": data.get("site_description", "").strip(),
                "author_bio": data.get("author_bio", "").strip(),
                "contact_email": data.get("contact_email", "").strip(),
            }
            database.update_settings(updates)
            self.send_redirect("/admin/settings?msg=Nastaveni+bylo+aktualizovano")
            return

        # Change own password
        elif path == "/admin/account":
            cur_pwd = data.get("current_password", "")
            new_pwd = data.get("new_password", "")
            cnf_pwd = data.get("confirm_password", "")

            conn = database.get_connection()
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE id = ?", (user["id"],))
            user_row = c.fetchone()

            if not database.verify_password(cur_pwd, user_row["password_hash"], user_row["salt"]):
                conn.close()
                self.send_redirect("/admin/account?err=Soucasne+heslo+neni+spravne")
                return

            if new_pwd != cnf_pwd or len(new_pwd) < 6:
                conn.close()
                self.send_redirect("/admin/account?err=Nova+hesla+se+neshoduji+nebo+jsou+kratsi+nez+6+znaku")
                return

            h, s = database.hash_password(new_pwd)
            c.execute("UPDATE users SET password_hash = ?, salt = ? WHERE id = ?", (h, s, user["id"]))
            conn.commit()
            conn.close()

            self.send_redirect("/admin/account?msg=Heslo+bylo+uspesne+zmeneno")
            return

        self.send_redirect("/admin")

def run_server():
    database.init_db()
    server_address = ("0.0.0.0", PORT)
    httpd = http.server.ThreadingHTTPServer(server_address, CMSRequestHandler)
    print("=" * 60)
    print("   PUD A POHODLÍ — Redakční systém & Web spuštěn")
    print(f"   Adresa webu: http://localhost:{PORT}")
    print(f"   Administrace: http://localhost:{PORT}/admin")
    print("   Výchozí přihlášení: admin / admin123")
    print("=" * 60)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nZastavuji server...")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
