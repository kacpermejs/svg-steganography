import re

def modify_floats_in_svg(input_file_path, output_file_path, replacement_function, message):
    
    with open(input_file_path, 'r') as file:
        svg_content = file.read()

    # end of the message for the decryption
    stop_character = '\0'

    message_list = list(message) + [stop_character]

    chunk_size = 3
    partioned_list = [message_list[i:i + chunk_size] for i in range(0, len(message_list), chunk_size)]

    print(partioned_list)

    float_pattern = re.compile(r'\b\d+\.\d+\b')

    matches = re.findall(float_pattern, svg_content)

    matches_number = len(matches)

    if(len(partioned_list) > matches_number):
        print("Too long message.")
        return 
    


    # List to store the parts of the modified content
    modified_content = []
    last_end = 0

    counter = 0
    
    for match in float_pattern.finditer(svg_content):
            if ( counter > len(partioned_list) - 1):
                break
            # Append the content before the current match
            modified_content.append(svg_content[last_end:match.start()])
            # Replace the current match
            replacement = replacement_function((partioned_list[counter]),match)
            modified_content.append(replacement)
            # Update the last_end to the end of the current match
            last_end = match.end()
            counter+=1
    
    
    # Append the remaining content after the last match
    modified_content.append(svg_content[last_end:])

    # Join all parts to form the modified content
    modified_svg_content = ''.join(modified_content)

    # Write the modified content back to the file
    with open(output_file_path, 'w') as file:
        file.write(modified_svg_content)

    print(f"Modified SVG file saved to {output_file_path}.")
    