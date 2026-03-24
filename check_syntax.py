import ast
import os

def check_syntax(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            ast.parse(f.read())
            return None
        except SyntaxError as e:
            return f"Syntax Error: {e.msg} at line {e.lineno}, col {e.offset}"
        except Exception as e:
            return str(e)

root = r'c:\Users\carvaldel\Documents\mi_proyecto_odoo\addons\school_lost_found'
for dirpath, dirnames, filenames in os.walk(root):
    for filename in filenames:
        if filename.endswith('.py'):
            path = os.path.join(dirpath, filename)
            err = check_syntax(path)
            if err:
                print(f"{path}: {err}")
            else:
                print(f"{path}: OK")
