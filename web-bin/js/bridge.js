function renderBridge() {
    main.innerHTML = `
    <div class="panel">
        <h1>Bridge</h1>

        <button onclick="bridge('iniciar')">Enable</button>
        <button onclick="bridge('parar')">Stop</button>
        <button onclick="bridge('estado')">Status</button>

        <div class="sep"></div>
        <button onclick="bridge('configurar mostrar')">Show</button>

        <div id="out"></div>
    </div>`;
}

async function bridge(cmd) {
    showOutput(await sendCommand(`bridge ${cmd}`));
}
