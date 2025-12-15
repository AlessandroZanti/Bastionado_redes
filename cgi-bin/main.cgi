#!/usr/bin/env python3
import sys, os, re, html
sys.path.append("/usr/local/JSBach/cgi-bin")

from logic import get_params, send_to_srv_cli, parse_interfaces
import wan, enrutar, bridge, cortafuegos

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
elif menu == "cortafuegos":
    content = cortafuegos.render(params)
else:
    content = "<h2>Error: menú desconocido</h2>"

# --------------------------
# HTML completo con estilo modernizado
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
    background: #030617;
    color: #e8eef2;
}}

/* Smooth fade-in */
body {{ opacity: 0; animation: fadeIn 0.4s ease-out forwards; }}
@keyframes fadeIn {{ from {{ opacity:0 }} to {{ opacity:1 }} }}

/* Botón hamburguesa */
.menu-btn {{
    position: fixed;
    top: 16px;
    left: 18px;
    font-size: 30px;
    cursor: pointer;
    color: #4dc0ff;
    z-index: 999;
    user-select: none;
    transition: transform 0.15s;
}}
.menu-btn:hover {{ transform: scale(1.06); }}

/* Sidebar */
.sidebar {{
    position: fixed;
    left: -250px;
    top: 0;
    width: 240px;
    height: 100%;
    background: #02040b;
    backdrop-filter: blur(6px);
    transition: left 0.28s ease;
    padding-top: 70px;
    box-shadow: 3px 0 10px rgba(0,0,0,0.55);
    z-index: 900;
}}
.sidebar.show {{ left: 0; }}

/* Links del sidebar */
.sidebar a {{
    display: block;
    color: #cdd6da;
    padding: 14px 20px;
    text-decoration: none;
    border-radius: 10px;
    margin: 6px 12px;
    font-weight: 500;
    background: rgba(255,255,255,0.02);
    transition: background 0.18s, color 0.18s, transform 0.12s;
}}
.sidebar a:hover {{ background: #030617; color: #2030ff; transform: translateX(4px); }}
.sidebar a.active {{ background: #030617; color: #2030ff; }}

/* Contenido */
.main {{
    padding: 70px 26px;
    transition: margin-left 0.28s;
    margin-left: 20px;
}}
.sidebar.show ~ .main {{ margin-left: 260px; }}

/* Paneles */
.panel {{
    background: linear-gradient(135deg, #02040b, #02040b);
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0 8px 18px rgba(0,0,0,0.5);
    border: 1px solid rgba(255,255,255,0.04);
}}

/* Botones */
button {{
    background: linear-gradient(135deg, #1c1d21, #17181b);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 11px 16px;
    border-radius: 8px;
    color: #e6eef0;
    cursor: pointer;
    font-weight: 500;
    transition: background 0.18s, transform 0.1s, box-shadow 0.12s;
    box-shadow: 0 3px 8px rgba(0,0,0,0.45);
}}
button:hover {{
    background: #030617;
    color: #2030ff;
    transform: translateY(-2px);
}}
button:active {{ transform: translateY(0); }}
button:focus {{ outline: none; box-shadow: 0 0 0 3px rgba(77,192,255,0.25); }}

/* Inputs y selects */
select, input {{
    background: #02040b;
    color: #e6eef0;
    border: 1px solid #26282b;
    padding: 10px;
    border-radius: 10px;
    transition: border 0.15s;
}}
select:focus, input:focus {{ border-color: #4dc0ff; }}

/* Separadores y pre */
.sep {{ height: 1px; background: #23272a; margin: 22px 0; border-radius:4px; }}
pre {{
    background: #000000;
    color: #00ff00;
    padding: 14px;
    border-radius: 10px;
    white-space: pre-wrap;
    overflow-x: auto;
    border: 1px solid rgba(255,255,255,0.06);
}}
</style>

<script>
function toggleMenu() {{
    document.querySelector('.sidebar').classList.toggle('show');
}}

document.addEventListener('click', function(e){{
    const sidebar = document.querySelector('.sidebar');
    if (!sidebar) return;
    if (e.target.closest('.sidebar a')) {{ sidebar.classList.remove('show'); }}
}});
</script>

</head>

<body>

<div class="menu-btn" onclick="toggleMenu()">☰</div>

<div class="sidebar">
    <a href="?menu=wan" class="{{ 'active' if menu=='wan' else '' }}">WAN</a>
    <a href="?menu=enrutar" class="{{ 'active' if menu=='enrutar' else '' }}">Routing</a>
    <a href="?menu=bridge" class="{{ 'active' if menu=='bridge' else '' }}">Bridge</a>
    <a href="?menu=cortafuegos" class="{{ 'active' if menu=='cortafuegos' else '' }}">Cortafuegos</a>
</div>

<div class="main">
{content}
</div>

</body>
</html>
""")
