"""Rebuild the standalone app from the canonical JSON and editable template."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
d=json.loads((R/'curriculum.json').read_text());assert len(d['lessons'])==98 and len(d['ageBands'])==7 and len(d['yearMap'])==48
s=(R/'source/app_template.html').read_text();assert s.count('__CURRICULUM__')==1
(R/'Early_Learning_Curriculum_and_Records.html').write_text(s.replace('__CURRICULUM__',json.dumps(d,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')))
print('Built 98 activities, seven pathways and 48 planning slots.')
