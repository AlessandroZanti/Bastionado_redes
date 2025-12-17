function bytesAMb(b) {
    return (b / 1024 / 1024).toFixed(1) + " MB";
}

function leerTrafico() {
    return {
        rx: bytesAMb(rand(50, 500) * 1024 * 1024),
        tx: bytesAMb(rand(20, 300) * 1024 * 1024)
    };
}

function leerInterfaces() {
    const t = leerTrafico();
    return `eno1\n  RX: ${t.rx}\n  TX: ${t.tx}\n`;
}

function leerDispositivos() {
    const n = rand(3, 8);
    const out = [];
    for (let i = 0; i < n; i++) {
        out.push({
            ip: `192.168.1.${100 + i}`,
            estado: "Activo",
            trafico: rand(1,50) + " MB"
        });
    }
    return out;
}

function rand(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function renderInicio() {
    const traf = leerTrafico();
    const interfaces = leerInterfaces();
    const dispositivos = leerDispositivos();

    document.getElementById('main').innerHTML = `
    <div class="panel">
        <h1 style="color:#4dc0ff">Network Control</h1>
        <p>Panel central de administración</p>

        <div class="sep"></div>

        <div class="panel">
            <h3>Estado General</h3>
            <p>RX: ${traf.rx}</p>
            <p>TX: ${traf.tx}</p>
            <p>Dispositivos: ${dispositivos.length}</p>
            <p>Sistema: <span style="color:#0f8">Operativo</span></p>
        </div>

        <div class="sep"></div>

        <div class="panel">
            <h3>Tráfico por Interfaces</h3>
            <pre>${interfaces}</pre>
        </div>

        <div class="sep"></div>

        <div class="panel">
            <h3>Dispositivos</h3>
            <table width="100%">
                <tr><th>IP</th><th>Estado</th><th>Tráfico</th></tr>
                ${dispositivos.map(d =>
                    `<tr><td>${d.ip}</td><td>${d.estado}</td><td>${d.trafico}</td></tr>`
                ).join("")}
            </table>
        </div>
    </div>`;
}
