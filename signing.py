import random
import re
import xml.etree.ElementTree as ET

class SVGProcessor:
    def __init__(self, attribute_fractions, redundant_attributes):
        """
        Initialize the SVGProcessor with attribute probabilities.

        Parameters:
        - attribute_fractions (dict): Dictionary where keys are attribute names and values are probabilities (0 to 1).
        """
        self.attribute_fractions = attribute_fractions
        
        self.redundant_attributes = redundant_attributes

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
                # Check if the attribute is already defined in the tag (either directly or via style)
                if attr == 'fill' and has_fill_attribute(attributes):
                    continue  # Skip adding fill if it's already present in style or attributes
                
                # If the attribute doesn't already exist, add it with probability
                if f'{attr}="' not in attributes:
                    if random.random() < self.attribute_fractions.get(attr, 1):  # Based on the provided probability
                        # Add a space if there are already existing attributes
                        if attributes:
                            attributes += f' {attr}="{value}"'
                        else:
                            attributes += f'{attr}="{value}"'
            
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

        with open(output_file, 'w') as f:
            f.write(modified_svg)
            
    def verify(self, input_file):
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
        attribute_counts = {key: 0 for key in self.attribute_fractions}
        total_elements = 0

        # Traverse the SVG elements and count relevant attributes
        for element in root.iter():
            # Strip namespace from the tag
            tag = strip_namespace(element.tag)

            if tag not in allowed_tags:
                continue  # Skip elements not in the allowed subset

            total_elements += 1
            for attribute in self.attribute_fractions:
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
                'expected': self.attribute_fractions[key],
                'actual': actual_fractions[key],
                'matches': abs(self.attribute_fractions[key] - actual_fractions[key]) < 0.1
            }
            for key in self.attribute_fractions
        }
        
        return verification_results
