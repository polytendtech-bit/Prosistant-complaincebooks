from pathlib import Path
from lxml import html
import json,csv,hashlib,collections
r=Path('/workspace/book_review/Prosistant_50_State_Practice_Books');out=Path('/workspace/book_review/results');d=json.loads((r/'developer-data/shared_curriculum_1000.json').read_text());m=json.loads((r/'manifest.json').read_text());errors=[];books=[]
for b in m['books']:
 p=r/b['book'];t=html.fromstring(p.read_bytes());a=t.xpath('//article[@class="case"]');byid={x.get('id'):x for x in a};mismatches=[]
 for i,c in enumerate(d,1):
  x=byid.get(f"{b['code']}-{i:04}")
  if x is None:mismatches.append(i);continue
  text=x.text_content()
  if not all(c[k] in text for k in ['scenario','scenario_zh','question','question_zh','model_answer','model_answer_zh','rationale','rationale_zh']):mismatches.append(i)
 row={'state':b['state'],'code':b['code'],'cases':len(a),'unique_ids':len(byid),'content_mismatches':mismatches,'hash_matches':hashlib.sha256(p.read_bytes()).hexdigest()==b['sha256'],'settings':dict(collections.Counter(x.get('data-setting') for x in a))}
 books.append(row)
with (r/'developer-data/case_review_register_50000.csv').open() as f:reg=list(csv.DictReader(f))
metrics={'scope':'Structural checks only; no substantive legal verification','shared_records':len(d),'scenario_families':len({c['family_id'] for c in d}),'distinct_questions':len({c['question'] for c in d}),'distinct_rationales':len({c['rationale'] for c in d}),'distinct_evidence_prompts':len({c['evidence'] for c in d}),'distinct_local_verification_prompts':len({c['local_verification'] for c in d}),'records_with_state_rule_verified':sum(c['state_rule_verified'] for c in d),'state_register_rows':len(reg),'state_register_rows_with_exact_rule_section':sum(bool(x['exact_rule_section'].strip()) for x in reg),'state_register_rows_with_named_rule_reviewer':sum(bool(x['rule_reviewer'].strip()) for x in reg),'books':books,'checks_passed':all(b['cases']==1000 and b['unique_ids']==1000 and b['hash_matches'] and not b['content_mismatches'] for b in books)}
(out/'structural_audit.json').write_text(json.dumps(metrics,indent=2));print(json.dumps({k:v for k,v in metrics.items() if k!='books'},indent=2))
