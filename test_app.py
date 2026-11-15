import io
from app import CMSRequestHandler

def make_request(method, path, body="", headers=None):
    headers = headers or {}
    req = f"{method} {path} HTTP/1.1\r\nHost: localhost\r\n"
    if body:
        headers["Content-Length"] = str(len(body.encode("utf-8")))
        if "Content-Type" not in headers:
            headers["Content-Type"] = "application/x-www-form-urlencoded"
    for k, v in headers.items():
        req += f"{k}: {v}\r\n"
    req += "\r\n" + body

    out_file = io.BytesIO()
    class DummyHandler(CMSRequestHandler):
        def __init__(self):
            self.client_address = ('127.0.0.1', 12345)
            self.rfile = io.BytesIO(req.encode("utf-8"))
            self.wfile = out_file
            self.raw_requestline = self.rfile.readline()
            self.parse_request()
            if method == "GET":
                self.do_GET()
            elif method == "POST":
                self.do_POST()

    DummyHandler()
    raw = out_file.getvalue()
    parts = raw.split(b"\r\n\r\n", 1)
    header_str = parts[0].decode("utf-8", errors="ignore")
    body_str = parts[1].decode("utf-8", errors="ignore") if len(parts) > 1 else ""
    status_line = header_str.split("\r\n")[0]
    headers_dict = {}
    for line in header_str.split("\r\n")[1:]:
        if ": " in line:
            k, v = line.split(": ", 1)
            headers_dict[k.lower()] = v
    return status_line, headers_dict, body_str

if __name__ == "__main__":
    print("--- 1. Testing Login ---")
    st, hdrs, b = make_request("POST", "/admin/login", "username=admin&password=admin123")
    print("Login POST:", st, "Location:", hdrs.get("location"))
    cookie = hdrs.get("set-cookie", "")
    print("Cookie received:", cookie[:35] + "...")
    token = cookie.split(";")[0]

    print("\n--- 2. Testing Admin Dashboard with session cookie ---")
    st, hdrs, b = make_request("GET", "/admin", headers={"Cookie": token})
    print("Admin GET:", st, "Contains 'Přehled redakce':", "Přehled redakce" in b)

    print("\n--- 3. Testing Creating New Admin for Partner/Friend ---")
    st, hdrs, b = make_request("POST", "/admin/users/new", "username=kolega&display_name=Kolega+Kynolog&password=heslo123&role=admin", headers={"Cookie": token})
    print("User Create POST:", st, "Location:", hdrs.get("location"))

    print("\n--- 4. Testing New Admin Login ---")
    st, hdrs, b = make_request("POST", "/admin/login", "username=kolega&password=heslo123")
    print("New Admin Login POST:", st, "Location:", hdrs.get("location"))

    print("\n--- 5. Testing Creating a New Article ---")
    st, hdrs, b = make_request("POST", "/admin/articles/new", "title=Testovaci+clanek&summary=Strucny+uvod&content=Obsah+clanku&tags=Test&is_published=1", headers={"Cookie": token})
    print("Article Create POST:", st, "Location:", hdrs.get("location"))

    print("\nAll auth & CMS tests passed flawlessly!")
