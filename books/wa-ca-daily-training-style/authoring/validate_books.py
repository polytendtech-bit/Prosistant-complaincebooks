from pathlib import Path
from lxml import html
import json,hashlib,collections,csv
r=Path(__file__).resolve().parent.parent;results=[]
for code,name in [('WA','Washington'),('CA','California')]:
 p=r/'books'/(code+'_'+name+'_Practice_Book.html');t=html.fromstring(p.read_bytes());base=html.fromstring((r/'authoring'/(code+'_baseline.html')).read_bytes());rows=json.loads((r/'data'/(code+'_curriculum_1000.json')).read_text());cards=t.xpath('//article[@class="case"]');oldcards=base.xpath('//article[@class="case"]');assert len(cards)==len(rows)==1000
 assert t.xpath('//style/text()')==base.xpath('//style/text()'),code
 assert t.xpath('//script/text()')==base.xpath('//script/text()'),code
 assert len({c.get('id') for c in cards})==1000
 assert collections.Counter(c.get('data-setting') for c in cards)==dict(center=500,home=500)
 topic=collections.Counter(c.get('data-topic') for c in cards);assert len(topic)==25 and set(topic.values())=={40}
 for a,b,c in zip(cards,oldcards,rows):
  for attr in ['id','data-setting','data-topic']:assert a.get(attr)==b.get(attr)
  text=a.text_content()
  for field in ['scenario','scenario_zh','question','question_zh','required','required_zh','practical','practical_zh','records_best_practice','records_best_practice_zh','verify','verify_zh']:assert c[field] in text,(code,c['case_id'],field)
  assert len(a.xpath('./details'))==1
  assert len(a.xpath('./details/h4'))==5
  assert c['current_rule_verified'] is False and c['checked_date'] is None
 for a in t.xpath('//a[@href]'):
  href=a.get('href')
  if not href.startswith(('http:','https:','#')):assert (p.parent/href).resolve().exists(),(code,href)
 for id in ['search','topic','setting','show','hide','print','count']:assert len(t.xpath('//*[@id="'+id+'"]'))==1
 if code=='CA':
  for forbidden in ['DCYF','WCCC','MERIT','WAC 110','Issaquah','Bellevue']:
   assert forbidden not in t.xpath('//main')[0].text_content(),forbidden
  assert not any('leg.wa.gov' in h for h in t.xpath('//a/@href'))
 results.append({'state':code,'cases':1000,'topics':25,'center':500,'home':500,'original_css_unchanged':True,'original_js_unchanged':True,'ids_and_filter_attributes_retained':True,'all_bilingual_content_fields_match':True,'relative_links_exist':True,'current_rules_verified':0,'new_checked_dates':0})
for name in ['START_HERE.html','STAFF_FOUNDATIONS.html','PRACTICE_ASSESSMENT_12.html']:
 t=html.fromstring((r/name).read_bytes())
 for h in t.xpath('//a/@href'):
  if not h.startswith(('http:','https:','#')):assert (r/h).resolve().exists(),(name,h)
with (r/'data/CHANGE_REGISTER_2000.csv').open(encoding='utf-8-sig') as f:reg=list(csv.DictReader(f))
assert len(reg)==2000 and len({x['case_id'] for x in reg})==2000
v={'structural_validation':'passed','state_books':results,'total_records':2000,'template_provenance':'Supplied DOCX; source and date claims not independently verified','wa_baseline':'Repository edition 0.2; user local file URL could not be opened','ca_baseline':'Attached HTML','browser_validation':'pending','legal_review':'not completed','independent_bilingual_review':'not completed'}
(r/'validation_report.json').write_text(json.dumps(v,indent=2));print(json.dumps(v,indent=2))
