import re


def replace_with_regex(patterns_replacements, text):
    """
    Replace multiple patterns in the text with their respective replacements using regular expressions.

    Args:
        patterns_replacements (dict): A dictionary where keys are patterns and values are replacements.
        text (str): The input string.

    Returns:
        str: The new string after replacements.
    """
    new_text = text

    # Iterate through the dictionary and perform replacements
    for pattern, replace in patterns_replacements.items():
        new_text = re.sub(pattern, replace, new_text)

    return new_text


# Example usage:
if __name__ == "__main__":
    patterns_replacements = {
        r"\bapple\b": "orange",  # Replace 'apple' with 'orange'
        r"\bdog\b": "cat",  # Replace 'dog' with 'cat'
        r"\bcar\b": "bicycle",  # Replace 'car' with 'bicycle'
    }

    input_text = "I have an apple, a dog, and a car."
    output_text = replace_with_regex(patterns_replacements, input_text)
    print(output_text)
