#!/usr/bin/env python3
"""
HTMLファイルにvariable-aliases.cssのリンクを追加
メインCSSファイルの後に読み込むことで、エイリアスが利用可能になる
"""

import re

def add_alias_css_link(html_file):
    """HTMLファイルにエイリアスCSSのリンクを追加"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 既にvariable-aliases.cssが含まれているか確認
    if 'variable-aliases.css' in content:
        print(f"  {html_file}: Already contains variable-aliases.css")
        return False
    
    # alc-study-unlimited.webflow.cssの後にエイリアスCSSを追加
    pattern = r'(<link href="css/alc-study-unlimited\.webflow\.css" rel="stylesheet" type="text/css">)'
    replacement = r'\1\n  <link href="css/variable-aliases.css" rel="stylesheet" type="text/css">'
    
    new_content = re.sub(pattern, replacement, content)
    
    if new_content != content:
        # バックアップを作成
        backup_file = html_file + '.backup'
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 更新されたコンテンツを保存
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"  {html_file}: Added variable-aliases.css link (backup: {backup_file})")
        return True
    else:
        print(f"  {html_file}: No changes needed")
        return False

# HTMLファイルのリスト
html_files = ['index.html', 'orientation-video.html', 'user-guide.html']

print("Adding variable-aliases.css to HTML files...")
print("-" * 50)

for html_file in html_files:
    add_alias_css_link(html_file)

print("-" * 50)
print("Complete!")
