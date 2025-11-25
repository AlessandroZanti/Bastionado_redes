import html
from logic import send_to_srv_cli
import re
import os

def render(params, interfaces):
    action = params.get("action", "")
    mode   = params.get("mode", "dhcp")
    iface  = params.get("iface", "")

    cli_output = ""
    cmd_sent = ""

    # Ejecutar comandos WAN
    if action == "iniciar":
        cmd_sent = "ifwan iniciar"
    elif action == "parar":
        cmd_sent = "ifwan parar"
    elif action == "configurar" and iface:
        cmd_sent = "interfaces listar"
        cmd_sent = f"ifwan configurar {mode} {iface}"

    if cmd_sent:
        cli_output = send_to_srv_cli(cmd_sent)

    # 🔹 Leer interfaces reales desde interfaces.conf
    conf_path = "/usr/local/JSBach/conf/interfaces.conf"
    interfaces_list = []
    if os.path.exists(conf_path):
        with open(conf_path, "r") as f:
            for line in f:
                m = re.match(r"\s*\d+\s*-\s*([A-Za-z0-9._-]+)", line)
                if m:
                    interfaces_list.append(m.group(1))

    # Construir <option> desde interfaces.conf
    iface_opts = "".join(
        f"<option value='{i}' {'selected' if i==iface else ''}>{i}</option>"
        for i in interfaces_list
    )

    # HTML final
    return f"""
<div class='panel'>
  <h1>WAN</h1>

  <form method="post">
      <input type="hidden" name="menu" value="wan">
      <button name="action" value="iniciar">Enable</button>
      <button name="action" value="configurar">Configure</button>
      <button name="action" value="parar">Stop</button>
  </form>

  {"""
  <div class="sep"></div>
  <form method="post">
      <input type="hidden" name="menu" value="wan">
      <input type="hidden" name="action" value="configurar">

      Mode:
      <select name="mode">
          <option value="dhcp" {'selected' if mode=='dhcp' else ''}>DHCP</option>
          <option value="manual" {'selected' if mode=='manual' else ''}>Manual</option>
      </select>

      Interface:
      <select name="iface">{iface_opts}</select>

      <button type="submit">Apply</button>
  </form>
  """ if action == "configurar" else ""}

  {f"""
  <div class="sep"></div>
  <div class='panel'>
    <h3>Script</h3><pre>{html.escape(cmd_sent)}</pre>
    <h3>CLI Output</h3><pre>{html.escape(cli_output)}</pre>
  </div>
  """ if action else ""}
</div>
"""
