import time

## Definisi Kelas ##
## Definisi Kelas Node
## Definisi Atribut
# level : level kedalaman di pohon
# selected : list kandidat yang sudah dipilih
# cost : biaya aktual sejauh ini
# bound : batas bawah (c_hat)
class Node:
    ## Definisi Konstruktor
    # Kamus Lokal
    # level : level kedalaman di pohon
    # selected : kandidat yang dipilih
    # cost : biaya aktual
    # bound : batas bawah
    def __init__(self, level, selected, cost, bound):
        self.level = level
        self.selected = list(selected)
        self.cost = cost
        self.bound = bound

## Definisi Kelas ##
## Definisi Kelas BranchBound
## Definisi Atribut
# Q : antrian prioritas
# node_counter : penghitung urutan node masuk
class BranchBound:
    ## Definisi Konstruktor
    # Kamus Lokal
    def __init__(self):
        self.Q = []
        self.node_counter = 0

    ## Definisi Method insert()
    # Kamus lokal
    # node : simpul yang akan dimasukkan
    def insert(self, node):
        self.node_counter += 1
        self.Q.append((node.bound, self.node_counter, node))

    ## Definisi Method delete()
    # Kamus lokal
    # min_idx : indeks simpul dengan bound terkecil
    # i : variabel perulangan
    # t : tuple sementara
    def delete(self):
        min_idx = 0
        for i in range(1, len(self.Q)):
            if (self.Q[i][0] < self.Q[min_idx][0]):
                min_idx = i
            elif (self.Q[i][0] == self.Q[min_idx][0] and self.Q[i][1] < self.Q[min_idx][1]):
                min_idx = i       
        t = self.Q[min_idx]
        new_Q = []
        for i in range(len(self.Q)):
            if (i != min_idx):
                new_Q.append(self.Q[i])
        self.Q = new_Q
        return t[2]

    ## Definisi Method empty()
    # Kamus lokal
    def empty(self):
        if (len(self.Q) == 0):
            return True
        else:
            return False

    ## Definisi Method hitung_bound()
    # Kamus lokal
    # node : simpul saat ini
    # costs : array of integer berisi biaya kandidat
    # k : jumlah orang yang dipilih
    # budget : batas biaya
    # n : jumlah total kandidat
    # sisa_orang : jumlah orang yang masih harus dipilih
    # tersedia : list kandidat yang masih bisa dipilih
    # i : untuk perulangan
    # estimasi_sisa : estimasi biaya untuk sisa orang
    # estimasi_total : total taksiran biaya
    def hitung_bound(self, node, costs, k, budget, n):
        sisa_orang = k - len(node.selected)
        if (sisa_orang == 0):
            return node.cost
        elif (sisa_orang < 0):
            return 9999999   
        tersedia = []
        for i in range(node.level, n):
            if (i not in node.selected):
                tersedia.append(costs[i])       
        if (len(tersedia) < sisa_orang):
            return 9999999  
        tersedia.sort()
        estimasi_sisa = sum(tersedia[:sisa_orang])
        estimasi_total = node.cost + estimasi_sisa
        if (estimasi_total > budget):
            return 9999999   
        return estimasi_total

    ## Definisi Method jalankan()
    # Kamus lokal
    # costs : array of integer berisi biaya kandidat
    # k : jumlah orang yang dipilih
    # budget : batas biaya
    # n : jumlah total kandidat
    # start_time : waktu mulai
    # summary : dictionary untuk menyimpan ringkasan
    # best_cost : biaya terbaik sementara
    # best_team : tim terbaik sementara
    # root : simpul awal
    # current : simpul yang sedang diproses
    # level : level simpul saat ini
    # new_selected : list kandidat terpilih yang baru
    # new_cost : total biaya baru
    # left_child : anak kiri (pilih kandidat)
    # sisa_kandidat : jumlah kandidat tersisa
    # butuh_orang : jumlah orang yang masih dibutuhkan
    # right_child : anak kanan (tidak pilih kandidat)
    # ada_solusi : boolean apakah solusi ditemukan
    def jalankan(self, costs, k, budget):
        # Reset state setiap kali dijalankan
        self.Q = []
        self.node_counter = 0
        n = len(costs)
        start_time = time.time()
        summary = {
            "nodes_generated": 0,
            "nodes_explored": 0,
            "nodes_pruned": 0
        }
        if (k > n):
            return [], 0, False, summary
        best_cost = budget + 1
        best_team = []
        root = Node(0, [], 0, 0)
        root.bound = self.hitung_bound(root, costs, k, budget, n)
        summary["nodes_generated"] += 1
        self.insert(root)
        while (not self.empty()):
            current = self.delete()
            summary["nodes_explored"] += 1
            if (current.bound >= best_cost):
                summary["nodes_pruned"] += 1
                continue
            level = current.level
            if (level >= n):
                if (len(current.selected) == k and current.cost < best_cost):
                    best_cost = current.cost
                    best_team = list(current.selected)
                continue
            new_selected = current.selected + [level]
            new_cost = current.cost + costs[level]
            if (new_cost <= budget and len(new_selected) <= k):
                if (len(new_selected) == k):
                    if (new_cost < best_cost):
                        best_cost = new_cost
                        best_team = list(new_selected)
                else:
                    left_child = Node(level + 1, new_selected, new_cost, 0)
                    left_child.bound = self.hitung_bound(left_child, costs, k, budget, n)
                    summary["nodes_generated"] += 1
                    if (left_child.bound < best_cost):
                        self.insert(left_child)
                    else:
                        summary["nodes_pruned"] += 1
            else:
                summary["nodes_pruned"] += 1
            sisa_kandidat = n - (level + 1)
            butuh_orang = k - len(current.selected)
            if (sisa_kandidat >= butuh_orang):
                right_child = Node(level + 1, list(current.selected), current.cost, 0)
                right_child.bound = self.hitung_bound(right_child, costs, k, budget, n)
                summary["nodes_generated"] += 1
                if (right_child.bound < best_cost):
                    self.insert(right_child)
                else:
                    summary["nodes_pruned"] += 1
            else:
                summary["nodes_pruned"] += 1
        summary["time"] = time.time() - start_time
        ada_solusi = False
        if (len(best_team) == k and best_cost <= budget):
            ada_solusi = True
        if (ada_solusi == False):
            best_cost = 0
        return best_team, best_cost, ada_solusi, summary
