"""Rebuild the self-contained HTML from its editable template and curriculum."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
data=json.loads((R/'curriculum.json').read_text())
assert len(data['lessons'])==126 and len(data['skills'])==766
assert len({s['id'] for s in data['skills']})==766
ids={l['id'] for l in data['lessons']}
assert all(s['lessonId'] in ids for s in data['skills'])
template=(R/'source/app_template.html').read_text()
assert template.count('__CURRICULUM__')==1
(R/'Montessori_Planning_and_Records.html').write_text(template.replace('__CURRICULUM__',json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')))
print('Built 126 planning outlines and 766 source-aligned tracking items.')
