async function sendCommand(cmd) {
    // TEMPORAL: simulación
    return {
        cmd,
        output: `Simulated output for:\n${cmd}`
    };
}

function showOutput(res) {
    document.getElementById("out").innerHTML = `
    <div class="panel">
        <h3>Script</h3><pre>${res.cmd}</pre>
        <h3>CLI Output</h3><pre>${res.output}</pre>
    </div>`;
}
