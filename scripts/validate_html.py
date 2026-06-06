import os
from html.parser import HTMLParser

class StrictHTMLParser(HTMLParser):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.stack = []
        self.errors = []
        # Void elements that don't need closing tags
        self.void_elements = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr', 'path', 'svg', 'line'}

    def handle_starttag(self, tag, attrs):
        if tag not in self.void_elements:
            self.stack.append((tag, self.getpos()))

    def handle_endtag(self, tag):
        if tag in self.void_elements:
            return
            
        if not self.stack:
            self.errors.append(f"Line {self.getpos()[0]}: Unexpected closing tag </{tag}>. No tags are currently open.")
            return
            
        expected_tag, pos = self.stack.pop()
        
        # HTML allows omitting some end tags like <li> or <p>, but we are doing strict checking.
        # Let's tolerate a bit or just report it
        if expected_tag != tag:
            # Maybe it's an unclosed <p> or <li> which is valid HTML but messy.
            optional_close = {'p', 'li', 'dt', 'dd', 'rt', 'rp', 'optgroup', 'option', 'colgroup', 'thead', 'tbody', 'tfoot', 'tr', 'td', 'th'}
            while expected_tag != tag and expected_tag in optional_close and self.stack:
                expected_tag, pos = self.stack.pop()
                
            if expected_tag != tag:
                self.errors.append(f"Line {self.getpos()[0]}: Mismatched closing tag </{tag}>. Expected </{expected_tag}> (opened at line {pos[0]}).")
                # push it back to try to recover
                self.stack.append((expected_tag, pos))

def validate_file(filepath):
    parser = StrictHTMLParser(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    try:
        parser.feed(content)
        if parser.stack:
            for tag, pos in parser.stack:
                # ignore optional closing tags at end of file
                if tag not in {'html', 'body'}:
                    parser.errors.append(f"Line {pos[0]}: Unclosed tag <{tag}>.")
    except Exception as e:
        parser.errors.append(f"Parse error: {e}")
        
    return parser.errors

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
has_errors = False
for root, dirs, files in os.walk(root_dir):
    if "legacy" in root or "clientes" in root or "scripts" in root:
        continue
    for file in files:
        if file.endswith(".html"):
            filepath = os.path.join(root, file)
            errors = validate_file(filepath)
            if errors:
                has_errors = True
                print(f"--- Syntax errors in {os.path.relpath(filepath, root_dir)} ---")
                for err in errors:
                    print(f"  {err}")

if not has_errors:
    print("No HTML syntax errors found.")
