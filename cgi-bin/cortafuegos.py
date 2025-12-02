import html
from logic import send_to_srv_cli

def render(params):
    action = params.get("action", "")
    cli_output = ""
    cmd_sent = ""

    if action in ("pene1", "pene2", "pene3", "pene4"):
        cmd_sent = f"cortafuegos {action}"
        cli_output = send_to_srv_cli(cmd_sent)

    return f"""

<div class='panel'>
  <h1>Cortafuegos</h1>

  <form method="post">
      <input type="hidden" name="menu" value="cortafuegos">
      <button name="action" value="pene1">pene1</button>
      <button name="action" value="pene2">pene2</button>
      <button name="action" value="pene3">pene3</button>
      <button name="action" value="pene4">pene4</button>
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
