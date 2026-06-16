from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

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
