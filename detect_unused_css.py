#!/usr/bin/env python3
"""
未使用CSSの検出スクリプト
HTMLファイルで使用されていないCSSクラスを特定
"""

import re
import os
from collections import defaultdict

def extract_classes_from_html(html_files):
    """HTMLファイルから使用されているクラスを抽出"""
    used_classes = set()
    
    for html_file in html_files:
        if not os.path.exists(html_file):
            continue
            
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # class属性から抽出
        class_matches = re.findall(r'class="([^"]*)"', content)
        for match in class_matches:
            classes = match.split()
            used_classes.update(classes)
            
        # JavaScriptから動的に追加される可能性のあるクラス
        js_class_matches = re.findall(r'[\'"]\.([a-zA-Z][a-zA-Z0-9_-]*)[\'"]', content)
        used_classes.update(js_class_matches)
        
        js_class_matches2 = re.findall(r'addClass\([\'"]([^\'"]*)[\'"]\)', content)
        for match in js_class_matches2:
            used_classes.update(match.split())
    
    return used_classes

def extract_classes_from_css(css_file):
    """CSSファイルから定義されているクラスを抽出"""
    defined_classes = set()
    
    with open(css_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # クラスセレクタを抽出（.class-name形式）
    class_matches = re.findall(r'\.([a-zA-Z][a-zA-Z0-9_-]*)', content)
    defined_classes.update(class_matches)
    
    return defined_classes

def analyze_css_usage():
    """CSS使用状況を分析"""
    # HTMLファイルのリスト
    html_files = ['index.html', 'orientation-video.html', 'user-guide.html', 'study-guide.html']
    
    # 使用されているクラスを抽出
    used_classes = extract_classes_from_html(html_files)
    
    # CSS files to analyze
    css_files = {
        'webflow.css': 'css/webflow.css',
        'alc-study-unlimited.webflow.css': 'css/alc-study-unlimited.webflow.css'
    }
    
    results = {}
    
    for css_name, css_path in css_files.items():
        if not os.path.exists(css_path):
            continue
            
        defined_classes = extract_classes_from_css(css_path)
        
        # Webflowの特殊クラスを除外（w-で始まるものなど）
        webflow_system_classes = {cls for cls in defined_classes if cls.startswith('w-')}
        custom_classes = defined_classes - webflow_system_classes
        
        # 未使用クラスを特定
        unused_classes = custom_classes - used_classes
        used_in_css = custom_classes & used_classes
        
        results[css_name] = {
            'total_defined': len(defined_classes),
            'custom_classes': len(custom_classes),
            'webflow_system': len(webflow_system_classes),
            'used': len(used_in_css),
            'unused': len(unused_classes),
            'unused_list': sorted(list(unused_classes))[:20]  # 最初の20個
        }
    
    return results, used_classes

# 分析実行
results, used_classes = analyze_css_usage()

# レポート出力
print("=" * 60)
print("CSS使用状況分析レポート")
print("=" * 60)
print()

print(f"HTMLファイルで使用されているクラス総数: {len(used_classes)}")
print()

for css_name, data in results.items():
    print(f"\n【{css_name}】")
    print(f"  定義されているクラス総数: {data['total_defined']}")
    print(f"  - Webflowシステムクラス: {data['webflow_system']}")
    print(f"  - カスタムクラス: {data['custom_classes']}")
    print(f"  - 使用されている: {data['used']}")
    print(f"  - 未使用の可能性: {data['unused']}")
    
    if data['unused_list']:
        print(f"\n  未使用の可能性があるクラス（最初の20個）:")
        for cls in data['unused_list']:
            print(f"    .{cls}")

# 詳細レポートを保存
with open('css_backup/staged/unused_css_report.txt', 'w', encoding='utf-8') as f:
    f.write("CSS未使用クラス分析レポート\n")
    f.write("=" * 60 + "\n\n")
    
    for css_name, data in results.items():
        f.write(f"\n{css_name}:\n")
        f.write(f"  定義: {data['total_defined']} | 使用: {data['used']} | 未使用の可能性: {data['unused']}\n")
        
        if data['unused_list']:
            f.write("\n  未使用の可能性があるクラス:\n")
            for cls in data['unused_list']:
                f.write(f"    .{cls}\n")

print("\n詳細レポート保存先: css_backup/staged/unused_css_report.txt")
