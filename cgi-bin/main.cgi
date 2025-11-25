#!/usr/bin/env python3
import sys, os, re, html
sys.path.append("/usr/local/JSBach/cgi-bin")

from logic import get_params, send_to_srv_cli, parse_interfaces
import wan, enrutar, bridge

# --------------------------
# Params
# --------------------------
params = get_params()
menu   = params.get("menu", "wan")
action = params.get("action", "")

# Lista de interfaces WAN
interfaces = parse_interfaces(send_to_srv_cli("interfaces listar"))

# --------------------------
# Routing de secciones
# --------------------------
if menu == "wan":
    content = wan.render(params, interfaces)
elif menu == "enrutar":
    content = enrutar.render(params)
elif menu == "bridge":
    content = bridge.render(params)
else:
    content = "<h2>Error: menú desconocido</h2>"

# --------------------------
# HTML completo
# --------------------------
print("Content-Type: text/html; charset=utf-8\n")
print(f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Network Control</title>

<style>
/* Layout general */
body {{
    margin: 0;
    font-family: Arial, sans-serif;
    background: #0f1113;
    color: #e6eef0;
}}

/* Botón hamburguesa */
.menu-btn {{
    position: fixed;
    top: 12px;
    left: 14px;
    font-size: 28px;
    cursor: pointer;
    color: #00bfff;
    z-index: 999;
    user-select: none;
}}

/* Sidebar */
.sidebar {{
    position: fixed;
    left: -240px;
    top: 0;
    width: 220px;
    height: 100%;
    background: #131416;
    transition: left 0.28s ease;
    padding-top: 64px;
    box-shadow: 2px 0 8px rgba(0,0,0,0.6);
    z-index: 900;
}}
.sidebar.show {{ left: 0; }}

/* Links del sidebar */
.sidebar a {{
    display: block;
    color: #cfd8da;
    padding: 14px 18px;
    text-decoration: none;
    border-radius: 8px;
    margin: 6px 10px;
    transition: background 0.18s, color 0.18s;
}}
.sidebar a:hover {{ background: #00bfff; color: #001219; }}
.sidebar a.active {{ background: #00bfff; color: #001219; }}

/* Contenido principal */
.main {{
    padding: 60px 20px;
    transition: margin-left 0.28s;
    margin-left: 20px;
}}

/* Al abrir sidebar */
.sidebar.show ~ .main {{
    margin-left: 240px;
}}

/* Paneles */
.panel {{
    background: #171819;
    padding: 16px;
    border-radius: 12px;
    box-shadow: 0 6px 14px rgba(0,0,0,0.45);
}}

/* Botones */
button {{
    background: linear-gradient(#222, #1a1a1a);
    border: 1px solid rgba(255,255,255,0.06);
    padding: 10px 14px;
    border-radius: 10px;
    color: #e6eef0;
    cursor: pointer;
    transition: background 0.18s, transform 0.06s, box-shadow 0.12s;
    box-shadow: 0 2px 6px rgba(0,0,0,0.4);
}}
button:hover {{
    background: #00bfff;
    color: #001219;
    transform: translateY(-1px);
}}
button:active {{ transform: translateY(0); }}
button:focus {{ outline: none; box-shadow: 0 0 0 3px rgba(0,191,255,0.12); }}

/* Inputs y selects */
select, input {{
    background: #0f1112;
    color: #e6eef0;
    border: 1px solid #2a2a2a;
    padding: 8px;
    border-radius: 8px;
}}

/* Separadores y pre */
.sep {{ height: 1px; background: #202427; margin: 18px 0; border-radius:4px; }}
pre {{
    background: #020403;
    color: #8fffb3;
    padding: 12px;
    border-radius: 8px;
    white-space: pre-wrap;
    overflow-x: auto;
}}
</style>

<script>
function toggleMenu() {{
    document.querySelector('.sidebar').classList.toggle('show');
}}

document.addEventListener('click', function(e){{
    const sidebar = document.querySelector('.sidebar');
    if (!sidebar) return;
    if (e.target.closest('.sidebar a')) {{
        sidebar.classList.remove('show');
    }}
}});
</script>

</head>

<body>

<div class="menu-btn" onclick="toggleMenu()">☰</div>

<div class="sidebar">
  <a href="?menu=wan" class="{{ 'active' if menu=='wan' else '' }}">WAN</a>
  <a href="?menu=enrutar" class="{{ 'active' if menu=='enrutar' else '' }}">Routing</a>
  <a href="?menu=bridge" class="{{ 'active' if menu=='bridge' else '' }}">Bridge</a>
</div>

<div class="main">
{content}
</div>

</body>
</html>
""")
