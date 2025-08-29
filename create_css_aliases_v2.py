#!/usr/bin/env python3
"""
CSS変数のエイリアス作成スクリプト（修正版）
長いWebflow生成の変数名に対して、短く分かりやすいエイリアスを作成
"""

import re

def extract_css_variables(css_content):
    """CSS内の:rootセクションから変数を抽出"""
    # :rootセクション内の変数を探す
    root_section = re.search(r':root\s*{([^}]+)}', css_content, re.DOTALL)
    if not root_section:
        return []
    
    root_content = root_section.group(1)
    # CSS変数の定義を抽出
    pattern = r'(--ai-gen-[^:]+):\s*([^;]+);'
    matches = re.findall(pattern, root_content)
    
    return matches

def extract_meaningful_name(long_name):
    """長い変数名から意味のある短い名前を抽出"""
    # 最後の意味のある部分を取得
    # 例: --ai-gen-xxx---container--container-width -> container-width
    parts = long_name.split('---')
    if len(parts) > 1:
        # 最後の部分を取得
        last_part = parts[-1]
        # ダブルダッシュを単一ダッシュに
        last_part = last_part.replace('--', '-')
        return last_part
    return long_name.replace('--ai-gen-', '')

def create_alias_mapping(css_variables):
    """CSS変数のエイリアスマッピングを作成"""
    alias_map = {}
    seen_names = {}
    
    for var_name, var_value in css_variables:
        var_name = var_name.strip()
        short_name = extract_meaningful_name(var_name)
        
        # 名前の重複を避ける
        if short_name in seen_names:
            # 重複する場合は番号を付ける
            counter = seen_names[short_name] + 1
            seen_names[short_name] = counter
            short_name = f"{short_name}-{counter}"
        else:
            seen_names[short_name] = 1
        
        alias_map[var_name] = f"--{short_name}"
    
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
        'section': [],
        'gap': [],
        'radius': [],
        'tag': [],
        'other': []
    }
    
    for long_name, short_name in sorted(alias_map.items(), key=lambda x: x[1]):
        category = 'other'
        short_clean = short_name.replace('--', '')
        
        # カテゴリ判定
        if 'container' in short_clean:
            category = 'container'
        elif 'section' in short_clean:
            category = 'section'
        elif 'spacing' in short_clean or 'padding' in short_clean or 'margin' in short_clean:
            category = 'spacing'
        elif 'gap' in short_clean:
            category = 'gap'
        elif 'radius' in short_clean:
            category = 'radius'
        elif 'color' in short_clean or 'neutral' in short_clean or 'accent' in short_clean or 'tint' in short_clean:
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
        elif 'typography' in short_clean or 'heading' in short_clean or 'eyebrow' in short_clean or 'h0' in short_clean or 'h1' in short_clean or 'h2' in short_clean or 'h3' in short_clean or 'h4' in short_clean or 'h5' in short_clean or 'h6' in short_clean:
            category = 'typography'
        elif 'tag' in short_clean:
            category = 'tag'
        
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
with open('css/alc-study-unlimited.webflow.css', 'r', encoding='utf-8') as f:
    content = f.read()

css_variables = extract_css_variables(content)
print(f"Found {len(css_variables)} CSS variables in :root section")

if css_variables:
    alias_map = create_alias_mapping(css_variables)
    alias_css = generate_alias_css(alias_map)
    
    # エイリアスCSS変数の保存
    with open('css_backup/staged/variable_aliases.css', 'w', encoding='utf-8') as f:
        f.write(alias_css)
    
    print(f"Created {len(alias_map)} variable aliases")
    print("Alias CSS saved to: css_backup/staged/variable_aliases.css")
    
    # マッピング情報も保存
    with open('css_backup/staged/variable_mapping.txt', 'w', encoding='utf-8') as f:
        f.write("CSS Variable Mapping\n")
        f.write("===================\n\n")
        for long_name, short_name in sorted(alias_map.items(), key=lambda x: x[1]):
            f.write(f"{short_name} -> {long_name}\n")
    
    print("Mapping saved to: css_backup/staged/variable_mapping.txt")
else:
    print("No CSS variables found in :root section")
