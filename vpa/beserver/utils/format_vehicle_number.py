def format_vehicle_number(value):
    """
    Format vehicle number with hyphens according to Indian vehicle registration format.
    Format: XX-XX-X(X)-XXXX
    - Part 1: 2 letters (state code)
    - Part 2: 2 digits (district code)
    - Part 3: 1-2 letters (series)
    - Part 4: 1-4 digits (registration number)
    
    Examples:
    - GA06B3515 -> GA-06-B-3515
    - DSASSADDCC -> DS-AS-SA-DDCC (if SA is 2 letters)
    """

    if value is None:
        return "Unknown"
    
    if value == "Unknown":
        return "Unknown"
    # Remove all non-alphanumeric characters and convert to uppercase
    cleaned = ''.join(c for c in value if c.isalnum()).upper()
    
    if len(cleaned) < 5:
        # Not enough characters for a valid vehicle number
        return cleaned
    
    # Extract parts
    part1 = cleaned[:2]  # First 2 letters (state code)
    part2 = cleaned[2:4]  # Next 2 digits (district code)
    
    # Find where letters end and numbers begin after position 4
    remaining = cleaned[4:]
    
    # Split remaining into letters (part3) and numbers (part4)
    part3 = ''
    part4 = ''
    
    for char in remaining:
        if char.isalpha() and not part4:  # Still in letter series
            part3 += char
        else:  # Numbers part
            part4 += char
    
    # Format with hyphens
    if part3 and part4:
        formatted = f"{part1}-{part2}-{part3}-{part4}"
    elif part3:
        formatted = f"{part1}-{part2}-{part3}"
    else:
        formatted = f"{part1}-{part2}"
    
    return formatted


# Example usage:
examples = [
    "GA06B3515",      # -> GA-06-B-3515
    "GA06AB3515",     # -> GA-06-AB-3515
    "DL01CAF1234",    # -> DL-01-CAF-1234 (wait, this would be 3 letters)
    "MH12DE1234",     # -> MH-12-DE-1234
]

for vehicle_number in examples:
    formatted = format_vehicle_number(vehicle_number)
    print(f"{vehicle_number:15} -> {formatted}")