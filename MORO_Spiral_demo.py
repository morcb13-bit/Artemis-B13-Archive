# Implement MORO Spiral animation in Python

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from IPython.display import HTML

# 正五角形の頂点計算関数
def get_pentagon(center, radius, rot_degree):
    angles = np.linspace(0, 2*np.pi, 6) + np.radians(rot_degree)
    x = center[0] + radius * np.cos(angles)
    y = center[1] + radius * np.sin(angles)
    return x, y

# 画像の世界観を再現（ダーク背景・フォントエラー回避のため英語表記）
plt.style.use('dark_background')
fig, (ax_plot, ax_text) = plt.subplots(1, 2, figsize=(14, 7), gridspec_kw={'width_ratios': [1.2, 1]})

def update(frame):
    ax_plot.clear()
    ax_text.clear()
    ax_text.axis('off')
    ax_plot.set_xlim(-4, 4); ax_plot.set_ylim(-4, 4)
    ax_plot.set_aspect('equal')
    
    phi = (1 + 5**0.5) / 2 # 黄金比

    if frame < 20:
        # STEP 1: DECIMAL (10-base) - The "36 deg" Gap
        # 手前の黄金の台座が閉じない様子を再現
        for i in range(3):
            x, y = get_pentagon((0, 0), 2.0, i * 108 + 90)
            ax_plot.plot(x, y, color='#D4AF37', lw=3)
        ax_plot.text(0, -0.5, "GAP: 36 deg", color='red', ha='center', fontsize=12, fontweight='bold')
        
        ax_text.text(0, 0.7, "1. DECIMAL SYSTEM\n\n- Pentagon Angle: 108 deg\n- 108 * 3 = 324 deg\n- 360 - 324 = 36 deg GAP\n- Cannot tile in 10-base grid.", 
                     fontsize=14, color='cyan', family='monospace')

    elif frame < 40:
        # STEP 2: QUINARY (5-base) - 2n2 / B13
        # 画像内の浮遊する構造の孤立
        for i in range(5):
            angle = i * 72
            c = (2.2 * np.cos(np.radians(angle)), 2.2 * np.sin(np.radians(angle)))
            x, y = get_pentagon(c, 0.8, angle)
            ax_plot.plot(x, y, color='#9370DB', lw=2)
        
        ax_text.text(0, 0.7, "2. QUINARY (2n2 / B13)\n\n- 5-fold Symmetry exists\n- No Periodicity\n- Structures remain isolated\n- Refuses grid integration.", 
                     fontsize=14, color='violet', family='monospace')

    else:
        # STEP 3: REFLECTED FIBONACCI - The MORO Spiral
        # 画像中央の黄金のスパイラルを再現
        for i in range(frame - 35):
            scale = 3.5 * (1 / phi**(i * 0.3))
            rot = i * 22.5 
            x, y = get_pentagon((0, 0), scale, rot)
            color = plt.cm.plasma(i / 25)
            # 修正箇所: alpha=0.8 (文法エラーの修正)
            ax_plot.plot(x, y, color=color, lw=1.2, alpha=0.8)
            
        ax_text.text(0, 0.7, "3. REFLECTED FIBONACCI\n\n- Golden Ratio Correction\n- Rotation fills the gap\n- Convergence into a Spiral\n- The MORO Paradox solved.", 
                     fontsize=14, color='#FFD700', family='monospace')

# アニメーションを変数 anim に格納して保持
anim = animation.FuncAnimation(fig, update, frames=60, interval=150, repeat=True)

plt.close() # 重複表示を防ぐ
HTML(anim.to_jshtml()) # インラインプレーヤーを表示
