from pathlib import Path
from lxml import html,etree
import json,csv,hashlib,copy,re
ROOT=Path(__file__).resolve().parent.parent;A=ROOT/'authoring';DATA=ROOT/'data';DATA.mkdir(exist_ok=True);(ROOT/'books').mkdir(exist_ok=True)
original=json.loads((A/'original_shared_curriculum.json').read_text());registry=json.loads((A/'state_registry.json').read_text());scenes={};actions={};teach={}
for line in (A/'scenes.tsv').read_text().splitlines():
 i,en,zh=line.split('\t');scenes[int(i)]=(en,zh)
for line in (A/'family_notes.tsv').read_text().splitlines():
 i,change,action=line.split('\t');actions[int(i)]=(change,action)
for line in (A/'teaching_notes.tsv').read_text().splitlines():
 i,why,whyzh,actionzh=line.split('\t');teach[int(i)]=(why,whyzh,actionzh)
qen=(A/'questions_en.txt').read_text().splitlines();qzh=(A/'questions_zh.txt').read_text().splitlines();assert len(qen)==len(qzh)==100
VARIANTS=[
('Immediate response','即时处理','Children remain in care while this decision is being made. Another worker suggests dealing with the records before changing the arrangement.','作出决定时，孩子仍在现场。另一名员工建议先处理记录，再改变眼前安排。','How would you divide the work now and prevent the response itself from leaving children unsupervised?','现在怎样分工，避免处理事情时又造成看护空档？','Keep the immediate safeguard in place while a named qualified person covers the children. Deal with routine paperwork after urgent care is secured.','先落实眼前防护，由明确的合格人员继续看护。紧急照护安排好后，再处理常规文书。'),
('Working alone','独自工作','In this version the setting is a family child-care home, and you are the only qualified caregiver on site. No approved second caregiver is immediately available.','本题设在家庭托育场所，现场只有你一位合格照护者，没有已确认可立即接手的第二个人。','What can you do yourself, what can wait, and when would you need the permitted backup or contingency plan?','哪些能自己做，哪些可以等，什么时候需要启用允许的备用或应变安排？','Keep responsibility for the children, pause non-urgent competing tasks and use only a verified permitted backup. If the actual setting cannot support safe care, use the appropriate contingency process rather than inventing an available helper.','你继续负责孩子，推迟不紧急的冲突任务，只使用已核实获准的备用人员。实际条件不能支持安全照护时，按应变安排处理，不假设有一个现成帮手。'),
('Pressure for an exception','要求破例','Someone asks you to overlook the concern just for today because changing plans would be inconvenient. The relevant facts and any claimed exception have not changed.','有人希望今天先通融，因为改变计划不方便。但实际情况和所谓例外，并没有因此得到确认。','What would you explain, and what alternative could you offer without promising an unverified exception?','你会怎样解释，并提供什么替代安排，而不承诺未经核实的例外？','Explain the specific concern calmly and offer the safe option identified for this event. Do not turn inconvenience or consent into proof that a legal exception exists.','平静说明这次具体顾虑，提供本事件可行的安全安排。不便或同意，都不能证明法律上确有例外。'),
('Substitute handoff','代班交接','A qualified substitute is due to take over later. They know the usual routine but have not been told what happened, which safeguards are in place or what remains unresolved.','合格代班人员稍后接手。他熟悉平时作息，却不知道这次发生了什么、已做了哪些防护，以及什么还没解决。','Before responsibility changes, what must the substitute be able to explain and find?','交接前，代班人员必须能说清什么、找到什么？','Brief the substitute on this event, the current safeguard, necessary child-specific instructions and any unresolved decision. Have them explain the next action and locate the relevant record before a clear handoff. Verify their actual role separately.','交代本事件、现有防护、必要的儿童个人说明和未决事项。请代班人员说出下一步并找到相关记录，再明确交接；实际岗位资格另行核实。'),
('Conflicting accounts','说法与记录不符','A coworker says the issue has already been resolved, but the available record does not confirm it. You cannot yet establish which account is accurate.','同事说问题已经解决，现有记录却不能证明。你还无法确定哪种说法准确。','What would you preserve, verify and correct, and which urgent actions must not wait for agreement?','你会保留、核实和更正什么？哪些紧急行动不能等到大家说法一致？','Keep each original account and separate observations, reported information and unknown facts. Make a dated, traceable clarification using actual evidence. Do not delay urgent care or an already-required report to produce one agreed story.','保留原始说法，区分亲见、转述和未知。根据实际依据，留下有日期、可追溯的补充或更正。不能为了统一故事拖延紧急照护或已经要求的报告。'),
('Unverified helper','帮手职责未核实','A helper offers to deal with the issue, but their eligibility for child care or confidential information has not been checked. Other staff assume willingness is enough.','有人愿意帮忙，但其承担儿童照护或接触保密资料的资格尚未核实。其他员工觉得热心就够了。','Which tasks could you consider delegating, and which responsibilities must stay with eligible people?','你可以考虑交出哪些工作，哪些责任必须由合格人员保留？','Consider only tasks allowed for the person’s actual role. Do not transfer supervision, count the helper as qualified staff or disclose private records merely because help was offered. Keep the safe-care responsibility clearly assigned.','只考虑该人实际职责允许的任务。不因对方愿意帮忙，就交出看护、算作合格人员或开放私人记录。安全照护责任必须明确。'),
('Family explanation','向家庭说明','The affected family asks for an explanation and also requests details about another child or worker. Some facts are still unknown.','受影响家庭要求解释，也问到另一名孩子或员工的细节，其中部分事实仍未知。','What would you tell the family now, what would remain private, and what separate notices might still be due?','现在向家庭说明什么，哪些要保密，哪些另行通知责任仍需处理？','Explain the verified facts relevant to that family’s child and what you actually did. State what remains unknown, restrict unrelated private details and handle any applicable official notice or report separately.','说明与该家庭孩子有关的已核实事实和实际行动，坦诚指出未知，限制无关隐私；另行处理适用的正式通知或报告。'),
('Preventing a repeat','防止再次发生','A similar problem occurred recently and received a verbal reminder. The same workflow or equipment remains in use, and the problem has returned.','类似问题不久前发生过，当时只作口头提醒。流程或设备没有变化，问题又出现了。','What measurable change would you make, who would own it and how would you check whether it works?','你会作什么可衡量改变、由谁负责，又怎样检查是否有效？','Change the actual workflow, environment, information or coverage gap behind this event. Name an owner and check the safeguard during safe ordinary use or a simulation; do not recreate a hazard with a child.','改变本事件背后的流程、环境、信息或人员缺口，明确负责人，在安全日常使用或模拟中检查效果，不让孩子再次冒险来测试。'),
('An older rule summary','旧摘要与现行要求','A saved summary appears to support a different response. Its effective date, license category and any exceptions have not been established.','一份旧摘要似乎支持不同做法，但生效日期、许可类别和例外均未查清。','Which issuing-source text and program facts would you need before changing the legal conclusion?','改变法律判断前，要取得什么签发机构原文和项目事实？','Identify the current issuing authority, exact license category and relevant program. Obtain the effective primary text and check scope, exceptions, required action, recipient and timing. Keep the general safety response in place; the jurisdiction-specific answer remains unresolved here.','确认当前签发机构、准确许可类别和相关项目，取得有效原文，核对范围、例外、行动、对象和时限。继续保持一般安全措施；本版尚不能确定具体法律结论。'),
('Explaining the response','说明处理经过','An authorized reviewer asks what you knew, what you did and how you decided whether the issue was resolved. The team has some records but also unresolved facts.','获授权审阅人员问你当时知道什么、做了什么，以及怎样判断问题已解决。团队有部分记录，也有未确定事实。','What factual timeline and evidence would you provide, and what uncertainty would you disclose?','你会提供什么真实时间线和证据，又会说明哪些不确定性？','Explain actual observations, actions, responsible people and results in order. Supply relevant authorized records and distinguish unresolved facts. Do not backdate, invent a completion or treat a polished explanation as proof of compliance.','按顺序说明真实观察、行动、负责人和结果，提供相关获授权记录，并区分未知。不倒签、不编造完成，也不把说得漂亮当成合规证明。')]
# These section numbers were supplied in the DOCX or are discovery leads, not current verified citations.
wa_topic=[['110-300-0345','110-300-0455'],['110-300-0356','110-300-0357'],['110-06-0040','110-06-0041','110-300-0100'],['110-300-0106','110-300-0107','110-300-0115'],[],['110-300-0215','110-300-0300'],['110-300-0300'],['110-300-0205','110-300-0500','110-300-0475'],[],[],['110-300-0470'],['110-300-0475','110-300-0460'],[],['110-300-0340','110-300-0486'],['110-300-0030','110-300-0340','110-300-0486'],['110-300-0455'],['110-300-0480','110-300-0106'],['110-300-0480','110-300-0345'],[],[],['110-300-0460','110-300-0115'],['110-15-0034','110-15-0036','110-15-0126'],[],[],[]]
def leads(code,topic):
 if code=='WA':
  result=[{'label':'WAC '+s,'url':'https://app.leg.wa.gov/wac/default.aspx?cite='+s} for s in wa_topic[topic]]
  if not result:result=[{'label':'WAC 110-300 — locate the setting-specific provision','url':'https://app.leg.wa.gov/wac/default.aspx?cite=110-300'}]
  if topic==12:result=[{'label':'RCW 26.44 — protective-reporting research lead','url':'https://app.leg.wa.gov/rcw/default.aspx?cite=26.44'}]
  if topic==14:result.append({'label':'DOJ child-care ADA guidance','url':'https://www.ada.gov/resources/child-care-centers/'})
  return result
 result=[{'label':'CDSS child-care laws and regulations','url':'https://www.cdss.ca.gov/inforesources/child-care-licensing/resources-for-providers/laws-and-regulations'},{'label':'CDSS child-care centers manual — verify current edition and scope','url':'https://www.cdss.ca.gov/ord/entres/getinfo/pdf/ccc7.pdf'},{'label':'CDSS family child-care homes manual — verify current edition and scope','url':'https://www.cdss.ca.gov/ord/entres/getinfo/pdf/fccman.pdf'}]
 if topic==12:result=[{'label':'California Legislative Information — locate current reporting law','url':'https://leginfo.legislature.ca.gov/'},{'label':'CDSS child-care licensing — separate licensing obligations','url':'https://www.cdss.ca.gov/inforesources/child-care-licensing'}]
 if topic==21:result=[{'label':'CDSS child-care and development programs — identify the actual subsidy program','url':'https://www.cdss.ca.gov/inforesources/child-care-and-development'}]
 if topic==14:result.append({'label':'DOJ child-care ADA guidance','url':'https://www.ada.gov/resources/child-care-centers/'})
 return result
def node(tag,text=None,**attrs):
 x=etree.Element(tag,**attrs)
 if text is not None:x.text=text
 return x
def pair(parent,zh,en,tag='p'):
 parent.append(node(tag,zh,lang='zh-Hans'));parent.append(node('p',en,lang='en',**{'class':'zh'}))
allrows=[];changes=[];manifest=[]
for code in ['WA','CA']:
 tree=html.fromstring((A/(code+'_baseline.html')).read_bytes());cards=tree.xpath('//article[@class="case"]');assert len(cards)==1000
 state=next(s for s in registry if s['code']==code);statezh='华盛顿州' if code=='WA' else '加州';authority='DCYF and the appropriate health, protective-reporting or subsidy authority' if code=='WA' else 'the applicable California licensing, health, protective-reporting or subsidy authority';authorityzh='DCYF及相应卫生、保护报告或补助机构' if code=='WA' else '加州相应许可、卫生、保护报告或补助机构'
 title_node=tree.xpath('//title')[0];title_node.text=state['state']+' child-care cases · bilingual daily-training style'
 main=tree.xpath('//main')[0];h1=main.xpath('./h1')[0];h1.clear();h1.text=statezh+'托育许可合规练习 / '+state['state']+' Child Care Practice'
 notice=main.xpath('./div[@class="notice"]')[0];notice.clear();notice.set('class','notice');pair(notice,'本版采用每日训练的案例写法：先分析事件，再展开参考答案。保留1,000个练习、25个主题和原有操作。它们来自100个基础情境的十种决策练习，并非1,000个独立编写的事件。','This edition uses the daily-training case style: analyze the incident before opening the answer. It retains 1,000 exercises, 25 topics and the original controls. These are ten guided decisions for each of 100 underlying situations, not 1,000 independently authored incidents.')
 pair(notice,'本次是写法与编排改写，现行法规核验未完成。参考答案的“必须事项”列出初稿中的安全处理底线，不代表完整、已核实的法定义务。场景人数、时间及金额是练习事实，不是法律门槛。模板中的旧核验日期没有作为本版核验结果沿用。','This is a writing and presentation revision; current rule verification is incomplete. “Required actions” sets out draft safety safeguards, not a complete verified statement of legal duties. Scenario counts, times and amounts are exercise facts, not legal thresholds. The template’s earlier checked dates have not been reused as verification for this edition.')
 # Preserve existing navigation and controls while changing the practice instructions.
 for p in main.xpath('./p'):
  if p.text and p.text.startswith('Read the short teaching note.'):
   p.text='Read the bilingual incident and questions, write or discuss your action plan, then reveal the reference answer. Use fictional facts; do not enter child or family records.'
  elif p.text and p.text.startswith('先读教学提示'):
   p.text='先读中英文情境和问题，写下或讨论处理方案，再展开参考答案。练习只用虚构资料，不输入真实儿童或家庭记录。'
 bookrows=[]
 for i,card in enumerate(cards):
  old=original[i];fi=i//10+1;vi=i%10;topic=i//40;v=VARIANTS[vi];lens,lenszh,context,contextzh,follow,followzh,approach,approachzh=v
  incident,incidentzh=scenes[fi];why,whyzh,actionzh=teach[fi];action=actions[fi][1]
  if fi==17:
   action='Remove the stuffed toy from the infant’s sleep space, maintain supervision and explain the safe-sleep procedure to the parent. A familiar item from home does not establish that it belongs in the sleep space.'
   actionzh='移走婴儿睡眠区域里的毛绒玩具，继续照看，并向家长解释安全睡眠做法。家中熟悉的物品，不代表适合留在睡眠区域。'
  if fi==18:
   action='Safely transfer the infant from the swing to an appropriate infant sleep space and continue the required observation. Do not turn the swing into the routine sleep place because transfer might wake the infant.'
   actionzh='把婴儿安全转到合适的婴儿睡眠空间，继续所需查看。不因担心转移会弄醒，就把摇椅当成固定睡眠地点。'
  if fi==1:
   action='Mia should say, “Jordan, you have Leo now,” and wait for Jordan to reply, “I have Leo.” Check Leo against the receiving list. Mia remains responsible until the handoff is complete.'
   actionzh='Mia说清：“Jordan，现在把Leo交给你。”等Jordan明确回应，再按接收名单核对Leo。交接完成前，Mia继续负责。'
  if fi==56:
   action='Write the observed event: “After a peer took the truck, Ava pushed a block toward that child.” Add the actual adult response and outcome. If either is unknown, record that uncertainty rather than invent a helpful response.'
   actionzh='写清观察事实：“同伴拿走小车后，Ava把积木推向对方。”再记实际成人回应和结果。不知道的地方如实注明，不为记录完整而编出一次帮助。'
  if fi==1 and vi==1:
   incident='At a residential care doorway, a child starts moving toward another room. A household adult says they can watch briefly, but their eligibility has not been established. You are still responsible for the group.'
   incidentzh='住宅托育的门口，一名孩子开始走向另一个房间。家中成人说可以暂时帮忙看，但资格未确认，你仍负责全组。'
   action='Keep responsibility for the child and group. Do not send the child through the doorway without a verified eligible person clearly accepting care. Use the safe approved area and the permitted contingency plan if safe care cannot continue.'
   actionzh='继续负责这个孩子和全组。没有已核实合格人员明确接手，就不让孩子独自进入另一房间。使用可安全照看的获准区域，不能继续安全照护时启用允许的应变安排。'
  if fi==2 and vi==1:
   action='Use an arrangement that safely supervises all children without assuming a second caregiver exists. If the actual bathroom and group layout cannot support that, use the permitted contingency plan rather than leaving children unattended.'
   actionzh='使用在只有一名合格照护者的条件下，仍能安全照看所有孩子的安排。实际洗手间和活动区布局做不到时，采用允许的应变方案，不把其他孩子单独留下。'
  applicability='Identify the exact license category and program before applying a legal conclusion.'
  applicabilityzh='作法律判断前，先确认准确许可类别和项目。'
  if fi in [77,78,79,80]:
   applicability='This exercise uses household facts. For a commercial center without those facts, adapt the incident or record it as not applicable rather than importing residential duties.'
   applicabilityzh='本题使用家庭住户事实。不具备这些事实的商业中心，应改写情境或注明不适用，不能直接套用住宅要求。'
  elif fi==10:
   applicability='This is a role-change exercise. If the actual license category has no such director role, use the relevant responsible role rather than assume a center requirement applies to a home.'
   applicabilityzh='这是岗位变更练习。实际许可类别没有这种主管岗位时，应使用对应负责岗位，不把中心岗位要求套到家庭托育。'
  role='As the family child-care provider' if old['setting']=='home' else 'As director';rolezh='作为家庭托育负责人' if old['setting']=='home' else '作为园长'
  question=role+', '+qen[fi-1][0].lower()+qen[fi-1][1:]+' '+follow
  questionzh=rolezh+'，'+qzh[fi-1]+followzh
  records='Keep the factual evidence relevant to “'+old['title'].split(' — ')[0]+'”: the actual observation, time, action, responsible person and result. '+why+' Record any unknown facts openly; use a dated correction rather than overwrite history.'
  recordszh='保留“'+old['title_zh'].split(' — ')[0]+'”相关事实：实际观察、时间、行动、负责人和结果。'+whyzh+' 未知事项如实注明；更正留实际日期，不覆盖历史。'
  verify=old['local_verification']+' Confirm any required route, form, deadline, exception and license condition with '+authority+'. '+applicability
  verifyzh=old['local_verification_zh']+' 向'+authorityzh+'核实实际渠道、表格、时限、例外和许可条件。'+applicabilityzh
  rec=dict(state_code=code,case_id=f'{code}-{i+1:04}',core_id=old['core_id'],family_id=old['family_id'],setting=old['setting'],topic=old['topic'],title=old['title'].split(' — ')[0]+' — '+lens,title_zh=old['title_zh'].split(' — ')[0]+' — '+lenszh,scenario=incident+' '+context,scenario_zh=incidentzh+contextzh,question=question,question_zh=questionzh,required=action,required_zh=actionzh,practical=approach,practical_zh=approachzh,records_best_practice=records,records_best_practice_zh=recordszh,verify=verify,verify_zh=verifyzh,source_leads=leads(code,topic),current_rule_verified=False,checked_date=None,review_status='editorial_style_revision',historical_first_presented=None)
  bookrows.append(rec);allrows.append(rec)
  # Keep article location, ID, data-setting and data-topic identical to the baseline.
  for child in list(card):card.remove(child)
  card.append(node('p',rec['case_id']+' · '+old['core_id']+' · '+old['family_id']+' · '+old['setting']+' · DRAFT',**{'class':'meta'}))
  h=node('h3',rec['title_zh']);h.append(node('br'));sp=node('span',rec['title'],lang='en',**{'class':'zh'});h.append(sp);card.append(h)
  pair(card,rec['scenario_zh'],rec['scenario']);pair(card,rec['question_zh'],rec['question'])
  details=node('details');details.append(node('summary','展开参考答案 / Reveal reference answer'))
  for heading,zhfield,enfield in [('必须事项（初稿） / Required actions (draft)','required_zh','required'),('实务处理 / Practical approach','practical_zh','practical'),('记录与最佳实践 / Records and best practice','records_best_practice_zh','records_best_practice'),('待确认事项 / Items to verify','verify_zh','verify')]:
   details.append(node('h4',heading));pair(details,rec[zhfield],rec[enfield])
  details.append(node('h4','官方资料查阅入口 / Official source leads'))
  for source in rec['source_leads']:
   p=node('p',**{'class':'meta'});p.append(node('a',source['label'],href=source['url']));details.append(p)
  pair(details,'现行核验未完成；没有新增核验日期或审核批准。','Current verification incomplete; no new checked date or reviewer approval has been created.')
  card.append(details);pair(card,'有即时危险时，立即启动相应应急处理，不等记录或练习完成。','For immediate danger, activate the appropriate emergency response now; do not wait for records or the exercise.')
  changes.append(dict(case_id=rec['case_id'],core_id=old['core_id'],family_id=old['family_id'],setting=old['setting'],change='Narrative incident with competing proposal; specific bilingual role question; required/practical/records/verification answer structure; original ID/filter attributes retained',current_rule_verified=False))
 out=ROOT/'books'/(code+'_'+state['state'].replace(' ','_')+'_Practice_Book.html');out.write_bytes(etree.tostring(tree,method='html',encoding='utf-8',doctype='<!doctype html>'))
 (DATA/(code+'_curriculum_1000.json')).write_text(json.dumps(bookrows,ensure_ascii=False,indent=2))
 manifest.append(dict(state_code=code,file='books/'+out.name,case_count=1000,source='Uploaded CA HTML' if code=='CA' else 'Repository WA edition 0.2; local file URL inaccessible',sha256=hashlib.sha256(out.read_bytes()).hexdigest(),baseline_css_sha256=hashlib.sha256(tree.xpath('//style')[0].text.encode()).hexdigest(),baseline_script_sha256=hashlib.sha256(tree.xpath('//script')[0].text.encode()).hexdigest()))
with (DATA/'CHANGE_REGISTER_2000.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=list(changes[0]),lineterminator='\n');w.writeheader();w.writerows(changes)
(ROOT/'manifest.json').write_text(json.dumps(dict(edition='WA/CA daily-training style rewrite',books=manifest,unique_underlying_situations=100,shared_tasks_per_situation=10,state_rule_verified_cases=0),indent=2))
# Reuse the original index styling and tile organization, now linking the two delivered books.
css=html.fromstring((A/'CA_baseline.html').read_bytes()).xpath('//style/text()')[0]
index='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>WA and CA bilingual daily-training practice books</title><style>'+css+'</style></head><body><main><h1>华州与加州托育案例练习<br>Washington and California Practice Books</h1><div class="notice"><p>参照每日训练案例写法改写；保留1,000题、25个主题、搜索、筛选、展开答案和打印。现行法规核验未完成，未把模板日期作为新核验日期。</p><p>Daily-training writing style, original book controls. Current legal verification remains incomplete; template dates are not newly verified dates.</p></div><div class="book-links">'
for b in manifest:index+='<a href="'+b['file']+'">'+b['state_code']+' · 1,000 bilingual exercises</a>'
index+='</div><p><a href="REVIEW_REPORT.md">改写说明 / Change notes</a> · <a href="data/CHANGE_REGISTER_2000.csv">题号对照 / Case register</a></p></main></body></html>'
(ROOT/'START_HERE.html').write_text(index)
print('Built 2 books, 2,000 state records, unchanged CSS and JS.')
