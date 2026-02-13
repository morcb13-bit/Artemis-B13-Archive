import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from IPython.display import Image as IPImage

# 正五角形の座標計算
def get_pentagon(cx, cy, radius, rot_degree):
    angles = np.linspace(0, 2*np.pi, 6) + np.radians(rot_degree)
    return cx + radius * np.cos(angles), cy + radius * np.sin(angles)

plt.style.use('dark_background')
frames = []
phi = (1 + 5**0.5) / 2 # 黄金比

# 60フレームの生成
for frame in range(60):
    fig, (ax_plot, ax_text) = plt.subplots(1, 2, figsize=(10, 5), gridspec_kw={'width_ratios': [1.2, 1]})
    ax_plot.set_xlim(-4, 4); ax_plot.set_ylim(-4, 4); ax_plot.set_aspect('equal')
    ax_text.axis('off')

    if frame < 20:
        # 1. DECIMAL (10進法: 画像手前の金色の台座)
        for i in range(3):
            x, y = get_pentagon(0, 0, 2.0, i * 108 + 90)
            ax_plot.plot(x, y, color='#D4AF37', lw=2.5)
        ax_plot.text(0, -0.5, "GAP: 36 deg", color='red', ha='center', fontweight='bold')
        msg = "1. DECIMAL SYSTEM\n\nGap: 36 deg\n108*3 = 324 (Not 360)\nGeometry mismatch."

    elif frame < 40:
        # 2. QUINARY (5進法: 2n2/B13 浮遊五角形)
        for i in range(5):
            angle = i * 72
            cx, cy = 2.2 * np.cos(np.radians(angle)), 2.2 * np.sin(np.radians(angle))
            x, y = get_pentagon(cx, cy, 0.8, angle)
            ax_plot.plot(x, y, color='#9370DB', lw=1.5)
        msg = "2. QUINARY (2n2/B13)\n\nIndependent units.\nSymmetry is high,\nbut connectivity is low."

    else:
        # 3. REFLECTED FIBONACCI (画像中央のMORO螺旋)
        for i in range(frame - 35):
            scale = 3.5 * (1 / phi**(i * 0.3))
            x, y = get_pentagon(0, 0, scale, i * 22.5)
            ax_plot.plot(x, y, color=plt.cm.plasma(i/25), lw=1, alpha=0.8)
        msg = "3. REFLECTED FIBONACCI\n\nCorrection via Phi.\nSpiral fills the gap.\nMORO convergence."

    ax_text.text(0, 0.5, msg, fontsize=11, color='white', family='monospace')
    
    # 画像変換 (Matplotlib -> PIL)
    fig.canvas.draw()
    rgba_buffer = fig.canvas.buffer_rgba()
    image = Image.frombuffer('RGBA', fig.canvas.get_width_height(), rgba_buffer, 'raw', 'RGBA', 0, 1).convert('RGB')
    frames.append(image)
    plt.close(fig)

# 【修正箇所】リストの最初の画像オブジェクトに対してsaveを呼び出す
gif_name = 'moro_final.gif'
if frames:
    frames[0].save(
        gif_name, 
        save_all=True, 
        append_images=frames[1:], 
        duration=150, 
        loop=0
    )

# 表示 (タブレットでも画像として表示される)
display(IPImage(filename=gif_name))
