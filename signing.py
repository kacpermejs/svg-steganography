import random
import re
import xml.etree.ElementTree as ET

class SVGProcessor:
    def __init__(self, redundant_attributes, micro_value_change):
        """
        Initialize the SVGProcessor with attribute probabilities.

        Parameters:
        - redundant_attributes (dict): Dictionary where there are attribute names
        and value is a tuple with value that don't change anything by default
        and a fraction of its expected occurrence.

        - micro_value_change (dict): Dictionary where there are attribute names
        and value is a tuple with micro value changes that won't be noticeable
        and a fraction of its expected occurrence.
        
        """
        self.redundant_attributes = redundant_attributes
        self.micro_value_changes = micro_value_change

    def _add_redundant_attributes(self, svg_content):
        """
        Add redundant attributes to SVG shapes with specified probabilities for each attribute.

        Parameters:
        - svg_content (str): The input SVG file content as a string.

        Returns:
        - str: The modified SVG content as a string.
        """
        # Define redundant attributes with their default values

        # Function to check if fill is already defined in the tag
        def has_fill_attribute(attributes):
            # Check if there is a fill attribute in the tag
            if 'fill="' in attributes:
                return True
            # Check if the style attribute contains a fill property (e.g., style="fill:#FFD63F;")
            if 'style="' in attributes:
                style_match = re.search(r'fill:\s*[^;]+', attributes)
                if style_match:
                    return True
            return False

        # Function to add redundant attributes to the matched tags
        def add_redundant_attributes_to_match(match):
            tag = match.group(1)
            attributes = match.group(2) if match.group(2) else ''
            closing = match.group(3)  # This captures the closing `/` for self-closing tags (e.g., <rect/>)

            # Add redundant attributes if not already present
            for attr, value in self.redundant_attributes.items():
                attr_value = value[0]
                fraction = value[1]
                
                # Check if the attribute is already defined in the tag (either directly or via style)
                if attr == 'fill' and has_fill_attribute(attributes):
                    continue  # Skip adding fill if it's already present in style or attributes
                
                # If the attribute doesn't already exist, add it with probability
                if f'{attr}="' not in attributes:
                    if random.random() < fraction:  # Based on the provided probability
                        # Add a space if there are already existing attributes
                        if attributes:
                            attributes += f' {attr}="{attr_value}"'
                        else:
                            attributes += f'{attr}="{attr_value}"'
            
            # Ensure redundant attributes are placed before the closing `/>` or `>`
            if closing:
                return f'<{tag} {attributes}/>'  # For self-closing tags
            else:
                return f'<{tag} {attributes}>'  # For regular tags

        # Regular expression to match all tags in the SVG (with or without attributes)
        # It captures the tag name, attributes, and any potential closing '/' for self-closing tags
        pattern = r'<(rect|path|circle)\s*([^>/]*)\s*(/?)>'

        # Modify the SVG content by adding redundant attributes to the relevant tags
        modified_svg_content = re.sub(pattern, add_redundant_attributes_to_match, svg_content)

        return modified_svg_content

    def _add_micro_value_changes(self, svg_content):

        # Function to add redundant attributes to the matched tags
        def add_micro_changes(match):
            tag = match.group(1)
            attributes = match.group(2) if match.group(2) else ''
            closing = match.group(3)  # This captures the closing `/` for self-closing tags (e.g., <rect/>)

            # Create a dictionary of existing attributes for easier manipulation
            attr_pattern = r'([a-zA-Z_:][\w:.-]*)\s*=\s*"([^"]*)"'
            existing_attributes = {attr: value for attr, value in re.findall(attr_pattern, attributes)}

            # Add or modify attributes based on `self.micro_value_changes`
            for attr, value in self.micro_value_changes.items():
                attr_value = value[0]
                fraction = value[1]
                default_value = value[2]
                predicate = value[3]

                if random.random() < fraction:
                    if attr in existing_attributes:
                        # Append the new value to the existing one
                        existing_attributes[attr] = f'{float(existing_attributes[attr]) + attr_value}'
                    else:
                        # Add the attribute with the new value if the probability check passes
                        existing_attributes[attr] = default_value + attr_value

            # Reconstruct the attributes string
            updated_attributes = ' '.join(f'{attr}="{value}"' for attr, value in existing_attributes.items())

            # Ensure redundant attributes are placed before the closing `/>` or `>`
            if closing:
                return f'<{tag} {updated_attributes}/>'  # For self-closing tags
            else:
                return f'<{tag} {updated_attributes}>'  # For regular tags

        # Regular expression to match all tags in the SVG (with or without attributes)
        # It captures the tag name, attributes, and any potential closing '/' for self-closing tags
        pattern = r'<(rect|path|circle)\s*([^>/]*)\s*(/?)>'

        # Modify the SVG content by adding redundant attributes to the relevant tags
        modified_svg_content = re.sub(pattern, add_micro_changes, svg_content)

        return modified_svg_content
    
    def _add_invisible_shapes(self, svg_content):
        return svg_content

    def process(self, input_file, output_file):
        """
        Process an input SVG file and write the modified SVG to an output file.

        Parameters:
        - input_file (str): Path to the input SVG file.
        - output_file (str): Path to the output SVG file.
        """
        with open(input_file, 'r') as f:
            svg_content = f.read()

        modified_svg = self._add_redundant_attributes(svg_content)
        modified_svg = self._add_micro_value_changes(modified_svg)
        modified_svg = self._add_invisible_shapes(modified_svg)

        with open(output_file, 'w') as f:
            f.write(modified_svg)
            

    def verify(self, input_file):
        r1 = self._verify_redundant_attributes(input_file)
        r2 = self._verify_micro_value_changes(input_file)
        return r1, r2

    def _verify_redundant_attributes(self, input_file):
    
        # Define the subset of SVG tags to match
        allowed_tags = {'rect', 'path', 'circle'}

        # Read the SVG content from the input file
        with open(input_file, 'r') as f:
            svg_content = f.read()

        # Parse the SVG content
        root = ET.fromstring(svg_content)

        # Function to strip namespace
        def strip_namespace(tag):
            return tag.split('}')[-1] if '}' in tag else tag

        # Initialize a dictionary to count attribute occurrences
        attribute_counts = {key: 0 for key in self.redundant_attributes}
        total_elements = 0

        # Traverse the SVG elements and count relevant attributes
        for element in root.iter():
            # Strip namespace from the tag
            tag = strip_namespace(element.tag)

            if tag not in allowed_tags:
                continue  # Skip elements not in the allowed subset

            total_elements += 1
            for attribute in self.redundant_attributes:
                if attribute in element.attrib:
                    attribute_counts[attribute] += 1

        # Compute the actual fractions
        actual_fractions = {
            key: count / total_elements if total_elements > 0 else 0
            for key, count in attribute_counts.items()
        }

        # Compare actual fractions to expected fractions
        verification_results = {
            key: {
                'expected': self.redundant_attributes[key][1],
                'actual': actual_fractions[key],
                'matches': abs(self.redundant_attributes[key][1] - actual_fractions[key]) < 0.1
            }
            for key in self.redundant_attributes
        }
        
        return verification_results

    def _verify_micro_value_changes(self, input_file):
        # Define the subset of SVG tags to match
        allowed_tags = {'rect', 'path', 'circle'}

        # Read the SVG content from the input file
        with open(input_file, 'r') as f:
            svg_content = f.read()

        # Parse the SVG content
        root = ET.fromstring(svg_content)

        # Function to strip namespace
        def strip_namespace(tag):
            return tag.split('}')[-1] if '}' in tag else tag

        # Initialize a dictionary to count value occurrences
        match_counts = {key: 0 for key in self.micro_value_changes}
        total_elements = 0

        # Traverse the SVG elements and count relevant values
        for element in root.iter():
            # Strip namespace from the tag
            tag = strip_namespace(element.tag)

            if tag not in allowed_tags:
                continue  # Skip elements not in the allowed subset

            total_elements += 1
            for key, value in self.micro_value_changes.items():
                # Extract the expected change and predicate from the tuple
                expected_change = value[0]
                predicate = value[3]
                
                if key in element.attrib:
                    try:
                        # Attempt to convert the attribute value to a float for numeric operations
                        numeric_value = float(element.attrib[key])

                        # Subtract and apply the predicate
                        if predicate(numeric_value - expected_change):
                            match_counts[key] += 1  # Increment the count for the specific key
                    except ValueError:
                        # Skip if the attribute value is not numeric
                        continue

        # Compute the actual fractions
        actual_fractions = {
            key: count / total_elements if total_elements > 0 else 0
            for key, count in match_counts.items()
        }

        # Compare actual fractions to expected fractions
        verification_results = {
            key: {
                'expected': self.micro_value_changes[key][1],
                'actual': actual_fractions[key],
                'matches': abs(self.micro_value_changes[key][1] - actual_fractions[key]) < 0.1
            }
            for key in self.micro_value_changes
        }
        
        return verification_results
