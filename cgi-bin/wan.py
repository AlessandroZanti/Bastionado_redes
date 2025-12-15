import html
from logic import send_to_srv_cli
import re
import os

def render(params, interfaces):
    action = params.get("action", "")
    mode   = params.get("mode", "dhcp")
    iface  = params.get("iface", "")
    ip     = params.get("ip", "")
    gw     = params.get("gw", "")
    dns    = params.get("dns", "")

    cli_output = ""
    cmd_sent = ""

    # Ejecutar comandos WAN
    if action == "iniciar":
        cmd_sent = "ifwan iniciar"
    elif action == "parar":
        cmd_sent = "ifwan parar"
    elif action == "estado":
        cmd_sent = "ifwan estado"
    elif action == "configurar":
        # Construir comando según modo
        if iface:
            if mode == "manual" and ip and gw and dns:
                cmd_sent = f"ifwan configurar {mode} {iface} {ip} {gw} {dns}"
            else:
                cmd_sent = f"ifwan configurar {mode} {iface}"
        else:
            cmd_sent = "interfaces listar"

    # Ejecutar el comando
    if cmd_sent:
        cli_output = send_to_srv_cli(cmd_sent)

    # Parsear la salida (solo si se listan interfaces)
    interfaces_list = []
    if action == "configurar" and cmd_sent == "interfaces listar" and cli_output:
        for line in cli_output.splitlines():
            line = line.strip()
            m = re.search(r"\d+\s*-\s*([A-Za-z0-9._-]+)", line)
            if m:
                interfaces_list.append(m.group(1))


    # HTML final
    return f"""
<div class='panel'>
    <h1>WAN</h1>

    <form method="post">
        <input type="hidden" name="menu" value="wan">
        <button name="action" value="iniciar">Enable</button>
        <button name="action" value="configurar">Configure</button>
        <button name="action" value="parar">Stop</button>
        <button name="action" value="estado">State</button>
    </form>

    {'<div class="sep"></div>' if action == "configurar" else ''}

    {f'''
    <form method="post">
        <input type="hidden" name="menu" value="wan">
        <input type="hidden" name="action" value="configurar">

        Mode:
        <select name="mode">
            <option value="dhcp" {'selected' if mode=='dhcp' else ''}>DHCP</option>
            <option value="manual" {'selected' if mode=='manual' else ''}>Manual</option>
        </select>

        Interface:
        <input type="text" name="iface" value="" placeholder="Escribe la interfaz" style="width:80px;">

        <button type="submit">Apply</button>
    </form>
    ''' if action == "configurar" else ''}

    {f'''
    <div class="sep"></div>
    <div class='panel'>
        <h3>Script</h3><pre>{html.escape(cmd_sent)}</pre>
        <h3>CLI Output</h3><pre>{html.escape(cli_output)}</pre>
    </div>
    ''' if action else ''}
</div>
"""
