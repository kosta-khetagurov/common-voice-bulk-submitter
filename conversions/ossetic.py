def os_process(text):
    # Define the mapping of "æ" to its Cyrillic analogs
    replacements = {
        'æ': 'ӕ',
        'Æ': 'Ӕ',
    }

    for old_char, new_char in replacements.items():
        text = text.replace(old_char, new_char)

    return text
