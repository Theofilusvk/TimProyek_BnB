from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import time

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
    nodes_explored: int
    nodes_pruned: int
    time_ms: float

class SolveResponse(BaseModel):
    selected_team: List[int]
    total_cost: int
    bb_summary: BBSummary

@app.post("/solve", response_model=SolveResponse)
def solve_team(request: SolveRequest):
    bnb = BranchBound()
    
    # Menjalankan algoritma BnB
    team, cost, ada_solusi, summary = bnb.jalankan(request.candidates, request.k, request.budget)
    
    if not ada_solusi:
        # Jika Anda ingin mengembalikan response khusus saat tidak ada solusi
        # Bisa juga dibuat me-return 404 atau 400.
        pass

    return SolveResponse(
        selected_team=team,
        total_cost=cost,
        bb_summary=BBSummary(
            nodes_explored=summary["nodes_explored"],
            nodes_pruned=summary["nodes_pruned"],
            time_ms=summary["time"] * 1000  # konversi ke ms untuk frontend
        )
    )
