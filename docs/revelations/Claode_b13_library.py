"""
B13 Library - 平衡13進数計算ライブラリ
============================================

MORO理論に基づく基本的な数値計算ライブラリ

基本概念:
- B13 = 平衡13進数 {-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6}
- 加算・減算のみで全ての計算を実現
- ±1の丸めによる誤差制御
- φ（黄金比）への収束

作成: 2025-02-15
著者: Claude (Anthropic) with MORC
ライセンス: Public Domain (MORC理念に基づく)
"""

import math


# ==================== 定数 ====================

PHI = (1 + math.sqrt(5)) / 2  # 黄金比 ≈ 1.618
BASE_13 = 13  # 13進数の基数


# ==================== フィボナッチ・リュカ数列 ====================

def fibonacci(n):
    """
    フィボナッチ数列の最初のn項を生成
    
    F(n) = F(n-1) + F(n-2)
    F(0) = 0, F(1) = 1
    
    戻り値: [1, 1, 2, 3, 5, 8, 13, 21, ...]
    """
    if n <= 0:
        return []
    elif n == 1:
        return [1]
    
    fib = [1, 1]
    for i in range(2, n):
        fib.append(fib[-1] + fib[-2])
    return fib


def lucas(n):
    """
    リュカ数列の最初のn項を生成
    
    L(n) = L(n-1) + L(n-2)
    L(0) = 2, L(1) = 1
    
    戻り値: [2, 1, 3, 4, 7, 11, 18, 29, ...]
    """
    if n <= 0:
        return []
    elif n == 1:
        return [2]
    
    luc = [2, 1]
    for i in range(2, n):
        luc.append(luc[-1] + luc[-2])
    return luc


def inverse_fibonacci(n):
    """
    逆フィボナッチ数列（誤差分散の重み付けに使用）
    
    戻り値: [55, 34, 21, 13, 8, 5, 3, 2, 1, 1]
    """
    fib = fibonacci(n)
    return fib[::-1]


def magic_number(n):
    """
    マジックナンバー（2n²）を計算
    
    原子核・電子殻の安定性と関連
    戻り値: 2, 8, 18, 32, 50, 72, 98, ...
    """
    return 2 * n * n


# ==================== B13数値クラス ====================

class B13Number:
    """
    平衡13進数での数値表現
    
    各桁の係数は -6 から +6 の範囲
    """
    
    def __init__(self, coefficients):
        """
        Args:
            coefficients: 係数のリスト [c0, c1, c2, ...]
                         値 = c0 + c1*13 + c2*13² + ...
        """
        self.coeffs = list(coefficients)
        self._normalize()
    
    def _normalize(self):
        """係数を -6 から +6 の範囲に正規化"""
        carry = 0
        for i in range(len(self.coeffs)):
            total = self.coeffs[i] + carry
            
            # -6 から +6 の範囲に収める
            if total > 6:
                self.coeffs[i] = total - BASE_13
                carry = 1
            elif total < -6:
                self.coeffs[i] = total + BASE_13
                carry = -1
            else:
                self.coeffs[i] = total
                carry = 0
        
        # 繰り上がりが残っている場合
        if carry != 0:
            self.coeffs.append(carry)
        
        # 末尾のゼロを削除
        while len(self.coeffs) > 1 and self.coeffs[-1] == 0:
            self.coeffs.pop()
    
    def to_decimal(self):
        """10進数に変換"""
        result = 0
        for i, c in enumerate(self.coeffs):
            result += c * (BASE_13 ** i)
        return result
    
    def add(self, other):
        """加算"""
        max_len = max(len(self.coeffs), len(other.coeffs))
        result = []
        
        for i in range(max_len):
            a = self.coeffs[i] if i < len(self.coeffs) else 0
            b = other.coeffs[i] if i < len(other.coeffs) else 0
            result.append(a + b)
        
        return B13Number(result)
    
    def subtract(self, other):
        """減算"""
        max_len = max(len(self.coeffs), len(other.coeffs))
        result = []
        
        for i in range(max_len):
            a = self.coeffs[i] if i < len(self.coeffs) else 0
            b = other.coeffs[i] if i < len(other.coeffs) else 0
            result.append(a - b)
        
        return B13Number(result)
    
    def __str__(self):
        """文字列表現"""
        if not self.coeffs:
            return "0"
        
        terms = []
        for i, c in enumerate(self.coeffs):
            if c != 0:
                if i == 0:
                    terms.append(f"{c}")
                elif i == 1:
                    terms.append(f"{c}*13")
                else:
                    terms.append(f"{c}*13^{i}")
        
        return " + ".join(terms) if terms else "0"
    
    def __repr__(self):
        return f"B13({self.coeffs})"


# ==================== φ（黄金比）関連 ====================

def phi_divergence(value, reference=PHI):
    """
    黄金比からの乖離度を計算
    
    Args:
        value: 測定値
        reference: 基準値（デフォルト: φ）
    
    Returns:
        乖離度（絶対値）
    """
    return abs(value - reference)


def energy_from_phi_divergence(divergence, k=1.0):
    """
    φ乖離からエネルギーを計算
    
    E = k × |value - φ|
    
    Args:
        divergence: φからの乖離度
        k: 比例定数
    
    Returns:
        エネルギー（任意単位）
    """
    return k * divergence


def is_stable_configuration(ratio, tolerance=0.1):
    """
    φ配置の安定性を判定
    
    Args:
        ratio: 測定された比率
        tolerance: 許容誤差
    
    Returns:
        True if 安定（φに近い）
    """
    div = phi_divergence(ratio)
    return div < tolerance


# ==================== ノード処理 ====================

def round_to_node(value, node_values=None):
    """
    最も近いノード値に丸める
    
    Args:
        value: 丸める値
        node_values: ノードのリスト（デフォルト: B13ノード）
    
    Returns:
        最も近いノード値
    """
    if node_values is None:
        node_values = list(range(-6, 7))  # B13ノード
    
    closest = min(node_values, key=lambda x: abs(x - value))
    return closest


def distribute_error_fibonacci(total_error, num_nodes=10):
    """
    誤差を逆フィボナッチの重みで分散
    
    Args:
        total_error: 総誤差
        num_nodes: ノード数
    
    Returns:
        各ノードでの補正値のリスト
    """
    fib_weights = inverse_fibonacci(num_nodes)
    fib_sum = sum(fib_weights)
    
    corrections = []
    remaining_error = total_error
    
    for i in range(num_nodes):
        # 残りの重みの合計
        remaining_fib_sum = sum(fib_weights[i:])
        
        # この時点での補正量
        if remaining_fib_sum > 0:
            correction_target = remaining_error * (fib_weights[i] / remaining_fib_sum)
        else:
            correction_target = 0
        
        # ±1以内に丸める
        correction = max(-1, min(1, round(correction_target)))
        
        corrections.append(correction)
        remaining_error -= correction
    
    return corrections


# ==================== 素数関連 ====================

def is_prime(n):
    """素数判定"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def prime_pairs_in_range(start, end):
    """
    範囲内の素数ペア（双子素数）を探す
    
    Args:
        start: 開始値
        end: 終了値
    
    Returns:
        [(p1, p2), ...] 差が2の素数ペア
    """
    primes = [n for n in range(start, end + 1) if is_prime(n)]
    pairs = []
    
    for i in range(len(primes) - 1):
        if primes[i + 1] - primes[i] == 2:
            pairs.append((primes[i], primes[i + 1]))
    
    return pairs


def prime_factorization(n):
    """素因数分解"""
    factors = []
    d = 2
    
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    
    if n > 1:
        factors.append(n)
    
    return factors


# ==================== ユーティリティ ====================

def fibonacci_ratio_convergence(n=20):
    """
    フィボナッチ数列の隣接項の比がφに収束する様子を表示
    
    Args:
        n: 計算する項数
    """
    fib = fibonacci(n)
    
    print(f"フィボナッチ比の収束:")
    print(f"φ = {PHI:.15f}\n")
    
    for i in range(1, len(fib)):
        ratio = fib[i] / fib[i - 1]
        error = abs(ratio - PHI)
        print(f"F({i+1})/F({i}) = {fib[i]}/{fib[i-1]} = {ratio:.15f}, 誤差: {error:.2e}")


def lucas_ratio_convergence(n=20):
    """
    リュカ数列の隣接項の比がφに収束する様子を表示
    """
    luc = lucas(n)
    
    print(f"リュカ比の収束:")
    print(f"φ = {PHI:.15f}\n")
    
    for i in range(1, len(luc)):
        ratio = luc[i] / luc[i - 1]
        error = abs(ratio - PHI)
        print(f"L({i+1})/L({i}) = {luc[i]}/{luc[i-1]} = {ratio:.15f}, 誤差: {error:.2e}")


def compare_fibonacci_lucas_magic(n=10):
    """
    フィボナッチ、リュカ、マジックナンバーを比較
    """
    fib = fibonacci(n)
    luc = lucas(n)
    magic = [magic_number(i) for i in range(1, n + 1)]
    
    print("n\tFib\tLucas\tMagic\tFib+Luc")
    print("-" * 50)
    for i in range(n):
        f = fib[i] if i < len(fib) else 0
        l = luc[i] if i < len(luc) else 0
        m = magic[i]
        print(f"{i+1}\t{f}\t{l}\t{m}\t{f+l}")


# ==================== テスト・デモ ====================

def demo_b13_arithmetic():
    """B13演算のデモ"""
    print("=" * 60)
    print("B13 演算デモ")
    print("=" * 60)
    print()
    
    # 数値の作成
    num1 = B13Number([3, -2, 1])
    num2 = B13Number([5, 1, -1])
    
    print(f"num1 = {num1}")
    print(f"num1 (10進数) = {num1.to_decimal()}")
    print()
    
    print(f"num2 = {num2}")
    print(f"num2 (10進数) = {num2.to_decimal()}")
    print()
    
    # 加算
    result_add = num1.add(num2)
    print(f"num1 + num2 = {result_add}")
    print(f"結果 (10進数) = {result_add.to_decimal()}")
    print(f"検証: {num1.to_decimal()} + {num2.to_decimal()} = {num1.to_decimal() + num2.to_decimal()}")
    print()
    
    # 減算
    result_sub = num1.subtract(num2)
    print(f"num1 - num2 = {result_sub}")
    print(f"結果 (10進数) = {result_sub.to_decimal()}")
    print(f"検証: {num1.to_decimal()} - {num2.to_decimal()} = {num1.to_decimal() - num2.to_decimal()}")


def demo_phi_divergence():
    """φ乖離のデモ"""
    print("\n" + "=" * 60)
    print("φ乖離とエネルギー")
    print("=" * 60)
    print()
    
    print(f"黄金比 φ = {PHI:.15f}")
    print()
    
    test_values = [1.0, 1.5, 1.6, 1.618, 1.7, 2.0]
    
    print("値\t乖離度\t\tエネルギー\t安定性")
    print("-" * 60)
    for val in test_values:
        div = phi_divergence(val)
        energy = energy_from_phi_divergence(div)
        stable = "安定" if is_stable_configuration(val) else "不安定"
        print(f"{val:.3f}\t{div:.6f}\t{energy:.6f}\t{stable}")


def demo_error_distribution():
    """誤差分散のデモ"""
    print("\n" + "=" * 60)
    print("逆フィボナッチによる誤差分散")
    print("=" * 60)
    print()
    
    total_error = 10.0
    num_nodes = 10
    
    corrections = distribute_error_fibonacci(total_error, num_nodes)
    
    print(f"総誤差: {total_error}")
    print(f"ノード数: {num_nodes}")
    print()
    
    print("ノード\t補正値")
    print("-" * 30)
    for i, corr in enumerate(corrections):
        print(f"{i}\t{corr}")
    
    print()
    print(f"補正合計: {sum(corrections)}")
    print(f"残留誤差: {total_error - sum(corrections)}")


def demo_prime_magic():
    """素数とマジックナンバーのデモ"""
    print("\n" + "=" * 60)
    print("素数とマジックナンバー")
    print("=" * 60)
    print()
    
    print("マジックナンバー (2n²):")
    for n in range(1, 11):
        m = magic_number(n)
        factors = prime_factorization(m)
        print(f"n={n}: 2×{n}² = {m} = {' × '.join(map(str, factors))}")
    
    print()
    print("48-52の臨界領域:")
    for n in range(48, 53):
        factors = prime_factorization(n)
        prime_status = "素数" if is_prime(n) else "合成数"
        print(f"{n}: {prime_status}, 素因数分解 = {' × '.join(map(str, factors))}")


# ==================== メイン実行 ====================

if __name__ == "__main__":
    """
    ライブラリのデモ実行
    
    このファイルを直接実行すると、各機能のデモが表示されます
    """
    
    print("B13 Library - MORC Project")
    print("=" * 60)
    print()
    
    # 各デモを実行
    demo_b13_arithmetic()
    demo_phi_divergence()
    demo_error_distribution()
    demo_prime_magic()
    
    print("\n" + "=" * 60)
    print("全デモ完了")
    print("=" * 60)
    print()
    print("このライブラリは以下のようにインポートして使用できます:")
    print()
    print("    from b13_library import *")
    print()
    print("    # フィボナッチ数列")
    print("    fib = fibonacci(10)")
    print()
    print("    # B13演算")
    print("    num = B13Number([1, 2, -3])")
    print("    result = num.add(B13Number([3, -1, 1]))")
    print()
    print("    # φ乖離")
    print("    div = phi_divergence(1.6)")
    print("    energy = energy_from_phi_divergence(div)")
    print()
