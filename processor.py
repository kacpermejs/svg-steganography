import re

def modify_floats_in_svg(input_file_path, output_file_path, replacement_function):
    
    with open(input_file_path, 'r') as file:
        svg_content = file.read()

    float_pattern = re.compile(r'\b\d+\.\d+\b')

    # List to store the parts of the modified content
    modified_content = []
    last_end = 0

    # Iterate over each match
    for match in float_pattern.finditer(svg_content):
        # Append the content before the current match
        modified_content.append(svg_content[last_end:match.start()])
        # Replace the current match
        replacement = replacement_function(match)
        modified_content.append(replacement)
        # Update the last_end to the end of the current match
        last_end = match.end()
    
    # Append the remaining content after the last match
    modified_content.append(svg_content[last_end:])

    # Join all parts to form the modified content
    modified_svg_content = ''.join(modified_content)

    # Write the modified content back to the file
    with open(output_file_path, 'w') as file:
        file.write(modified_svg_content)

    print(f"Modified SVG file saved to {output_file_path}.")
    