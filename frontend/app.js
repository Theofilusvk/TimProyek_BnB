const API_URL = 'http://localhost:8000';

// Preset Ukuran 

// Terapkan preset ukuran (Small/Medium/Large) dan isi biaya acak
function applyPreset(n) {
  document.getElementById('n').value = n;
  generateCandidateInputs();
  // Isi biaya acak 20–100 agar bisa langsung demo
  document.querySelectorAll('.candidate-cost').forEach(inp => {
    inp.value = Math.floor(Math.random() * 81) + 20;
  });
  // Highlight tombol preset aktif
  document.querySelectorAll('.btn-preset').forEach(btn => btn.classList.remove('active'));
  const map = { 12: 'btn-small', 18: 'btn-medium', 24: 'btn-large' };
  if (map[n]) document.getElementById(map[n]).classList.add('active');
}

// Generate Input Kandidat 

// Generate kotak input biaya sesuai jumlah kandidat yang diisi
function generateCandidateInputs() {
  const n = parseInt(document.getElementById('n').value) || 0;
  const container = document.getElementById('candidate-inputs');
  const section   = document.getElementById('candidate-section');
  container.innerHTML = '';
  if (n <= 0) {
    section.style.display = 'none';
    return;
  }
  section.style.display = '';
  for (let i = 0; i < n; i++) {
    const wrapper = document.createElement('div');
    wrapper.className = 'candidate-item';

    const lbl = document.createElement('span');
    lbl.className = 'candidate-label';
    lbl.textContent = `K-${i + 1}`;

    const input = document.createElement('input');
    input.type = 'number';
    input.className = 'candidate-cost';
    input.placeholder = `c[${i}]`;
    input.id = `c_${i}`;
    input.min = '1';

    wrapper.appendChild(lbl);
    wrapper.appendChild(input);
    container.appendChild(wrapper);
  }
}

// Reset Form 

function resetForm() {
  document.getElementById('n').value = '';
  document.getElementById('k').value = '';
  document.getElementById('budget').value = '';
  document.getElementById('candidate-inputs').innerHTML = '';
  document.getElementById('candidate-section').style.display = 'none';
  document.getElementById('hasil').innerHTML = '';
  document.querySelectorAll('.btn-preset').forEach(btn => btn.classList.remove('active'));
}

// Solve

async function solve() {
  // Validasi input sebelum dikirim ke backend
  const n = parseInt(document.getElementById('n').value) || 0;
  if (n < 12) {
    showAlert('Jumlah kandidat (n) harus minimal 12.');
    return;
  }
  const k = parseInt(document.getElementById('k').value) || 0;
  if (k < 5 || k > 10) {
    showAlert('Ukuran tim (k) harus antara 5 dan 10.');
    return;
  }
  if (k > n) {
    showAlert('Ukuran tim (k) tidak boleh lebih dari jumlah kandidat (n).');
    return;
  }
  const budget = parseInt(document.getElementById('budget').value) || 0;
  if (budget <= 0) {
    showAlert('Batas anggaran (B) harus lebih dari 0.');
    return;
  }

  // Mengambil semua nilai biaya dari kotak input kandidat
  const inputs     = document.querySelectorAll('.candidate-cost');
  const candidates = Array.from(inputs).map(inp => parseInt(inp.value) || 0);

  // Tampilkan loading
  document.getElementById('hasil').innerHTML = `
    <div class="loading">
      <div class="spinner"></div>
      <p>Menjalankan Branch &amp; Bound…</p>
    </div>`;

  // Kirim data ke backend dan tampilkan hasilnya
  try {
    const res = await fetch(`${API_URL}/solve`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ candidates, k, budget })
    });
    if (!res.ok) {
      const err = await res.json();
      showError(err.detail || 'Terjadi kesalahan di server.');
      return;
    }
    const data = await res.json();
    tampilkan(data, candidates);
  } catch {
    showError('Gagal konek ke backend. Pastikan server berjalan di localhost:8000.');
  }
}

// Tampilkan Hasil 

function tampilkan(data, candidates) {
  const { ada_solusi, selected_team, total_cost, bb_summary } = data;

  // Format angka ribuan
  const fmt = (n) => Number(n).toLocaleString('id-ID');

  let html = '';

  // Bagian 1: Status solusi 
  if (!ada_solusi) {
    html += `
      <div class="alert-no-solution">

        <div>
          <strong>Tidak ada solusi ditemukan.</strong>
          <p>Tidak ada kombinasi tim sebanyak ${document.getElementById('k').value} orang
          yang totalnya ≤ anggaran. Coba naikkan anggaran atau kurangi ukuran tim.</p>
        </div>
      </div>`;
  } else {
    // Tabel tim terpilih
    const rows = selected_team.map(i =>
      `<tr>
        <td><span class="badge-kandidat">K-${i + 1}</span></td>
        <td>Rp ${fmt(candidates[i])}</td>
      </tr>`
    ).join('');

    html += `
      <div class="result-header">

        <div>
          <strong>Tim Terpilih Ditemukan</strong>
          <p>Total Biaya: <strong>Rp ${fmt(total_cost)}</strong>
             dari ${selected_team.length} anggota</p>
        </div>
      </div>
      <table>
        <thead><tr><th>Kandidat</th><th>Biaya</th></tr></thead>
        <tbody>${rows}</tbody>
      </table>`;
  }

  // Bagian 2: Statistik B&B 
  html += `
    <h3 class="section-title">Ringkasan Proses B&amp;B</h3>
    <div class="stats">
      <div class="stat">
        <span>${bb_summary.nodes_generated != null ? fmt(bb_summary.nodes_generated) : '—'}</span>Nodes Generated
      </div>
      <div class="stat">
        <span>${fmt(bb_summary.nodes_explored)}</span>Nodes Explored
      </div>
      <div class="stat">
        <span>${fmt(bb_summary.nodes_pruned)}</span>Nodes Pruned
      </div>
      <div class="stat">
        <span>${bb_summary.time_ms.toFixed(2)}</span>Waktu (ms)
      </div>
    </div>`;

  // Bagian 3: Expansion Order 
  const eo = bb_summary.expansion_order;
  if (eo && eo.length > 0) {
    // Batasi tampilan maks 50 baris agar tidak berat
    const displayed = eo.slice(0, 50);
    const isTruncated = eo.length > 50;

    const eoRows = displayed.map(node => {
      const selLabel = node.selected.length > 0
        ? node.selected.map(i => `K-${i + 1}`).join(', ')
        : '—';
      let tersediaLabel = '—';
      if (node.tersedia && node.tersedia.length > 0) {
        if (node.tersedia.length > 3) {
          tersediaLabel = `K-${node.tersedia[0] + 1} s.d K-${node.tersedia[node.tersedia.length - 1] + 1}`;
        } else {
          tersediaLabel = node.tersedia.map(i => `K-${i + 1}`).join(', ');
        }
      }
      const boundLabel = node.bound >= 9999999 ? '∞ (pruned)' : node.bound;
      
      let statusStyle = '';
      if (node.status && node.status.includes('Pruned')) statusStyle = 'color: #e53e3e;';
      else if (node.status && node.status.includes('Solusi')) statusStyle = 'color: #38a169; font-weight: bold;';

      return `<tr>
        <td class="text-center">${node.urutan}</td>
        <td class="text-center">${node.level}</td>
        <td>${selLabel}</td>
        <td><small style="color: #666;">${tersediaLabel}</small></td>
        <td class="text-right">${node.cost}</td>
        <td class="text-right">${boundLabel}</td>
        <td style="${statusStyle}">${node.status || 'Diekspansi'}</td>
      </tr>`;
    }).join('');

    html += `
      <h3 class="section-title">Urutan Ekspansi Simpul (Expansion Order)</h3>
      <div class="expansion-wrapper">
        <table class="expansion-table">
          <thead>
            <tr>
              <th class="text-center">#</th>
              <th class="text-center">Level</th>
              <th>Kandidat Terpilih</th>
              <th>Kandidat Tersedia</th>
              <th class="text-right">Cost</th>
              <th class="text-right">Bound (ĉ)</th>
              <th>Status / Prune</th>
            </tr>
          </thead>
          <tbody>${eoRows}</tbody>
        </table>
        ${isTruncated
          ? `<p class="truncate-note">Menampilkan 50 dari ${fmt(eo.length)} simpul yang diekspansi.</p>`
          : ''}
      </div>`;
  }

  document.getElementById('hasil').innerHTML = html;
}

// Helper UI 

function showAlert(msg) {
  document.getElementById('hasil').innerHTML =
    `<div class="alert-warn">${msg}</div>`;
}

function showError(msg) {
  document.getElementById('hasil').innerHTML =
    `<div class="alert-error">${msg}</div>`;
}

// Fitur Import Excel / CSV 

function triggerUpload() {
  document.getElementById('file-upload').click();
}

async function handleFileUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append('file', file);

  document.getElementById('hasil').innerHTML = `
    <div class="loading">
      <div class="spinner"></div>
      <p>Membaca file ${file.name}...</p>
    </div>`;

  try {
    const res = await fetch(`${API_URL}/upload-data`, {
      method: 'POST',
      body: formData
    });

    if (!res.ok) {
      const err = await res.json();
      showError(err.detail || 'Gagal memproses file.');
      document.getElementById('file-upload').value = '';
      return;
    }

    const data = await res.json();
    const costs = data.costs;

    if (!costs || costs.length === 0) {
      showError('Tidak ditemukan data angka yang valid di dalam file.');
      return;
    }

    // Update UI
    document.getElementById('n').value = costs.length;
    generateCandidateInputs();
    
    // Auto-fill values
    const inputs = document.querySelectorAll('.candidate-cost');
    costs.forEach((cost, index) => {
      if (inputs[index]) {
        inputs[index].value = cost;
      }
    });

    document.getElementById('hasil').innerHTML = `<div class="alert-success">Berhasil mengimpor ${costs.length} data biaya dari ${file.name}!</div>`;
    document.getElementById('file-upload').value = '';

    // Reset aktif preset buttons
    document.querySelectorAll('.btn-preset').forEach(btn => btn.classList.remove('active'));

  } catch (err) {
    showError('Gagal mengirim file ke server.');
    document.getElementById('file-upload').value = '';
  }
}

