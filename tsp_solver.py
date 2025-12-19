import sys
import time

INF = float('inf')

def parse_matrix(filename):
    try:
        with open(filename, 'r', encoding='utf-8-sig') as f:
            lines = [ln.strip() for ln in f.readlines() if ln.strip()]
        if not lines:
            print('Error: file empty')
            return None
        n = len(lines)
        mat = []
        for i, line in enumerate(lines):
            parts = line.split()
            if len(parts) != n:
                print(f'Error: row {i} has {len(parts)} entries, expected {n}')
                return None
            row = []
            for p in parts:
                if p.lower() in ('inf','-1'):
                    row.append(INF)
                else:
                    try:
                        row.append(float(p))
                    except:
                        print(f"Error: invalid value '{p}'")
                        return None
            mat.append(row)
        return mat
    except FileNotFoundError:
        print(f"Error: file '{filename}' not found")
        return None

def held_karp(mat):
    n = len(mat)
    full = (1<<n) - 1
    dp = [[INF]*n for _ in range(1<<n)]
    parent = [[-1]*n for _ in range(1<<n)]
    dp[1<<0][0] = 0.0
    for mask in range(1<<n):
        for u in range(n):
            if not (mask & (1<<u)): continue
            du = dp[mask][u]
            if du == INF: continue
            for v in range(n):
                if mask & (1<<v): continue
                w = mat[u][v]
                if w == INF: continue
                nm = mask | (1<<v)
                nd = du + w
                if nd < dp[nm][v]:
                    dp[nm][v] = nd
                    parent[nm][v] = u
    best = INF
    last = -1
    for u in range(n):
        if dp[full][u] == INF: continue
        back = mat[u][0]
        if back == INF: continue
        cost = dp[full][u] + back
        if cost < best:
            best = cost
            last = u
    if best == INF:
        return None, INF
    path = []
    mask = full
    cur = last
    while cur != -1:
        path.append(cur)
        prev = parent[mask][cur]
        mask ^= (1<<cur)
        cur = prev
    path.reverse()
    tour = path + [0]
    total = 0.0
    for i in range(len(tour)-1):
        total += mat[tour[i]][tour[i+1]]
    return tour, total


def nearest_neighbor(mat, start=0):
    n = len(mat)
    tour = [start]
    visited = {start}
    cur = start
    while len(tour) < n:
        best = INF
        nxt = -1
        for v in range(n):
            if v in visited: continue
            w = mat[cur][v]
            if w == INF: continue
            if w < best:
                best = w
                nxt = v
        if nxt == -1:
            return None
        tour.append(nxt)
        visited.add(nxt)
        cur = nxt
    tour.append(start)
    return tour


def two_opt(tour, mat):
    improved = True
    n = len(tour)
    while improved:
        improved = False
        for i in range(1, n-2):
            for k in range(i+1, n-1):
                a = tour[i-1]
                b = tour[i]
                c = tour[k]
                d = tour[k+1]
                w1 = mat[a][b]
                w2 = mat[c][d]
                w3 = mat[a][c]
                w4 = mat[b][d]
                if w1 == INF or w2 == INF or w3 == INF or w4 == INF:
                    continue
                delta = (w3 + w4) - (w1 + w2)
                if delta < -1e-9:
                    tour[i:k+1] = reversed(tour[i:k+1])
                    improved = True
        if improved:
            continue
    return tour


def heuristic_tsp(mat, time_limit=5.0):
    n = len(mat)
    best_tour = None
    best_cost = INF
    start_time = time.time()
    starts = list(range(n))
    if n > 50:
        starts = starts[:10]
    for s in starts:
        cand = nearest_neighbor(mat, s)
        if cand is None: continue
        cand = two_opt(cand, mat)
        total = 0.0
        ok = True
        for i in range(len(cand)-1):
            w = mat[cand[i]][cand[i+1]]
            if w == INF:
                ok = False
                break
            total += w
        if not ok: continue
        if total < best_cost:
            best_cost = total
            best_tour = cand[:]
        if time.time() - start_time > time_limit:
            break
    if best_tour is None:
        return None, INF
    return best_tour, best_cost


def solve(filename='problem.txt', exact_threshold=12):
    mat = parse_matrix(filename)
    if mat is None:
        return
    n = len(mat)
    names = [chr(ord('A')+i) for i in range(n)]
    print('\nMatrix loaded, n =', n)
    if n <= exact_threshold:
        tour, cost = held_karp(mat)
        if tour is not None:
            print('\nExact Held-Karp result:')
            print(' -> '.join(names[i] for i in tour), f'Cost = {cost:.2f}')
            print('Breakdown:')
            for i in range(len(tour)-1):
                a = tour[i]
                b = tour[i+1]
                print(f'  {names[a]} -> {names[b]}: {mat[a][b]:.2f}')
            return
    tour, cost = heuristic_tsp(mat, time_limit=5.0)
    if tour is None:
        print('No feasible tour found')
        return
    print('\nHeuristic result (NN + 2-opt):')
    print(' -> '.join(names[i] for i in tour), f'Cost = {cost:.2f}')
    print('Breakdown:')
    for i in range(len(tour)-1):
        a = tour[i]
        b = tour[i+1]
        print(f'  {names[a]} -> {names[b]}: {mat[a][b]:.2f}')

if __name__ == '__main__':
    solve('problem.txt')
