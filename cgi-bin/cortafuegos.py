import html
from logic import send_to_srv_cli

def render(params):
    action = params.get("action", "")
    mode = params.get("mode", "")
    vlan = params.get("vlan", "")
    cli_output = ""
    cmd_sent = ""

    # Acciones directas
    if action in ("iniciar", "parar", "estado"):
        cmd_sent = f"cortafuegos {action}"
        cli_output = send_to_srv_cli(cmd_sent)

    # Entrar en configurar (sin ejecutar nada)
    elif action == "configurar" and not mode:
        cmd_sent = "cortafuegos configurar"
        cli_output = send_to_srv_cli(cmd_sent)

    # Ejecutar configurar con parámetros
    elif action == "configurar" and mode and vlan:
        cmd_sent = f"cortafuegos configurar {mode} {vlan}"
        cli_output = send_to_srv_cli(cmd_sent)

    return f"""
<div class='panel'>
  <h1>Cortafuegos</h1>
  <div style="margin:30px 0;"></div>
  <div class="sep"></div>

  <form method="post">
      <input type="hidden" name="menu" value="cortafuegos">
      <button name="action" value="iniciar">Iniciar</button>
      <button name="action" value="parar">Parar</button>
      <button name="action" value="configurar">Configurar</button>
      <button name="action" value="estado">Estado</button>
  </form>

  {"".join([f'''
  <div class="sep"></div>
  <form method="post">
      <input type="hidden" name="menu" value="cortafuegos">
      <input type="hidden" name="action" value="configurar">

      <div style="margin:10px 0;">
          <button name="mode" value="conectar">Conectar</button>
          <button name="mode" value="desconectar">Desconectar</button>
          <button name="mode" value="conectar_puertos_wls">Conectar Puertos WLS</button>
      </div>

      <div style="margin:10px 0;">
          VLAN: <input type="text" name="vlan" style="width:80px;">
      </div>
  </form>
  ''' if action == "configurar" else ""])}
  
  {f'''
  <div class='sep'></div>
  <div class='panel'>
    <h3>Script</h3>
    <pre>{html.escape(cmd_sent)}</pre>
    <h3>CLI Output</h3>
    <pre>{html.escape(cli_output)}</pre>
  </div>
  ''' if cmd_sent else ""}
</div>
"""
