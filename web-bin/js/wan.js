function renderWAN() {
    const main = document.getElementById("main");

    main.innerHTML = `
    <div class="panel">
        <h1>WAN</h1>

        <button onclick="wanAction('iniciar')">Enable</button>
        <button onclick="showWanConfig()">Configure</button>
        <button onclick="wanAction('parar')">Stop</button>
        <button onclick="wanAction('estado')">State</button>
        <button onclick="wanAction('interfaces')">Interfaces</button>

        <div id="wan-config"></div>
        <div id="wan-output"></div>
    </div>`;
}

async function wanAction(action) {
    let cmd = `ifwan ${action}`;
    if (action === "interfaces") cmd = "interfaces listar";

    const res = await sendCommand(cmd);
    showOutput(res);
}

function showWanConfig() {
    document.getElementById("wan-config").innerHTML = `
    <div class="sep"></div>
    <select id="wan-mode" onchange="toggleWanManual()">
        <option value="dhcp">DHCP</option>
        <option value="manual">Manual</option>
    </select>

    <input id="iface" placeholder="Iface" style="width:70px">

    <span id="manual-fields" style="display:none">
        <input id="ip" placeholder="IP/MASK">
        <input id="gw" placeholder="GW">
        <input id="dns" placeholder="DNS">
    </span>

    <button onclick="applyWan()">Apply</button>`;
}

function toggleWanManual() {
    document.getElementById("manual-fields").style.display =
        document.getElementById("wan-mode").value === "manual" ? "inline" : "none";
}

async function applyWan() {
    const mode = wan - mode.value;
    const iface = iface.value;
    let cmd = `ifwan configurar ${mode} ${iface}`;

    if (mode === "manual") {
        cmd += ` ${ip.value} ${gw.value} ${dns.value}`;
    }

    showOutput(await sendCommand(cmd));
}
