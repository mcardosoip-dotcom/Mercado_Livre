# coding: utf-8
import re, os
sql_dir = os.path.dirname(os.path.abspath(__file__))
for f in os.listdir(sql_dir):
    if not f.endswith('.sql') or f.startswith('_'):
        continue
    path = os.path.join(sql_dir, f)
    with open(path, 'r', encoding='utf-8') as fp:
        t = fp.read()
    if 'dme000426.' not in t:
        continue
    # Replace dme000426.TABLE with `<ENV>.TABLE`
    t = re.sub(r'dme000426\.([A-Za-z0-9_]+)', r'`<ENV>.\1`', t)
    with open(path, 'w', encoding='utf-8') as fp:
        fp.write(t)
    print('Done:', f)
