import re

def modify_floats_in_svg(file_path):
    
    with open(file_path, 'r') as file:
        svg_content = file.read()

    float_pattern = re.compile(r'\b\d+\.\d+\b')
    matches = float_pattern.findall(svg_content)

    print(*matches, sep='\n')