import html
from logic import send_to_srv_cli

def render(params):
    action = params.get("action", "")
    cli_output = ""
    cmd_sent = ""

    if action in ("iniciar", "parar", "estado"):
        cmd_sent = f"enrutar {action}"
        cli_output = send_to_srv_cli(cmd_sent)

    return f"""
<div class='panel'>
  <h1>Routing</h1>

  <form method="post">
      <input type="hidden" name="menu" value="enrutar">
      <button name="action" value="iniciar">On</button>
      <button name="action" value="parar">Off</button>
      <button name="action" value="estado">Status</button>
  </form>

  {f"""
  <div class='sep'></div>
  <div class='panel'>
    <h3>Script</h3><pre>{html.escape(cmd_sent)}</pre>
    <h3>CLI Output</h3><pre>{html.escape(cli_output)}</pre>
  </div>
  """ if action else ""}
</div>
"""

