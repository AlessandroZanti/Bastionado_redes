# inicio.py
from logic import send_to_srv_cli

def render(params):

    trafico_rx = "124.6 MB"
    trafico_tx = "98.2 MB"
    dispositivos = 7
    interfaces_activas = 3
    estado = "Operativo"

    dispositivos_lista = [
        ("192.168.1.10", "Laptop", "1.2 GB"),
        ("192.168.1.12", "Móvil", "540 MB"),
        ("192.168.1.20", "Servidor", "3.8 GB"),
        ("192.168.1.30", "IoT", "120 MB"),
    ]

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
WAN0
  RX: 82.4 MB
  TX: 61.9 MB

LAN0
  RX: 42.2 MB
  TX: 36.3 MB
            </pre>
        </div>

        <div class="sep"></div>

        <!-- PANEL GRANDE: DISPOSITIVOS -->
        <div class="panel">
            <h3>🖥 Dispositivos Conectados</h3>

            <table style="width:100%; border-collapse:collapse; font-size:14px;">
                <tr style="color:#7fa9c9; text-align:left;">
                    <th>IP</th>
                    <th>Tipo</th>
                    <th>Tráfico</th>
                </tr>

                {''.join(f'''
                <tr>
                    <td>{ip}</td>
                    <td>{tipo}</td>
                    <td>{traf}</td>
                </tr>
                ''' for ip, tipo, traf in dispositivos_lista)}
            </table>
        </div>

        <div class="sep"></div>

        <!-- ACCESOS -->
        <div class="sep"></div>

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
