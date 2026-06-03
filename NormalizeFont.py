#!/usr/bin/env python3
import os
import sys
import re

def normalize_match(match):
    val = float(match.group(0))
    if val.is_integer():
        return str(int(val))
    return str(val)

def normalize_glyph_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    normalized_lines = []
    for line in lines:
        if line.startswith("ModTime:") or line.startswith("CreateTime:"):
            continue
        line = re.sub(r'\b\d+\.\d+\b', normalize_match, line)
        
        normalized_lines.append(line)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(normalized_lines)

def walk_sfdir(sfdir_path):
    if not os.path.isdir(sfdir_path) or not sfdir_path.endswith('.sfdir'):
        print(f"Error: {sfdir_path} is not a valid .sfdir directory.")
        sys.exit(1)

    print(f"Normalizing glyph files in {sfdir_path}...")
    count = 0
    for root, _, files in os.walk(sfdir_path):
        for file in files:
            if file.endswith('.glyph') or file in ['font.props', 'layers.txt']:
                normalize_glyph_file(os.path.join(root, file))
                count += 1
    print(f"Successfully normalized {count} files!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python normalize_sfdir.py <path_to_your_font.sfdir>")
        sys.exit(1)
        
    walk_sfdir(sys.argv[1])