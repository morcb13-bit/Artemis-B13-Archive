# pentagon_loop_by_edge3.py
# Pydroid OK (matplotlib必要)
# 出力: pentagon_edge3_loop.png

import math
import matplotlib.pyplot as plt


def rot(v, ang):
    x, y = v
    c, s = math.cos(ang), math.sin(ang)
    return (c * x - s * y, s * x + c * y)

def add(a, b): return (a[0] + b[0], a[1] + b[1])
def sub(a, b): return (a[0] - b[0], a[1] - b[1])
def norm(a): return math.hypot(a[0], a[1])

def build_pentagon_from_edge(p0, v01, turn_sign=+1):
    """
    p0: 頂点0
    v01: 頂点0->頂点1 ベクトル（長さ=辺長）
    turn_sign: +1 で CCW に 72°ずつ回す、-1 で CW
    戻り値: 頂点 v0..v4 (5点)
    """
    ext = turn_sign * (2 * math.pi / 5)  # 72°
    pts = [p0]
    v = v01
    p = p0
    for _ in range(4):  # v1..v4
        p = add(p, v)
        pts.append(p)
        v = rot(v, ext)
    return pts

def plot_polys(polys, fname, title):
    fig, ax = plt.subplots(figsize=(7, 7))
    for poly in polys:
        xs = [p[0] for p in poly] + [poly[0][0]]
        ys = [p[1] for p in poly] + [poly[0][1]]
        ax.plot(xs, ys, linewidth=2)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, linewidth=0.5)
    ax.set_title(title)
    plt.tight_layout()
    plt.savefig(fname, dpi=220)
    plt.show()
    print("Saved:", fname)

def main():
    # 初期設定
    s = 3.0
    v01 = (s, 0.0)     # 最初の辺は右向き
    p0 = (0.0, 0.0)     # 最初の頂点0
    turn_sign = +1      # 必要なら -1 に

    polys = []

    # 1個目
    poly = build_pentagon_from_edge(p0, v01, turn_sign=turn_sign)
    polys.append(poly)

    # 「3個目の辺」= v2 -> v3
    e3_start = poly[2]
    e3_end   = poly[3]

    # 以降：その終点(v3)から始めて、終点->始点 へ戻る辺を1本目にする
    for _ in range(9):  # 合計10個
        p0_next = e3_end
        v01_next = sub(e3_start, e3_end)  # v3 -> v2 （戻る）

        poly = build_pentagon_from_edge(p0_next, v01_next, turn_sign=turn_sign)
        polys.append(poly)

        # 次のために更新
        e3_start = poly[2]
        e3_end   = poly[3]

    closure = norm(sub(polys[-1][0], polys[0][0]))
    print("closure_error(|last.v0 - first.v0|) =", closure)

    plot_polys(polys, "pentagon_edge3_loop.png",
               f"Pentagon loop by returning along 3rd edge (steps=10), closure={closure:.6g}")

if __name__ == "__main__":
    main()
