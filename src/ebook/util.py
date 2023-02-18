import re

def namespace_from_tag(tag):
    try:
        result = ''
        result = re.search('^{(.*)}', tag)
        result = result.group(1)
    finally:
        return result
