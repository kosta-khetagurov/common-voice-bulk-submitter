from conversions.ossetic import os_process

def preprocess(text, locale):
    if locale.lower() == 'os':
        return os_process(text)
    return text
