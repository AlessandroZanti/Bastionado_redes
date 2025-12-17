function renderCortafuegos() {
    main.innerHTML = `
    <div class="panel">
        <h1>Cortafuegos</h1>

        <button onclick="fw('iniciar')">Iniciar</button>
        <button onclick="fw('parar')">Parar</button>
        <button onclick="fw('estado')">Estado</button>

        <div class="sep"></div>
        <input id="fw-vlan" placeholder="VLAN">
        <button onclick="fwConfig('conectar')">Conectar</button>
        <button onclick="fwConfig('desconectar')">Desconectar</button>

        <div id="out"></div>
    </div>`;
}

async function fw(action) {
    showOutput(await sendCommand(`cortafuegos ${action}`));
}

async function fwConfig(mode) {
    showOutput(await sendCommand(`cortafuegos configurar ${mode} ${fw - vlan.value}`));
}
