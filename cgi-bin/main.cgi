#!/usr/bin/env python3
# /usr/local/JSBach/cgi-bin/main.cgi
# Interfaz CGI moderna con menú lateral, CLI visible y ejecución funcional
# Muestra la salida del cliente, el comando ejecutado y refresca tras 5s

import os, sys, html, urllib.parse, re, subprocess

CLIENT_PATH = "/usr/local/JSBach/scripts/client_srv_cli"

def send_to_srv_cli(cmd):
    """Ejecuta el script cliente y devuelve stdout+stderr."""
    try:
        args = [CLIENT_PATH] + cmd.split()
        proc = subprocess.run(args, capture_output=True, text=True, timeout=6)
        out = proc.stdout
        if proc.stderr:
            out += ("\n[stderr]\n" + proc.stderr)
        return out.strip()
    except subprocess.TimeoutExpired:
        return "ERROR: tiempo de espera agotado al conectar con srv_cli"
    except FileNotFoundError:
        return "ERROR: cliente no encontrado"
    except Exception as e:
        return f"ERROR ejecutando cliente: {e}"

# Leer parámetros CGI
method = os.environ.get("REQUEST_METHOD", "GET").upper()
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

if iface and not re.fullmatch(r"[A-Za-z0-9._-]{1,32}", iface):
    iface = ""
if mode not in ("dhcp", "manual"):
    mode = "dhcp"

# 🔹 Ejecutar interfaces listar al inicio (para precargar)
interfaces_raw = send_to_srv_cli("interfaces listar")
interfaces_list = []
for line in interfaces_raw.splitlines():
    m = re.match(r'^\s*\d+\s*-\s*([A-Za-z0-9._-]+)', line)
    if m:
        interfaces_list.append(m.group(1))
if not interfaces_list:
    for token in re.findall(r'\b([A-Za-z0-9._-]{2,15})\b', interfaces_raw):
        if token.lower() not in ("listado", "interfaces", "de", "red", "salida"):
            interfaces_list.append(token)
    seen = set()
    interfaces_list = [x for x in interfaces_list if not (x in seen or seen.add(x))]

# 🔹 Mapear acciones a comandos
cmd_to_send = None
if menu == "wan":
    if action == "parar":
        cmd_to_send = "ifwan parar"
    elif action == "iniciar":
        cmd_to_send = "ifwan iniciar"
    elif action == "configurar" and iface:
        cmd_to_send = f"ifwan configurar {mode} {iface}"
elif menu == "enrutar":
    if action == "iniciar":
        cmd_to_send = "enrutar iniciar"
    elif action == "parar":
        cmd_to_send = "enrutar parar"
    elif action == "estado":
        cmd_to_send = "enrutar estado"

# 🔹 Ejecutar comando (si hay)
cli_output = send_to_srv_cli(cmd_to_send) if cmd_to_send else ""
show_config_block = (menu == "wan" and action == "configurar")

# -----------------------------------------------------
#                   HTML
# -----------------------------------------------------
print("Content-Type: text/html; charset=utf-8\n")
print(f"""<!doctype html>
<html>
<head>
<meta charset='utf-8'>
<title>Network Control</title>
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
.section {{ display: none; }}
.section.active {{ display: block; }}
.panel {{
    background: #222;
    padding: 16px;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.4);
}}
h1 {{ margin-top: 0; }}
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
button:hover {{ background: #00bfff; color: white; }}
button.active {{ background: #00bfff; color: white; }}
select, input {{
    background: #1a1a1a;
    color: #eee;
    border: 1px solid #555;
    padding: 8px;
    border-radius: 6px;
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

// 🔹 Esperar 5 segundos antes de recargar tras ejecutar acción
if (window.performance && performance.navigation.type === 1) {{
    setTimeout(() => location.reload(), 5000);
}}
</script>
</head>

<body>
<div class="menu-btn" onclick="toggleMenu()">☰</div>

<div class="sidebar">
    <a href="#" data-id="wan" class="{ 'active' if menu=='wan' else '' }" onclick="mostrarSeccion('wan')">WAN</a>
    <a href="#" data-id="enrutar" class="{ 'active' if menu=='enrutar' else '' }" onclick="mostrarSeccion('enrutar')">Routing</a>
</div>

<div class="main">

  <!-- ==================== WAN ==================== -->
  <div id="wan" class="section { 'active' if menu=='wan' else '' }">
    <div class="panel">
      <h1>WAN</h1>
      <form method="post" action="/cgi-bin/main.cgi">
        <input type="hidden" name="menu" value="wan">
        <div class="row">
          <button type="submit" name="action" value="iniciar">Enable</button>
          <button type="submit" name="action" value="configurar">Configure</button>
          <button type="submit" name="action" value="parar">Stop</button>
        </div>
      </form>

      {"<div class='sep'></div><form method='post' action='/cgi-bin/main.cgi'><input type='hidden' name='menu' value='wan'><input type='hidden' name='action' value='configurar'><label>Mode:</label> <select name='mode'><option value='dhcp'>DHCP</option><option value='manual'>Manual</option></select> <label>Interface:</label> <select name='iface'>" + ''.join(f"<option value='{i}'>{i}</option>" for i in interfaces_list) + "</select> <button type='submit'>Apply</button></form>" if show_config_block else ""}
    </div>

    {"<div class='sep'></div><div class='panel'><h3>Script</h3><pre>" + html.escape(cmd_to_send or '') + "</pre><h4>CLI</h4><pre>" + html.escape(cli_output) + "</pre></div>" if action else ""}
  </div>

  <!-- ==================== ROUTING ==================== -->
  <div id="enrutar" class="section { 'active' if menu=='enrutar' else '' }">
    <div class="panel">
      <h1>Routing</h1>
      <form method="post" action="/cgi-bin/main.cgi">
        <input type="hidden" name="menu" value="enrutar">
        <div class="row">
          <button type="submit" name="action" value="iniciar">On</button>
          <button type="submit" name="action" value="parar">Off</button>
          <button type="submit" name="action" value="estado">Status</button>
        </div>
      </form>
      {"<div class='sep'></div><div class='panel'><h3>Script</h3><pre>" + html.escape(cmd_to_send or '') + "</pre><h4>CLI</h4><pre>" + html.escape(cli_output) + "</pre></div>" if menu=='enrutar' and action else ""}
    </div>
  </div>

  <div class="footer">
    Net Control Web • Secured CGI (localhost 127.0.0.1)
  </div>
</div>
</body>
</html>
""")
