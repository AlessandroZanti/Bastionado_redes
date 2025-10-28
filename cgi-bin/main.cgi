#!/usr/bin/env python3
# /usr/local/JSBach/cgi-bin/main.cgi
# Interfaz CGI con menú WAN y Enrutar — versión moderna con menú lateral y UI dinámica

import os, sys, html, socket, urllib.parse, re, subprocess

HOST = "127.0.0.1"
PORT = 1234
SO_TIMEOUT = 4  # segundos

CLIENT_PATH = "/usr/local/JSBach/scripts/client_srv_cli"

def recv_all(s, timeout=SO_TIMEOUT):
    s.settimeout(timeout)
    data = bytearray()
    try:
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            data.extend(chunk)
    except Exception:
        pass
    return data.decode(errors="replace")

def send_to_srv_cli(cmd):
    """
    Ejecuta el script cliente y devuelve la salida (stdout+stderr).
    Timeout para evitar bloqueo.
    """
    try:
        args = [CLIENT_PATH] + cmd.split()
        proc = subprocess.run(args, capture_output=True, text=True, timeout=6)
        out = proc.stdout
        if proc.stderr:
            out += ("\n[stderr]\n" + proc.stderr)
        return out
    except subprocess.TimeoutExpired:
        return "ERROR: tiempo de espera agotado al conectar con srv_cli"
    except FileNotFoundError:
        return "ERROR: cliente no encontrado"
    except Exception as e:
        return f"ERROR ejecutando cliente: {e}"

# Leer parámetros
method = os.environ.get("REQUEST_METHOD", "GET").upper()
qs = ""
if method == "GET":
    qs = os.environ.get("QUERY_STRING", "")
else:
    try:
        length = int(os.environ.get("CONTENT_LENGTH", "0"))
    except:
        length = 0
    qs = sys.stdin.read(length) if length > 0 else ""

params = urllib.parse.parse_qs(qs, keep_blank_values=True)

menu = (params.get("menu", ["wan"])[0] or "wan").lower()
action = (params.get("action", [""])[0] or "").strip()
mode = (params.get("mode", ["dhcp"])[0] or "dhcp").strip().lower()
iface = (params.get("iface", [""])[0] or "").strip()

# Validaciones
if iface and not re.fullmatch(r"[A-Za-z0-9._-]{1,32}", iface):
    iface = ""
if mode not in ("dhcp", "manual"):
    mode = "dhcp"

# Mapeo acciones
cmd_to_send = None
if menu == "wan":
    if action == "parar":
        cmd_to_send = "ifwan parar"
    elif action == "iniciar":
        cmd_to_send = "ifwan iniciar"
    elif action == "configurar" and iface:
        cmd_to_send = f"ifwan configurar {mode} {iface}"

# HTML output
print("Content-Type: text/html; charset=utf-8\n")
print(f"""<!doctype html>
<html>
<head>
<meta charset='utf-8'>
<title>JSBach Network Control</title>
<style>
body {{
    margin: 0;
    font-family: Arial, sans-serif;
    background: #111;
    color: #eee;
}}
.menu-btn {{
    position: fixed;
    top: 12px;
    left: 14px;
    font-size: 28px;
    cursor: pointer;
    color: #00bfff;
    z-index: 3;
}}
.sidebar {{
    position: fixed;
    left: -220px;
    top: 0;
    width: 220px;
    height: 100%;
    background: #1b1b1b;
    transition: 0.3s;
    padding-top: 60px;
    box-shadow: 2px 0 6px rgba(0,0,0,0.5);
}}
.sidebar.show {{ left: 0; }}
.sidebar a {{
    display: block;
    color: #ccc;
    padding: 14px 18px;
    text-decoration: none;
}}
.sidebar a:hover, .sidebar a.active {{
    background: #00bfff;
    color: white;
}}
.main {{
    padding: 60px 20px;
    transition: 0.3s;
    margin-left: 10px;
}}
.section {{
    display: none;
}}
.section.active {{
    display: block;
}}
.panel {{
    background: #222;
    padding: 16px;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.4);
}}
h1 {{
    margin-top: 0;
}}
.row {{
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 12px;
}}
button {{
    background: #333;
    border: none;
    padding: 10px 14px;
    border-radius: 8px;
    color: #eee;
    cursor: pointer;
    transition: 0.3s;
}}
button:hover {{
    background: #00bfff;
    color: white;
}}
button.active {{
    background: #00bfff;
    color: white;
}}
select, input {{
    background: #1a1a1a;
    color: #eee;
    border: 1px solid #555;
    padding: 8px;
    border-radius: 6px;
}}
.config-opciones {{
    display: none;
    margin-top: 10px;
}}
.sep {{
    height: 1px;
    background: #333;
    margin: 18px 0;
}}
pre {{
    background: #000;
    color: #00ff99;
    padding: 10px;
    border-radius: 6px;
    white-space: pre-wrap;
}}
.footer {{
    color: #777;
    font-size: 0.9em;
    margin-top: 16px;
    text-align: center;
}}
</style>

<script>
function toggleMenu() {{
    document.querySelector('.sidebar').classList.toggle('show');
}}

function mostrarSeccion(id) {{
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.getElementById(id).classList.add('active');
    document.querySelectorAll('.sidebar a').forEach(a => a.classList.remove('active'));
    document.querySelector(`.sidebar a[data-id="${{id}}"]`).classList.add('active');
    document.querySelector('.sidebar').classList.remove('show');
}}

function activarBoton(btn, tipo) {{
    document.querySelectorAll('#wanButtons button').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const cfg = document.querySelector('.config-opciones');
    if (tipo === 'configurar') {{
        cfg.style.display = 'block';
    }} else {{
        cfg.style.display = 'none';
    }}
}}
</script>
</head>

<body>
<div class="menu-btn" onclick="toggleMenu()">☰</div>

<div class="sidebar">
    <a href="#" data-id="wan" class="{'active' if menu=='wan' else ''}" onclick="mostrarSeccion('wan')">Menú WAN</a>
    <a href="#" data-id="enrutar" class="{'active' if menu=='enrutar' else ''}" onclick="mostrarSeccion('enrutar')">Menú Enrutar</a>
</div>

<div class="main">

  <div id="wan" class="section {'active' if menu=='wan' else ''}">
    <div class="panel">
      <h1>Gestión WAN</h1>
      <form method="post" action="/cgi-bin/main.cgi">
        <input type="hidden" name="menu" value="wan">

        <div id="wanButtons" class="row">
          <button type="submit" name="action" value="iniciar" onclick="activarBoton(this, 'iniciar')">Enable</button>
          <button type="button" onclick="activarBoton(this, 'configurar')">Configurar</button>
          <button type="submit" name="action" value="parar" onclick="activarBoton(this, 'parar')">Parar</button>
        </div>

        <div class="config-opciones">
          <label>Modo:</label>
          <select name="mode">
            <option value="dhcp" {"selected" if mode=="dhcp" else ""}>DHCP</option>
            <option value="manual" {"selected" if mode=="manual" else ""}>Manual</option>
          </select>
          &nbsp;
          <label>Interfaz:</label>
          <input name="iface" value="{html.escape(iface)}" placeholder="eth0, wlan0, etc." maxlength="32">
          &nbsp;
          <button type="submit" name="action" value="configurar">OK</button>
        </div>
      </form>
    </div>

    {"<div class='sep'></div><div class='panel'><h3>Comando enviado</h3><pre>" + html.escape(cmd_to_send or '') + "</pre><h4>Salida del servicio:</h4><pre>" + html.escape(send_to_srv_cli(cmd_to_send)) + "</pre></div>" if action else ""}
  </div>

  <div id="enrutar" class="section {'active' if menu=='enrutar' else ''}">
    <div class="panel">
      <h1>Menú Enrutar</h1>
      <button>Botón</button>
    </div>
  </div>

  <div class="footer">
    JSBach Web Control • CGI seguro (localhost 127.0.0.1)
  </div>

</div>
</body>
</html>
""")

