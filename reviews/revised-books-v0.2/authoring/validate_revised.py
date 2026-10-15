from pathlib import Path
from lxml import html
import json,hashlib,collections,csv
ROOT=Path(__file__).resolve().parent.parent
core=json.loads((ROOT/'data/revised_curriculum_1000.json').read_text());m=json.loads((ROOT/'manifest.json').read_text());errors=[];book_results=[]
assert len(core)==1000 and len({c['core_id'] for c in core})==1000
assert len({c['family_id'] for c in core})==100
assert all(c['state_rule_verified'] is False and c['training_credit'] is False for c in core)
assert all(c['model_answer_zh'] and c['rationale_zh'] for c in core)
assert sum(c['assessment_status']=='unscored legal research task' for c in core)==100
for book in m['books']:
 p=ROOT/book['file'];tree=html.fromstring(p.read_bytes());cards=tree.xpath('//article[@class="case"]');assert len(cards)==1000,book['state']
 assert len({c.get('id') for c in cards})==1000
 assert collections.Counter(c.get('data-setting') for c in cards)==dict(center=500,home=500)
 assert hashlib.sha256(p.read_bytes()).hexdigest()==book['sha256']
 for i,(card,c) in enumerate(zip(cards,core),1):
  assert card.get('id')==f'{book["code"]}-{i:04}'
  text=card.text_content()
  for field in ['scenario','scenario_zh','question','question_zh','model_answer','model_answer_zh','rationale','rationale_zh','applicability']:
   assert c[field] in text,(book['code'],c['core_id'],field)
  assert len(card.xpath('./details'))==1
 for link in tree.xpath('//a[@href]'):
  h=link.get('href')
  if not h.startswith(('http:','https:','#')):assert (p.parent/h).resolve().exists(),(p.name,h)
 assert len(tree.xpath('//*[@lang="zh-Hans"]'))>=7000
 book_results.append({'state':book['state'],'cases':len(cards),'hash_and_content_match':True,'internal_links_exist':True})
for name in ['START_HERE.html','STAFF_FOUNDATIONS.html','PRACTICE_ASSESSMENT_12.html']:
 p=ROOT/name;tree=html.fromstring(p.read_bytes())
 for link in tree.xpath('//a[@href]'):
  h=link.get('href')
  if not h.startswith(('http:','https:','#')):assert (p.parent/h).resolve().exists(),(name,h)
with (ROOT/'data/CHANGE_REGISTER_1000.csv').open(encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
assert len(rows)==1000 and len({r['core_id'] for r in rows})==1000
assert all(r['old_answer']!=r['new_answer'] and r['old_rationale']!=r['new_rationale'] and r['old_question']!=r['new_question'] for r in rows)
samples=json.loads((ROOT/'data/practice_assessment_12.json').read_text())['questions'];assert len(samples)==12
assert collections.Counter(s['answer'] for s in samples)==dict(A=3,B=3,C=3,D=3)
logs=json.loads((ROOT/'sources/retrieval_log.json').read_text());assert len(logs)==72
result=dict(structural_validation='passed',state_books=50,state_records=50000,shared_exercises=1000,situation_families=100,distinct_situation_rationales=len({c['rationale'] for c in core}),bilingual_answer_and_rationale_presence='passed',local_research_tasks_unscored=100,foundation_lessons=8,practice_questions=12,changed_questions_answers_and_rationales=1000,source_requests=72,source_texts_retrieved=sum(x.get('http_status')==200 for x in logs),state_rule_verified_cases=0,regulatory_approval='not_obtained',independent_translation_review='not_completed',browser_validation='pending',books=book_results)
(ROOT/'validation_report.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='books'},indent=2))
