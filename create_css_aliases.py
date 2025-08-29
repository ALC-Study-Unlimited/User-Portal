#!/usr/bin/env python3
"""
CSS変数のエイリアス作成スクリプト
長いWebflow生成の変数名に対して、短く分かりやすいエイリアスを作成
"""

import re

def extract_meaningful_name(long_name):
    """長い変数名から意味のある短い名前を抽出"""
    # 最後の部分から意味のある名前を取得
    parts = long_name.split('--')
    if len(parts) > 1:
        last_part = parts[-1]
        # container-width -> container-width
        # bg-primary -> bg-primary
        return last_part
    return long_name

def create_alias_mapping(css_content):
    """CSS変数のエイリアスマッピングを作成"""
    pattern = r'(--ai-gen-[^:]+):\s*([^;]+);'
    matches = re.findall(pattern, css_content)
    
    alias_map = {}
    seen_names = set()
    
    for var_name, var_value in matches:
        short_name = extract_meaningful_name(var_name.strip())
        
        # 名前の重複を避ける
        if short_name in seen_names:
            # 重複する場合は番号を付ける
            counter = 2
            while f"{short_name}-{counter}" in seen_names:
                counter += 1
            short_name = f"{short_name}-{counter}"
        
        seen_names.add(short_name)
        alias_map[var_name.strip()] = f"--{short_name}"
    
    return alias_map

def generate_alias_css(alias_map):
    """エイリアスCSSを生成"""
    css_lines = [
        "/* ================================= */",
        "/* CSS Variable Aliases for Better Maintainability */",
        "/* Generated to simplify long Webflow variable names */",
        "/* Original values are preserved - these are just references */",
        "/* ================================= */",
        "",
        ":root {"
    ]
    
    # カテゴリごとにグループ化
    categories = {
        'container': [],
        'spacing': [],
        'color': [],
        'text': [],
        'background': [],
        'border': [],
        'button': [],
        'card': [],
        'input': [],
        'typography': [],
        'other': []
    }
    
    for long_name, short_name in sorted(alias_map.items(), key=lambda x: x[1]):
        category = 'other'
        short_clean = short_name.replace('--', '')
        
        if 'container' in short_clean:
            category = 'container'
        elif 'spacing' in short_clean or 'padding' in short_clean or 'margin' in short_clean:
            category = 'spacing'
        elif 'color' in short_clean or 'neutral' in short_clean or 'accent' in short_clean:
            category = 'color'
        elif 'text' in short_clean or 'font' in short_clean:
            category = 'text'
        elif 'bg-' in short_clean or 'background' in short_clean:
            category = 'background'
        elif 'border' in short_clean:
            category = 'border'
        elif 'button' in short_clean or 'btn' in short_clean:
            category = 'button'
        elif 'card' in short_clean:
            category = 'card'
        elif 'input' in short_clean:
            category = 'input'
        elif 'typography' in short_clean or 'heading' in short_clean:
            category = 'typography'
        
        categories[category].append((long_name, short_name))
    
    # カテゴリごとに出力
    for category, items in categories.items():
        if items:
            css_lines.append(f"  /* {category.title()} Variables */")
            for long_name, short_name in items:
                css_lines.append(f"  {short_name}: var({long_name});")
            css_lines.append("")
    
    css_lines.append("}")
    css_lines.append("")
    
    return '\n'.join(css_lines)

# メイン処理
with open('css/alc-study-unlimited.webflow.css', 'r') as f:
    content = f.read()

alias_map = create_alias_mapping(content)
alias_css = generate_alias_css(alias_map)

# エイリアスCSS変数の保存
with open('css_backup/staged/variable_aliases.css', 'w') as f:
    f.write(alias_css)

print(f"Created {len(alias_map)} variable aliases")
print("Alias CSS saved to: css_backup/staged/variable_aliases.css")

# マッピング情報も保存
with open('css_backup/staged/variable_mapping.txt', 'w') as f:
    f.write("CSS Variable Mapping\n")
    f.write("===================\n\n")
    for long_name, short_name in sorted(alias_map.items(), key=lambda x: x[1]):
        f.write(f"{short_name} -> {long_name}\n")

print("Mapping saved to: css_backup/staged/variable_mapping.txt")
