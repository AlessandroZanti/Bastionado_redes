function renderEnrutar() {
    main.innerHTML = `
    <div class="panel">
        <h1>Routing</h1>

        <button onclick="enrutar('iniciar')">On</button>
        <button onclick="enrutar('parar')">Off</button>
        <button onclick="enrutar('estado')">Status</button>

        <div class="sep"></div>
        <input id="rt-iface" placeholder="Iface">
        <button onclick="enrutarConfig()">Configure</button>

        <div id="out"></div>
    </div>`;
}

async function enrutar(action) {
    showOutput(await sendCommand(`enrutar ${action}`));
}

async function enrutarConfig() {
    showOutput(await sendCommand(`enrutar configurar ${rt - iface.value}`));
}
