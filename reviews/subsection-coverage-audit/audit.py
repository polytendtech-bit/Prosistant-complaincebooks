from pathlib import Path
from lxml import html
import json,csv,collections,hashlib,re
out=Path('/workspace/subsection_revision');repo=Path('/workspace/Prosistant-complaincebooks/books/wa-ca-daily-training-style');inputs={'WA':Path('/workspace/attachments/2edd8101-8e42-4880-9e91-b6052b9d8650/WA_Washington_Practice_Book(10_15 improved version).html'),'CA':Path('/workspace/attachments/cea5c57f-8a03-46fd-a00e-b6c3107c3ec6/CA_California_Practice_Book (10_15 improved version).html')}
allrows=[];stats={};data={};queue=[]
for code,p in inputs.items():
 t=html.fromstring(p.read_bytes());cards=t.xpath('//article[@class="case"]');records=json.loads((repo/'data'/(code+'_curriculum_1000.json')).read_text());assert len(cards)==len(records)==1000
 for c,r in zip(cards,records):
  assert c.get('id')==r['case_id'];assert r['scenario'] in c.text_content();assert r['required'] in c.text_content()
 data[code]=records;fam=collections.Counter(x['family_id'] for x in records);required=collections.Counter(x['required'] for x in records);practical=collections.Counter(x['practical'] for x in records);recordtexts=collections.Counter(x['records_best_practice'] for x in records)
 stats[code]={'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'input_matches_latest_repository_book':p.read_bytes()==(repo/'books'/('WA_Washington_Practice_Book.html' if code=='WA' else 'CA_California_Practice_Book.html')).read_bytes(),'cases':len(cards),'topic_count':len({x['topic'] for x in records}),'base_families':len(fam),'family_task_counts':dict(collections.Counter(fam.values())),'distinct_required_answer_texts':len(required),'distinct_practical_answer_texts':len(practical),'distinct_record_answer_texts':len(recordtexts),'verified_current_rule_cases':sum(x['current_rule_verified'] for x in records),'cases_with_exact_subsection_field':sum(bool(x.get('rule_subsection')) for x in records)}
 for r in records:
  urls=[x['url'] for x in r['source_leads']]
  allrows.append(dict(state=code,case_id=r['case_id'],topic=r['topic'],family_id=r['family_id'],current_title=r['title'],same_family_cases=fam[r['family_id']],identical_required_answer_cases=required[r['required']],identical_practical_answer_cases=practical[r['practical']],identical_record_answer_cases=recordtexts[r['records_best_practice']],current_source_leads='; '.join(urls),exact_current_rule_subsection='',distinct_requirement_id='',rule_text_retrieved=False,disposition='Re-author from a distinct verified requirement; do not keep a generic decision variant solely to fill the count',scope='Coverage audit; no new legal approval'))
 for url in sorted({s['url'] for r in records for s in r['source_leads']}):
  queue.append(dict(state=code,url=url,role='Existing reference lead; not exact-subsection verification',current_text_retrieved=False,next_step='Retrieve effective text, identify setting and program, extract each operative subsection/condition/exception, then map new cases.'))
shared={}
for field in ['scenario','question','required','practical','records_best_practice']:
 shared[field]=sum(a[field]==b[field] for a,b in zip(data['WA'],data['CA']))
summary={'scope':'Audit of both actual uploaded HTML books; no current primary rule text verified','states':stats,'cross_state_identical_text_at_same_case_position':shared,'source_leads':dict(collections.Counter(r['state'] for r in queue)),'all_cases_need_exact_subsection_mapping':len(allrows)}
(out/'coverage_audit.json').write_text(json.dumps(summary,indent=2))
def csvout(name,rows):
 with (out/name).open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
csvout('CASE_COVERAGE_REGISTER_2000.csv',allrows);csvout('SOURCE_RETRIEVAL_QUEUE.csv',queue)
print(json.dumps(summary,indent=2))
