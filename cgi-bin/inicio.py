# inicio.py (versión rápida, con datos simulados)

import random

# ==========================
# Helpers
# ==========================
def bytes_a_mb(b):
    try:
        return f"{int(b) / 1024 / 1024:.1f} MB"
    except:
        return "N/A"

# ==========================
# Tráfico SIMULADO
# ==========================
def leer_trafico_eno1():
    # Retorna valores aleatorios simulados
    rx = random.randint(50*1024*1024, 500*1024*1024)  # 50MB a 500MB
    tx = random.randint(20*1024*1024, 300*1024*1024)  # 20MB a 300MB
    return bytes_a_mb(rx), bytes_a_mb(tx)

def leer_trafico_interfaces():
    rx, tx = leer_trafico_eno1()
    return f"""eno1
  RX: {rx}
  TX: {tx}
"""

# ==========================
# Dispositivos SIMULADOS
# ==========================
def leer_dispositivos():
    # Simulamos 3 a 8 dispositivos conectados
    n = random.randint(3, 8)
    dispositivos = []
    for i in range(n):
        ip = f"192.168.1.{100 + i}"
        estado = "Activo"
        traf = f"{random.randint(1,50)} MB"
        dispositivos.append((ip, estado, traf))
    return dispositivos

# ==========================
# Render
# ==========================
def render(params):

    trafico_rx, trafico_tx = leer_trafico_eno1()
    trafico_interfaces = leer_trafico_interfaces()
    dispositivos_lista = leer_dispositivos()

    dispositivos = len(dispositivos_lista)
    estado = "Operativo"

    return f"""
    <div class="panel">

        <h1 style="margin-top:0; font-size:30px; color:#4dc0ff;">
            Network Control
        </h1>

        <h2 style="margin-bottom:6px;">
            Alessandro Zanti Alcala
        </h2>

        <p style="color:#b7c2c8; max-width:720px;">
            Panel central de administración y monitorización de red.
        </p>

        <div class="sep"></div>

        <!-- PANEL PRINCIPAL DE ESTADO -->
        <div class="panel">
            <h3>📡 Estado General</h3>
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(160px,1fr)); gap:14px;">

                <div>
                    <div style="font-size:13px; color:#7f8b91;">Tráfico RX</div>
                    <div style="font-size:18px; color:#4dc0ff;">{trafico_rx}</div>
                </div>

                <div>
                    <div style="font-size:13px; color:#7f8b91;">Tráfico TX</div>
                    <div style="font-size:18px; color:#4dc0ff;">{trafico_tx}</div>
                </div>

                <div>
                    <div style="font-size:13px; color:#7f8b91;">Dispositivos</div>
                    <div style="font-size:18px;">{dispositivos}</div>
                </div>

                <div>
                    <div style="font-size:13px; color:#7f8b91;">Sistema</div>
                    <div style="font-size:16px; color:#00ff88;">{estado}</div>
                </div>

            </div>
        </div>

        <div class="sep"></div>

        <!-- PANEL GRANDE: TRÁFICO -->
        <div class="panel">
            <h3>📊 Tráfico por Interfaces</h3>
            <pre>
{trafico_interfaces}
            </pre>
        </div>

        <div class="sep"></div>

        <!-- PANEL GRANDE: DISPOSITIVOS -->
        <div class="panel">
            <h3>🖥 Dispositivos Conectados</h3>

            <table style="width:100%; border-collapse:collapse; font-size:14px;">
                <tr style="color:#7fa9c9; text-align:left;">
                    <th>IP</th>
                    <th>Estado</th>
                    <th>Tráfico</th>
                </tr>

                {''.join(f'''
                <tr>
                    <td>{ip}</td>
                    <td>{estado}</td>
                    <td>{traf}</td>
                </tr>
                ''' for ip, estado, traf in dispositivos_lista)}
            </table>
        </div>

        <div class="sep"></div>

        <!-- ACCESOS WAN / Routing / Bridge / Firewall -->
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(220px,1fr)); gap:18px;">

            <div class="panel">
                <h3>🌐 WAN</h3>
                <p style="color:#b7c2c8;">
                    Configuración y estado de las interfaces de salida a red.
                </p>
                <a href="?menu=wan"><button>Administrar WAN</button></a>
            </div>

            <div class="panel">
                <h3>🧭 Routing</h3>
                <p style="color:#b7c2c8;">
                    Gestión de rutas estáticas y políticas de encaminamiento.
                </p>
                <a href="?menu=enrutar"><button>Configurar Routing</button></a>
            </div>

            <div class="panel">
                <h3>🔗 Bridge</h3>
                <p style="color:#b7c2c8;">
                    Unión de interfaces y administración de bridges.
                </p>
                <a href="?menu=bridge"><button>Gestionar Bridge</button></a>
            </div>

            <div class="panel">
                <h3>🔥 Cortafuegos</h3>
                <p style="color:#b7c2c8;">
                    Reglas de filtrado y seguridad del tráfico.
                </p>
                <a href="?menu=cortafuegos"><button>Ajustar Firewall</button></a>
            </div>

        </div>

    </div>
    """
