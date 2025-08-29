#!/usr/bin/env python3
"""
CSS最小化スクリプト
プロダクション用に最適化されたCSSファイルを生成
"""

import re
import os

def minify_css(css_content):
    """CSSを最小化"""
    # コメントを削除（ただし、重要なライセンス情報は保持）
    css_content = re.sub(r'/\*(?![!]).*?\*/', '', css_content, flags=re.DOTALL)
    
    # 改行とタブを削除
    css_content = re.sub(r'\s+', ' ', css_content)
    
    # 不要なスペースを削除
    css_content = re.sub(r'\s*([{}:;,>+~])\s*', r'\1', css_content)
    
    # セミコロンの前の最後のスペースを削除
    css_content = re.sub(r';\s*}', '}', css_content)
    
    # 0pxを0に
    css_content = re.sub(r'([: ])0px', r'\g<1>0', css_content)
    css_content = re.sub(r'([: ])0em', r'\g<1>0', css_content)
    css_content = re.sub(r'([: ])0rem', r'\g<1>0', css_content)
    
    # カラーコードの短縮（#FFFFFFを#FFFに）
    css_content = re.sub(r'#([0-9a-fA-F])\1([0-9a-fA-F])\2([0-9a-fA-F])\3', r'#\1\2\3', css_content)
    
    return css_content.strip()

def process_css_files():
    """CSSファイルを処理"""
    css_files = [
        'css/normalize.css',
        'css/webflow.css',
        'css/alc-study-unlimited.webflow.css',
        'css/variable-aliases.css'
    ]
    
    # minifiedディレクトリを作成
    os.makedirs('css/minified', exist_ok=True)
    
    total_original = 0
    total_minified = 0
    
    for css_file in css_files:
        if not os.path.exists(css_file):
            continue
            
        with open(css_file, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # ファイルサイズ（オリジナル）
        original_size = len(original_content.encode('utf-8'))
        total_original += original_size
        
        # 最小化
        minified_content = minify_css(original_content)
        
        # ファイルサイズ（最小化後）
        minified_size = len(minified_content.encode('utf-8'))
        total_minified += minified_size
        
        # 保存
        base_name = os.path.basename(css_file)
        min_name = base_name.replace('.css', '.min.css')
        min_path = f'css/minified/{min_name}'
        
        with open(min_path, 'w', encoding='utf-8') as f:
            f.write(minified_content)
        
        # 圧縮率を計算
        reduction = (1 - minified_size / original_size) * 100
        
        print(f"{base_name}:")
        print(f"  オリジナル: {original_size:,} bytes")
        print(f"  最小化後: {minified_size:,} bytes")
        print(f"  削減率: {reduction:.1f}%")
        print()
    
    # 全体の統計
    total_reduction = (1 - total_minified / total_original) * 100
    print("=" * 50)
    print("合計:")
    print(f"  オリジナル: {total_original:,} bytes ({total_original/1024:.1f} KB)")
    print(f"  最小化後: {total_minified:,} bytes ({total_minified/1024:.1f} KB)")
    print(f"  削減率: {total_reduction:.1f}%")
    print(f"  削減量: {(total_original-total_minified)/1024:.1f} KB")

# 実行
print("CSS最小化処理を開始...")
print("=" * 50)
process_css_files()
print("\n最小化されたファイルは css/minified/ に保存されました")
