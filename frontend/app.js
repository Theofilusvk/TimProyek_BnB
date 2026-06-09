const API_URL = 'http://localhost:8000';

function generateCandidateInputs() {
  const n = parseInt(document.getElementById('n').value) || 0;
  const container = document.getElementById('candidate-inputs');
  container.innerHTML = '';
  for (let i = 0; i < n; i++) {
    const input = document.createElement('input');
    input.type = 'number';
    input.className = 'candidate-cost';
    input.placeholder = `Kandidat ${i + 1}`;
    container.appendChild(input);
  }
}

async function solve() {
  const inputs = document.querySelectorAll('.candidate-cost');
  const candidates = Array.from(inputs).map(inp => parseInt(inp.value) || 0);
  const k      = parseInt(document.getElementById('k').value);
  const budget = parseInt(document.getElementById('budget').value);

  document.getElementById('hasil').innerHTML = '<p>Memproses...</p>';

  try {
    const res  = await fetch(`${API_URL}/solve`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ candidates, k, budget })
    });
    const data = await res.json();
    tampilkan(data, candidates);
  } catch {
    document.getElementById('hasil').innerHTML =
      '<p style="color:red">Gagal konek ke backend.</p>';
  }
}

function tampilkan(data, candidates) {
  const { selected_team, total_cost, bb_summary } = data;

  const rows = selected_team.map(i =>
    `<tr><td>Kandidat ${i + 1}</td><td>Rp ${candidates[i]}</td></tr>`
  ).join('');

  document.getElementById('hasil').innerHTML = `
    <h3>Tim Terpilih — Total: Rp ${total_cost}</h3>
    <table>
      <thead><tr><th>Anggota</th><th>Biaya</th></tr></thead>
      <tbody>${rows}</tbody>
    </table>
    <div class="stats">
      <div class="stat"><span>${bb_summary.nodes_explored}</span>Nodes Explored</div>
      <div class="stat"><span>${bb_summary.nodes_pruned}</span>Nodes Pruned</div>
      <div class="stat"><span>${bb_summary.time_ms} ms</span>Waktu</div>
    </div>
  `;
}

function testDummy() {
  const candidates = [];
  tampilkan({
    selected_team: [0, 0, 0, 0, 0],
    total_cost: 0,
    bb_summary: { nodes_explored: 0, nodes_pruned: 0, time_ms: 0 }
  }, candidates);
}