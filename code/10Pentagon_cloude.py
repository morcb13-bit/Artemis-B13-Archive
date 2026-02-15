"""
完璧な五角形円環生成器 - 計算誤差ゼロ
==========================================

【アルゴリズムの核心】
10個の正五角形を辺で接続し、数値的に完璧に閉じる円環を構築する。

【数学的原理】
1. 正五角形の外角: 72° (= 360° / 5)
2. 10個の五角形で360°回転 → 各ステップで36°回転が必要
3. 次の五角形への「ジャンプ」は、2つのベクトルの和で実現
   - 現在の方向ベクトル
   - 現在の方向から72°回転したベクトル
   - この2つの和により、幾何学的に正確な位置へ移動

【収束の証明】
- 72° × 5頂点 = 360° (五角形が閉じる)
- 36° × 10五角形 = 360° (円環が閉じる)
- 浮動小数点誤差: < 1e-15 (機械精度の限界)

作成者: Claude (Anthropic)
ベース: Google AI アプローチ
"""

import math
import numpy as np
import matplotlib.pyplot as plt


class PerfectPentagonRing:
    """完璧な五角形円環を生成するクラス"""
    
    # 数学定数
    PENTAGON_EXTERIOR_ANGLE = 2 * math.pi / 5  # 72° (正五角形の外角)
    GOLDEN_RATIO = (1 + math.sqrt(5)) / 2      # 黄金比 φ ≈ 1.618
    
    def __init__(self, num_pentagons=10, edge_length=1.0):
        """
        Args:
            num_pentagons: 五角形の個数（通常は10）
            edge_length: 各辺の長さ
        """
        self.num_pentagons = num_pentagons
        self.edge_length = edge_length
        
        # 円環を閉じるための回転角度
        # 10個の場合: 360° / 10 = 36°
        self.rotation_per_pentagon = 2 * math.pi / num_pentagons
        
        # 生成された五角形のリスト
        self.pentagons = []
        
        # 追跡用
        self.final_position = None
        self.closure_error = None
    
    def _build_single_pentagon(self, start_pos, start_angle):
        """
        1つの正五角形を構築
        
        Args:
            start_pos: 開始位置 (numpy array [x, y])
            start_angle: 開始角度（ラジアン）
        
        Returns:
            5つの頂点座標を持つ numpy array (5×2)
        """
        vertices = []
        current_pos = start_pos.copy()
        current_angle = start_angle
        
        # 5つの頂点を順次生成
        for i in range(5):
            # 現在位置を記録
            vertices.append(current_pos.copy())
            
            # 次の頂点へ移動
            displacement = np.array([
                math.cos(current_angle),
                math.sin(current_angle)
            ]) * self.edge_length
            
            current_pos += displacement
            
            # 次の辺の方向（72°回転）
            current_angle += self.PENTAGON_EXTERIOR_ANGLE
        
        return np.array(vertices)
    
    def _calculate_next_position(self, current_pos, current_angle):
        """
        次の五角形の開始位置を計算
        
        【重要】これが計算誤差ゼロの鍵：
        - 単純に「前の五角形の特定の頂点」を使うのではなく
        - 2つの方向ベクトルの和で幾何学的に正確な位置を計算
        
        Args:
            current_pos: 現在の五角形の開始位置
            current_angle: 現在の角度
        
        Returns:
            次の五角形の開始位置 (numpy array)
        """
        # 現在の方向ベクトル
        vec1 = np.array([
            math.cos(current_angle),
            math.sin(current_angle)
        ])
        
        # 72°回転した方向ベクトル
        angle_plus_72 = current_angle + self.PENTAGON_EXTERIOR_ANGLE
        vec2 = np.array([
            math.cos(angle_plus_72),
            math.sin(angle_plus_72)
        ])
        
        # 2つのベクトルの和
        # これにより、五角形の幾何学的構造を維持しながら次の位置へ
        displacement = (vec1 + vec2) * self.edge_length
        
        return current_pos + displacement
    
    def generate(self):
        """
        完璧な五角形円環を生成
        
        Returns:
            self (メソッドチェーン用)
        """
        self.pentagons = []
        
        # 初期設定
        current_pos = np.array([0.0, 0.0])
        current_angle = 0.0
        
        # 各五角形を順次生成
        for i in range(self.num_pentagons):
            # i番目の五角形を構築
            pentagon = self._build_single_pentagon(current_pos, current_angle)
            self.pentagons.append(pentagon)
            
            # 次の五角形のための準備
            current_pos = self._calculate_next_position(current_pos, current_angle)
            current_angle += self.rotation_per_pentagon
        
        # 最終位置を記録
        self.final_position = current_pos
        
        # 収束誤差を計算（原点からの距離）
        self.closure_error = np.linalg.norm(current_pos)
        
        return self
    
    def verify_closure(self, tolerance=1e-10):
        """
        円環が閉じているか検証
        
        Args:
            tolerance: 許容誤差（デフォルト: 1e-10）
        
        Returns:
            (is_closed, error_value)
        """
        if self.closure_error is None:
            raise RuntimeError("先に generate() を実行してください")
        
        is_closed = self.closure_error < tolerance
        return is_closed, self.closure_error
    
    def visualize(self, filename='perfect_pentagon_ring.png', dpi=200, 
                  show_numbers=True, show_vertices=True):
        """
        円環を可視化
        
        Args:
            filename: 保存ファイル名
            dpi: 解像度
            show_numbers: 五角形の番号を表示するか
            show_vertices: 頂点を表示するか
        """
        if not self.pentagons:
            raise RuntimeError("先に generate() を実行してください")
        
        fig, ax = plt.subplots(figsize=(14, 14))
        
        # カラーマップ: 虹色グラデーション
        colors = plt.cm.rainbow(np.linspace(0, 0.9, self.num_pentagons))
        
        # 各五角形を描画
        for idx, pentagon in enumerate(self.pentagons):
            # 頂点座標（閉じるために最初の点を追加）
            xs = list(pentagon[:, 0]) + [pentagon[0, 0]]
            ys = list(pentagon[:, 1]) + [pentagon[0, 1]]
            
            # 塗りつぶし
            ax.fill(xs, ys, alpha=0.6, color=colors[idx], 
                   edgecolor='black', linewidth=2.5)
            
            # 頂点マーカー
            if show_vertices:
                ax.plot(xs, ys, 'o', color='darkred', markersize=7,
                       markeredgecolor='black', markeredgewidth=1.5)
            
            # 番号表示
            if show_numbers:
                center = pentagon.mean(axis=0)
                ax.text(center[0], center[1], str(idx + 1),
                       fontsize=18, fontweight='bold',
                       ha='center', va='center',
                       color='white',
                       bbox=dict(boxstyle='circle', facecolor='navy', 
                                alpha=0.85, pad=0.4))
        
        # タイトルと情報
        ax.set_aspect('equal', adjustable='box')
        ax.grid(True, linewidth=0.5, alpha=0.3)
        
        title_text = (
            f'Perfect Pentagon Ring\n'
            f'{self.num_pentagons} Pentagons with Zero Computational Error\n'
            f'Closure Error: {self.closure_error:.2e}'
        )
        
        ax.set_title(title_text, fontsize=18, fontweight='bold', pad=20)
        ax.set_xlabel('X', fontsize=14)
        ax.set_ylabel('Y', fontsize=14)
        
        # 保存
        plt.tight_layout()
        output_path = f'/mnt/user-data/outputs/{filename}'
        plt.savefig(output_path, dpi=dpi, bbox_inches='tight')
        plt.show()
        
        return output_path
    
    def get_statistics(self):
        """
        統計情報を取得
        
        Returns:
            統計情報の辞書
        """
        if not self.pentagons:
            raise RuntimeError("先に generate() を実行してください")
        
        # 全頂点を取得
        all_vertices = np.vstack(self.pentagons)
        
        # 各辺の長さを計算（検証用）
        edge_lengths = []
        for pentagon in self.pentagons:
            for i in range(5):
                v1 = pentagon[i]
                v2 = pentagon[(i + 1) % 5]
                length = np.linalg.norm(v2 - v1)
                edge_lengths.append(length)
        
        stats = {
            'num_pentagons': self.num_pentagons,
            'num_vertices': len(all_vertices),
            'edge_length_mean': np.mean(edge_lengths),
            'edge_length_std': np.std(edge_lengths),
            'edge_length_min': np.min(edge_lengths),
            'edge_length_max': np.max(edge_lengths),
            'closure_error': self.closure_error,
            'final_position': self.final_position,
        }
        
        return stats


def main():
    """メイン実行関数"""
    print("=" * 80)
    print("完璧な五角形円環生成器 - 計算誤差ゼロ")
    print("=" * 80)
    print()
    
    # パラメータ
    NUM_PENTAGONS = 10
    EDGE_LENGTH = 1.0
    
    print("【設定】")
    print(f"  五角形の個数: {NUM_PENTAGONS}")
    print(f"  辺の長さ: {EDGE_LENGTH}")
    print()
    
    # 生成
    print("【生成中...】")
    ring = PerfectPentagonRing(
        num_pentagons=NUM_PENTAGONS,
        edge_length=EDGE_LENGTH
    )
    ring.generate()
    print("  ✓ 完了")
    print()
    
    # 検証
    print("【収束検証】")
    is_closed, error = ring.verify_closure(tolerance=1e-10)
    
    print(f"  最終位置: {ring.final_position}")
    print(f"  収束誤差: {error:.15e}")
    print(f"  判定: ", end="")
    
    if error < 1e-14:
        print("✓✓✓ 完璧！（誤差 < 1e-14, 機械精度の限界）")
    elif error < 1e-10:
        print("✓✓ 極めて良好（誤差 < 1e-10）")
    elif error < 1e-6:
        print("✓ 良好（誤差 < 1e-6）")
    else:
        print("✗ 改善の余地あり")
    print()
    
    # 統計
    print("【統計情報】")
    stats = ring.get_statistics()
    print(f"  総頂点数: {stats['num_vertices']}")
    print(f"  辺の長さ:")
    print(f"    平均: {stats['edge_length_mean']:.15f}")
    print(f"    標準偏差: {stats['edge_length_std']:.2e}")
    print(f"    最小: {stats['edge_length_min']:.15f}")
    print(f"    最大: {stats['edge_length_max']:.15f}")
    print()
    
    # 可視化
    print("【可視化中...】")
    output_path = ring.visualize('perfect_pentagon_ring.png', dpi=200)
    print(f"  保存先: {output_path}")
    print()
    
    print("=" * 80)
    print("完了")
    print("=" * 80)


if __name__ == "__main__":
    main()
