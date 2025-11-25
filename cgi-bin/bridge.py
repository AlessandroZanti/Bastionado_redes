import html
from logic import send_to_srv_cli

def render(params):
    action = params.get("action", "")
    
    mode = params.get("mode", "")
    subtype = params.get("subtype", "")
    vlan_name = params.get("vlan_name", "")
    vlan_id = params.get("vlan_id", "")
    vlan_ip = params.get("vlan_ip", "")
    dev_ip = params.get("dev_ip", "")
    cli_output = ""
    cmd_sent = ""

    if action in ("iniciar", "parar", "estado"):
        cmd_sent = f"bridge {action}"
        cli_output = send_to_srv_cli(cmd_sent)
    if action == "configurar" and mode == "guardar" and subtype == "vlan" and vlan_name:
        cmd_sent = f"bridge configur guardar vlan {vlan_name} {vlan_id} {vlan_ip} {dev_ip}"
        cli_output = send_to_srv_cli(cmd_sent)

    return f"""

    <div class='panel'>
  <h1>Bridge</h1>

  <form method="post">
      <input type="hidden" name="menu" value="bridge">
      <button name="action" value="iniciar">Enable</button>
      <button name="action" value="configurar">Configure</button>
      <button name="action" value="parar">Stop</button>
      <button name="action" value="estado">Status</button>
  </form>

 {"""
<div class="sep"></div>
<form method="post">
    <input type="hidden" name="menu" value="bridge">
    <input type="hidden" name="action" value="configurar">

    <div style="margin: 10px 0;">
        <button type="submit" name="mode" value="mostrar">Show</button>
        <button type="submit" name="mode" value="guardar">Save</button>
        <button type="submit" name="mode" value="borrar">Delete</button>
    </div>

    """ + (
        '''
        <div style="margin-top: 15px;">
    <input type="hidden" name="mode" value="guardar">

    <button type="submit" name="subtype" value="vlan">VLAN</button>
    <button type="submit" name="subtype" value="bridge">Bridge</button>
    <button type="submit" name="subtype" value="bridge_if">Bridge IF</button><br>
</div>

        '''
        if mode == "guardar" else ""
   ) + (

'''
<div style="margin-top: 15px; border:1px solid #444; padding:10px; display:flex; align-items:center; gap:10px; flex-wrap:wrap;">

    <input type="hidden" name="mode" value="guardar">
    <input type="hidden" name="subtype" value="vlan">

    <label>Name:</label>
    <input 
        type="text" 
        name="vlan_name" 
        placeholder="Vlan_2" 
        style="width:45px;">

    <label>ID:</label>
    <input 
        type="text" 
        name="vlan_id" 
        placeholder="2" 
        style="width:15px;">

    <label>IP/MASC:</label>
    <input 
        type="text" 
        name="vlan_ip" 
        placeholder="192.168.2.1/24" 
        style="width:90px;">

    <label>DEV IP/MASC:</label>
    <input 
        type="text" 
        name="dev_ip" 
        placeholder="192.168.2.10/24" 
        style="width:100px;">

    <button type="submit">Ok</button>
</div>
'''
if mode == "guardar" and subtype == "vlan" else ""
) + """
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
