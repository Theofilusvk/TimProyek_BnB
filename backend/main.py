from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import pandas as pd
import io

from algorithm.branch_bound import BranchBound

app = FastAPI()

# Tambahkan CORS middleware agar frontend bisa memanggil API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Anda bisa spesifikkan origin jika perlu (misal: http://127.0.0.1:5500)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SolveRequest(BaseModel):
    candidates: List[int]
    k: int
    budget: int

class BBSummary(BaseModel):
    nodes_generated: int
    nodes_explored: int
    nodes_pruned: int
    time_ms: float
    expansion_order: List[Dict[str, Any]]

class SolveResponse(BaseModel):
    ada_solusi: bool
    selected_team: List[int]
    total_cost: int
    bb_summary: BBSummary

@app.post("/solve", response_model=SolveResponse)
def solve_team(request: SolveRequest):
    n = len(request.candidates)
    if n < 12:
        raise HTTPException(status_code=400, detail="Jumlah kandidat (n) minimal 12")
    if not (5 <= request.k <= 10):
        raise HTTPException(status_code=400, detail="Ukuran tim (k) harus antara 5 dan 10")
    if request.k > n:
        raise HTTPException(status_code=400, detail="Ukuran tim (k) tidak boleh lebih dari jumlah kandidat (n)")
    if request.budget <= 0:
        raise HTTPException(status_code=400, detail="Anggaran (B) harus lebih dari 0")

    bnb = BranchBound()

    # Menjalankan algoritma BnB
    team, cost, ada_solusi, summary = bnb.jalankan(request.candidates, request.k, request.budget)

    return SolveResponse(
        ada_solusi=ada_solusi,
        selected_team=team,
        total_cost=cost,
        bb_summary=BBSummary(
            nodes_generated=summary["nodes_generated"],
            nodes_explored=summary["nodes_explored"],
            nodes_pruned=summary["nodes_pruned"],
            time_ms=summary["time"] * 1000,
            expansion_order=summary["expansion_order"]
        )
    )

@app.post("/upload-data")
async def upload_data(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents), sep=None, engine='python')
        elif file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
            df = pd.read_excel(io.BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="Format file tidak didukung. Gunakan .csv atau .xlsx")
        
        numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        numeric_df = df.select_dtypes(include=numerics)
        
        if numeric_df.empty:
            raise HTTPException(status_code=400, detail="Tidak ditemukan kolom angka pada file.")
            
        costs = numeric_df.iloc[:, 0].dropna().astype(int).tolist()
        return {"costs": costs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal memproses file: {str(e)}")

