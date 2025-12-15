import html
from logic import send_to_srv_cli

def render(params):
    # -------------------------
    #   PARÁMETROS
    # -------------------------
    action  = params.get("action", "")
    mode    = params.get("mode", "")
    subtype = params.get("subtype", "")

    cli_output = ""
    cmd_sent = ""

    vlan_name = params.get("vlan_name", "")
    vlan_id   = params.get("vlan_id", "")
    vlan_ip   = params.get("vlan_ip", "")
    dev_ip    = params.get("dev_ip", "")

    vlanb_id = params.get("vlanb_id", "")

    # -------------------------
    #   PROCESAR ACCIONES
    # -------------------------
    # Enable
    if action == "iniciar":
        cmd_sent = f"bridge iniciar"
        cli_output = send_to_srv_cli(cmd_sent)
        
    # Configure
    if action == "configurar":
        cli_output = "ara q retrasao"
        if mode == "mostrar":
            cmd_sent = f"bridge configurar mostrar"
            cli_output = send_to_srv_cli(cmd_sent)
        if mode == "guardar":
            if subtype == "vlan" and vlan_name:
                cmd_sent = f"bridge configurar guardar vlan {vlan_name} {vlan_id} {vlan_ip} {dev_ip}"
                cli_output = send_to_srv_cli(cmd_sent)
        if mode == "borrar":
            cmd_sent = f"bridge configurar borrar {subtype}"
            cli_output = send_to_srv_cli(cmd_sent)
            if subtype == "vlan":
                cmd_sent = f"bridge configurar borrar vlan {vlanb_id}"
                cli_output = send_to_srv_cli(cmd_sent)
            if subtype == "bridge":
                cmd_sent = f"bridge configurar borrar bridge {bridge_name}"
                cli_output = send_to_srv_cli(cmd_sent)
    
    # Disable
    if action == "parar":
        cmd_sent = f"bridge parar"
        cli_output = send_to_srv_cli(cmd_sent)

    # Status
    if action == "estado":
        cmd_sent = f"bridge estado"
        cli_output = send_to_srv_cli(cmd_sent)

    # Show
    if action == "mostrar":
        cmd_sent = f"vlan_sho"
        cli_output = send_to_srv_cli(cmd_sent)


    # -------------------------
    #   UTILIDADES HTML
    # -------------------------
    def hidden(**vals):
        """Genera inputs hidden rápidamente."""
        return "\n".join(
            f'<input type="hidden" name="{k}" value="{v}">'
            for k, v in vals.items()
        )

    def button(name, value, label=None):
        return f'<button name="{name}" value="{value}">{label or value}</button>'

    # -------------------------
    #   HTML PRINCIPAL
    # -------------------------
    html_main = f"""
    <div class='panel'>
        <h1>Bridge</h1>
        <div style="margin:40px 0;"></div>
        <!-- BOTONES PRINCIPALES -->
        <form method="post">
            {hidden(menu="bridge")}
            {button("action", "iniciar", "Enable")}
            {button("action", "configurar", "Configure")}
            {button("action", "parar", "Stop")}
            {button("action", "estado", "Status")}
            {button("action", "mostrar", "Show")}
        </form>
    """

    # -------------------------
    #   CONFIGURACIÓN
    # -------------------------
    if action == "configurar":
        html_main += f"""
        <div class="sep"></div>
        <form method="post">
            {hidden(menu="bridge", action="configurar")}
            <div style="margin:10px 0;">
                {button("mode", "mostrar", "Show")}
                {button("mode", "guardar", "Save")}
                {button("mode", "borrar", "Delete")}
            </div>
            <div style="margin:10px 0;">
        """
        if mode == "guardar":
            html_main += f"""
            <div class="sep"></div>
            <div style="margin-top: 10px;">
                {hidden(mode="guardar")}
                {button("subtype", "vlan", "VLAN")}
                {button("subtype", "bridge", "Bridge")}
                {button("subtype", "bridge_if", "Bridge IF")}
            </div>
            """
            
            if subtype == "vlan":
                html_main += f"""
            <div style="margin-top:20px; border:1px solid #444; padding:10px; display:flex; gap:10px; flex-wrap:wrap;">

                {hidden(mode="guardar", subtype="vlan")}

                <label>Name:</label>
                <input name="vlan_name" placeholder="Vlan_2" style="width:70px;">

                <label>ID:</label>
                <input name="vlan_id" placeholder="2" style="width:40px;">

                <label>IP/MASC:</label>
                <input name="vlan_ip" placeholder="192.168.2.1/24" style="width:120px;">

                <label>DEV IP/MASC:</label>
                <input name="dev_ip" placeholder="192.168.2.10/24" style="width:120px;">

                <button type="submit">OK</button>
            </div>
            """
            
        if mode == "borrar":
            html_main += f"""
            <div class="sep"></div>
            <div style="margin-top: 10px;">
                {hidden(mode="borrar")}
                {button("subtype", "vlan", "VLAN")}
                {button("subtype", "bridge", "Bridge")}
            </div>
            """
            if subtype == "vlan":
                html_main += f"""
            <div style="margin-top:10px; border:1px solid #444; padding:10px; display:flex; gap:10px; flex-wrap:wrap;">

                {hidden(mode="borrar", subtype="vlan")}

                <label>ID:</label>
                <input name="vlanb_id" placeholder="2" style="width:40px;">

                <button type="submit">OK</button>
            </div>
            """

        html_main += "</form>"

    # -------------------------
    #   SALIDA CLI
    # -------------------------
    if action:
        html_main += f"""
        <div class="sep"></div>
        <div class='panel'>
            <h3>Script</h3><pre>{html.escape(cmd_sent)}</pre>

            <h3>CLI Output</h3><pre>{html.escape(cli_output)}</pre>
        </div>
        """

    html_main += "</div>"
    return html_main
