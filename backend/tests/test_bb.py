import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from algorithm.branch_bound import BranchBound

## Definisi Method run_test()
# Kamus lokal
# nama : nama test
# costs : array of integer biaya
# k : jumlah orang
# budget : batas biaya
# bnb : objek BranchBound
# team : tim yang terpilih
# cost : total biaya
# ada_solusi : apakah solusi valid
# summary : ringkasan eksekusi
def run_test(nama, costs, k, budget):
    print(f"--- TEST {nama} ---")
    print(f"n = {len(costs)}, k = {k}, budget = {budget}")
    bnb = BranchBound()
    team, cost, ada_solusi, summary = bnb.jalankan(costs, k, budget)
    if (ada_solusi == True):
        print(f"Tim terpilih : {team}")
        print(f"Biaya masing2: {[costs[i] for i in team]}")
        print(f"Total biaya  : {cost}")
    else:
        print("TIDAK ADA SOLUSI YANG MEMENUHI SYARAT!")
    if (ada_solusi == True):
        print("Bisa?        : Ya")
    else:
        print("Bisa?        : Tidak")
    print(f"Nodes dibuat : {summary['nodes_generated']}")
    print(f"Nodes dicek  : {summary['nodes_explored']}")
    print(f"Nodes dipotong: {summary['nodes_pruned']}")
    print(f"Waktu        : {summary['time']:.5f} detik")
    print("----------------------\n")

## Program utama ##
# Kamus Lokal
# costs_small : array biaya untuk test small
# costs_med : array biaya untuk test medium
# costs_large : array biaya untuk test large
# costs_fail : array biaya untuk test gagal
# costs_tight : array biaya untuk test budget pas
def main():
    print("=" * 11)
    print("Menjalankan unit tests Branch & Bound...\n")
    costs_small = [10, 25, 15, 30, 20, 5, 35, 12, 18, 22, 8, 28]
    run_test("SMALL", costs_small, 5, 60)
    costs_med = [15, 40, 22, 35, 10, 28, 50, 18, 30, 12, 45, 25, 8, 38, 20, 33, 14, 42]
    run_test("MEDIUM", costs_med, 7, 110)
    costs_large = [20, 55, 30, 45, 15, 35, 60, 25, 40, 10, 50, 28, 12, 48, 22, 38, 18, 52, 32, 42, 8, 58, 26, 36]
    run_test("LARGE", costs_large, 8, 180)
    costs_fail = [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160]
    run_test("TIDAK ADA SOLUSI", costs_fail, 5, 100)
    costs_tight = [10, 25, 15, 30, 20, 5, 35, 12, 18, 22, 8, 28]
    run_test("TIGHT BUDGET", costs_tight, 5, 50)
    print("Program Selesai")

if __name__ == "__main__":
    main()
