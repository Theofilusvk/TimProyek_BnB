const API_URL = 'http://localhost:8000';

// generate kotak input biaya sesuai jumlah kandidat yang diisi
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
  // validasi input sebelum dikirim ke backend
  const n = parseInt(document.getElementById('n').value) || 0;
  if (n < 12) {
    alert("Jumlah kandidat (n) harus minimal 12.");
    return;
  }
  const k = parseInt(document.getElementById('k').value) || 0;
  if (k < 5 || k > 10) {
    alert("Ukuran tim (k) harus antara 5 dan 10.");
    return;
  }
  if (k > n) {
    alert("Ukuran tim (k) tidak boleh lebih dari jumlah kandidat (n).");
    return;
  }

  // mengambil semua nilai biaya dari kotak input kandidat
  const inputs = document.querySelectorAll('.candidate-cost');
  const candidates = Array.from(inputs).map(inp => parseInt(inp.value) || 0);
  const budget = parseInt(document.getElementById('budget').value) || 0;

  document.getElementById('hasil').innerHTML = '<p>Memproses...</p>';

  // kirim data ke backend dan tampilkan hasilnya
  try {
    const res = await fetch(`${API_URL}/solve`, {
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

// tampilkan hasil tim terpilih dan ringkasan proses B&B
function tampilkan(data, candidates) {
  const { selected_team, total_cost, bb_summary } = data;

  // format angka jadi rupiah
  const formatRupiah = (angka) => {
    return angka.toLocaleString('id-ID');
  };

  // baris tabel dari kandidat yang terpilih
  const rows = selected_team.map(i =>
    `<tr><td>Kandidat ${i + 1}</td><td>Rp ${formatRupiah(candidates[i])}</td></tr>`
  ).join('');

  document.getElementById('hasil').innerHTML = `
    <h3>Tim Terpilih — Total: Rp ${formatRupiah(total_cost)}</h3>
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
