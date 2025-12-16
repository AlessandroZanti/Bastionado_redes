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
    elif action == "interfaces":
        cmd_sent = "interfaces listar"
    # Ejecutar el comando
    if cmd_sent:
        cli_output = send_to_srv_cli(cmd_sent)

    # HTML final
    return f"""
<div class='panel'>
    <h1>WAN</h1>
    <div style="margin:30px 0;"></div>
    <div class="sep"></div>

    <form method="post">
        <input type="hidden" name="menu" value="wan">
        <button name="action" value="iniciar">Enable</button>
        <button name="action" value="configurar">Configure</button>
        <button name="action" value="parar">Stop</button>
        <button name="action" value="estado">State</button>
        <button name="action" value="interfaces">Interfaces</button>
    </form>

    {'<div class="sep"></div>' if action == "configurar" else ''}

    {f'''
<form method="post" style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
    <input type="hidden" name="menu" value="wan">
    <input type="hidden" name="action" value="configurar">

    Mode:
    <select name="mode" id="mode-select" onchange="toggleManualFields()">
        <option value="dhcp" {'selected' if mode=='dhcp' else ''}>DHCP</option>
        <option value="manual" {'selected' if mode=='manual' else ''}>Manual</option>
    </select>

    Interface:
    <input type="text" name="iface" value="" placeholder="Iface" style="width:70px;">

    <div id="manual-fields" style="display: {'inline-flex' if mode=='manual' else 'none'}; gap:10px; align-items:center;">
        IP/MASC:
        <input type="text" name="ip" value="" placeholder="IP/MASC" style="width:100px;">

        Gateway:
        <input type="text" name="gw" value="" placeholder="Gateway" style="width:80px;">

        DNS:
        <input type="text" name="dns" value="" placeholder="DNS" style="width:80px;">
    </div>

    <button type="submit">Apply</button>
</form>

<script>
function toggleManualFields() {{
    var mode = document.getElementById('mode-select').value;
    var manualFields = document.getElementById('manual-fields');
    manualFields.style.display = (mode === 'manual') ? 'inline-flex' : 'none';
}}
</script>


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
