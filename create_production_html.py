#!/usr/bin/env python3
"""
プロダクション用HTMLファイルの作成
最小化されたCSSファイルを使用するバージョンを生成
"""

import re
import os

def create_production_html(html_file):
    """プロダクション用HTMLを作成"""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # CSSファイルのパスを最小化版に置き換え
    replacements = [
        ('css/normalize.css', 'css/minified/normalize.min.css'),
        ('css/webflow.css', 'css/minified/webflow.min.css'),
        ('css/alc-study-unlimited.webflow.css', 'css/minified/alc-study-unlimited.webflow.min.css'),
        ('css/variable-aliases.css', 'css/minified/variable-aliases.min.css')
    ]
    
    prod_content = content
    for original, minified in replacements:
        prod_content = prod_content.replace(f'href="{original}"', f'href="{minified}"')
    
    # プロダクションディレクトリに保存
    os.makedirs('production', exist_ok=True)
    
    base_name = os.path.basename(html_file)
    prod_path = f'production/{base_name}'
    
    with open(prod_path, 'w', encoding='utf-8') as f:
        f.write(prod_content)
    
    return base_name

# HTMLファイルのリスト
html_files = ['index.html', 'orientation-video.html', 'user-guide.html']

print("プロダクション用HTMLファイルの作成...")
print("=" * 50)

for html_file in html_files:
    if os.path.exists(html_file):
        created_file = create_production_html(html_file)
        print(f"✓ {created_file} -> production/{created_file}")

print("\nプロダクション用ファイルは production/ ディレクトリに作成されました")
print("\n注意: 最小化版を使用する場合は、production/内のHTMLファイルを使用してください")
