import random
from IPython.display import SVG, display

# Function to display SVG
def display_svg(file_path):
    display(SVG(filename=file_path))

# Define the function to generate an SVG with random rectangles
def generate_svg_with_random_rectangles(output_file="output/random_rectangles.svg", num_rectangles=5, svg_width=800, svg_height=600):

    svg_content = f'<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">\n'

    for _ in range(num_rectangles):
        x = random.random() * svg_width - 100
        y = random.random() * svg_height - 100
        width = random.random() * random.randint(20, 1000)
        height = random.random() * random.randint(20, 1000)
        color = f'#{random.randint(0, 0xFFFFFF):06x}'

        svg_content += f'  <rect x="{x}" y="{y}" width="{width}" height="{height}" fill="{color}" />\n'

    svg_content += '</svg>'

    with open(output_file, 'w') as file:
        file.write(svg_content)

    print(f"SVG file '{output_file}' generated with {num_rectangles} random rectangles.")