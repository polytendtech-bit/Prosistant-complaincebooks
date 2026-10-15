from pathlib import Path
import json,html,csv,hashlib,collections,zipfile,shutil
ROOT=Path(__file__).resolve().parent.parent;AUTH=ROOT/'authoring';BOOKS=ROOT/'books';DATA=ROOT/'data';BOOKS.mkdir(exist_ok=True);DATA.mkdir(exist_ok=True)
e=html.escape
original=json.loads((AUTH/'original_shared_curriculum.json').read_text());states=json.loads((AUTH/'state_registry.json').read_text())
familynotes={};teaching={}
for line in (AUTH/'family_notes.tsv').read_text().splitlines():
 n,change,action=line.split('\t');familynotes[int(n)]={'change':change,'action':action}
for line in (AUTH/'teaching_notes.tsv').read_text().splitlines():
 n,why,whyzh,actionzh=line.split('\t');teaching[int(n)]={'why':why,'whyzh':whyzh,'actionzh':actionzh}
LENSES=[
('First safe action','先做什么','State a practical first action. Explain how children remain supervised while it is done.','说出可行的第一步，并说明怎样保持儿童有人照看。'),
('Working alone','独自工作','You are the only qualified caregiver on site. What can you do now, and what must wait or use an approved backup plan?','现场只有你一位合格照护者。现在能做什么，什么需要推迟或采用获准备用方案？'),
('Explain a limit','解释界限','Someone asks you to skip a step. What will you explain, and what safe alternative will you offer?','有人要求省略一个步骤。你怎样解释，并提供什么安全替代安排？'),
('Handoff','交接','A qualified substitute will take over later. What facts, actions and unresolved points must you explain before the handoff?','合格代班人员稍后接手。交接前，要说清哪些事实、行动和未解决事项？'),
('Uncertain records','记录不明确','The record says the issue is resolved, but you cannot confirm it. What facts will you check and record without guessing?','记录说问题已解决，但你无法确认。你应核对和记录什么，怎样避免猜测？'),
('An offer of help','有人帮忙','A helper has not been approved for child-care duties. What help could you consider without handing over supervision or private records?','帮手尚未获准承担照护职责。你可考虑什么协助，同时不把看护或私人资料交给对方？'),
('Talk with a family','向家庭说明','What verified information about this situation can you explain to the affected family, and what must remain private or unresolved?','你可向受影响家庭说明什么已知事实，哪些隐私或未知情况需要保留？'),
('Prevent a repeat','防止重演','What practical change would reduce a repeat, and how could you check it without putting a child at risk?','什么实际改进可减少重演？怎样检查效果而不让儿童冒险？'),
('Find the local rule','查当地规则','What exact program, license category and current source must be identified before answering the legal part of this situation?','回答本情境的法律问题前，要先确认什么项目、许可类别和现行来源？'),
('Show what happened','说明处理经过','What truthful explanation and supporting record would show what you did, what worked and what is still unknown?','你会怎样如实说明做了什么、哪些有效、哪些仍未知，并提供什么记录？')]
CONTEXTS=[
('You are handling this situation while children are in care.','你处理这个情况时，仍有儿童在园。'),
('You operate a family child-care home and are the only qualified caregiver on site.','你经营家庭托育，现场只有你一位合格照护者。'),
('Someone asks you to skip a safety or verification step because it would be more convenient.','有人为图方便，要求省略安全或核实步骤。'),
('A qualified substitute will take over later and needs a specific briefing.','合格代班人员稍后接手，需要了解具体情况。'),
('The available record and a verbal account do not clearly agree.','现有记录和口头说法不完全一致。'),
('Someone offers practical help, but their permitted role has not been checked.','有人愿意帮忙，但其允许承担的职责尚未核实。'),
('The affected family asks for an explanation of what happened.','受影响家庭询问发生了什么。'),
('A similar problem has returned after an earlier reminder.','此前提醒过，但类似问题再次出现。'),
('A saved summary may be outdated or may concern a different license category.','保存的摘要可能过时，也可能针对其他许可类别。'),
('An authorized reviewer asks for the facts and the evidence supporting your response.','获授权的审阅人员要求了解事实和支持处理结果的资料。')]
source_ids=[['HEADSTART_SUPERVISION','CCDF'],['CCDF'],['CCDF'],['CCDF'],['NIH_SLEEP','CDC_SLEEP','CPSC_CRIB'],['CCDF','HEADSTART'],['CDC_ALLERGY'],['CCDF'],['CDC_DIAPER','CDC_HANDS'],['CDC_CLEAN','EPA'],['CCDF','HEADSTART'],['CCDF','HEADSTART'],['NY_REPORT','CCDF'],['NAEYC_DAP','HEADSTART'],['ADA_CHILDCARE','IDEA','HEADSTART'],['CCDF'],['NHTSA','HEADSTART'],['CCDF'],['CCDF'],['CCDF'],['ADA_CHILDCARE','CCDF'],['CCDF'],['CCDF'],['NAEYC_DAP','CDC_MILESTONES','IDEA'],['CCDF']]
core=[];change_rows=[]
for fi in range(1,101):
 base=original[(fi-1)*10];note=familynotes[fi];teach=teaching[fi];topic=(fi-1)//4
 title=base['title'].split(' — ')[0];titlezh=base['title_zh'].split(' — ')[0]
 incident=base['scenario'].removeprefix('You are responsible for a center group when this is discovered. Other children still need active supervision. ')
 incidentzh=base['scenario_zh'].removeprefix('你负责托育中心的一组儿童，发现这一情况时，其他儿童仍需要积极监管。')
 action=note['action'];actionzh=teach['actionzh'];why=teach['why'];whyzh=teach['whyzh']
 for vi,(lens,lenszh,q,qzh) in enumerate(LENSES):
  old=original[(fi-1)*10+vi];ctx,ctxzh=CONTEXTS[vi];a=action;azh=actionzh
  if vi==0:
   a+=' Keep children supervised while addressing the issue; do not let paperwork delay an urgent safety response.'
   azh+=' 处理时保持儿童有人照看；紧急安全行动不能等文书完成。'
  elif vi==1:
   if fi==1:
    a='Stay responsible for the child while the handoff is incomplete. If no eligible adult is actually available, do not send the child through the doorway alone. Keep children with you in a permitted, safely supervised area and use the approved contingency plan if safe care cannot continue.'
    azh='交接未完成前，继续负责照看。没有合格成人接手时，不让儿童独自穿过门口。让儿童留在允许且能安全照看的区域；不能持续安全照护时，采用获准应变方案。'
   elif fi==2:
    a='Use a bathroom arrangement that preserves safe supervision of all children without inventing a second caregiver. Keep supplies ready and use only an approved layout or backup plan. If the actual layout makes safe care impossible, use the permitted contingency process rather than leave the other children unattended.'
    azh='如厕安排须在没有第二位成人的实际条件下，也能安全照看所有儿童。备好用品，使用获准布局或备用方案。实际场所无法保证安全时，采用允许的应变流程，不能留下其他儿童无人照看。'
   else:
    a+=' Keep the children supervised. Delay non-urgent competing tasks. Use a backup caregiver only if their role is permitted and their eligibility is confirmed; if safe care cannot continue, use the applicable contingency plan.'
    azh+=' 继续照看儿童，推迟不紧急的冲突任务。只有核实职责和资格后才能用备用照护者；不能安全继续时，按适用应变方案处理。'
  elif vi==2:
   a+=' Explain the concern in plain language: '+why+' Offer the safe option described above, or pause the proposed activity while a permitted alternative is confirmed. Do not promise an exception you have not verified.'
   azh+=' 用简单话解释原因：'+whyzh+' 提供上述安全做法，或在核实允许的替代安排前暂停拟议活动。不承诺未核实的例外。'
  elif vi==3:
   a+=' Tell the substitute what was observed, what has been done, and what remains unresolved. Have them explain the next action in this particular situation before you transfer responsibility. Check role eligibility separately.'
   azh+=' 说清看到了什么、已做什么、还未解决什么；请代班人员复述本情境的下一步。实际交接前另行核实职责资格。'
  elif vi==4:
   a+=' Separate direct observations, another person\'s account and unknown facts. Preserve the original entry and add a dated correction or clarification through the record process. Do not postpone urgent care or an already-required report to make the accounts agree.'
   azh+=' 区分亲眼观察、他人转述和未知事实。保留原记录，按程序注明实际日期作更正或补充。不能为了统一说法拖延紧急照护或已经要求的报告。'
  elif vi==5:
   a+=' Keep child-care responsibility yourself unless an eligible person has formally accepted it. Consider only help allowed for that person, such as an approved non-care task that does not expose private information. Do not treat willingness as clearance or training.'
   azh+=' 没有合格人员正式接手时，你继续负责看护。只安排该人获准承担的工作，例如不涉及儿童照护和隐私的适当杂务。热心不等于完成审查或培训。'
  elif vi==6:
   a+=' Explain the verified facts affecting that family\'s child and the action actually taken. Say openly what is not yet known. Restrict unrelated private details, while fulfilling any separately applicable notice or reporting duty.'
   azh+=' 说明与该家庭儿童有关的已核实事实和实际行动，坦诚指出未知情况。限制无关隐私，同时履行另行适用的通知或报告义务。'
  elif vi==7:
   a+=' Turn this action into a checkable routine: name the responsible person and confirm that the relevant safeguard works during safe ordinary use or a simulation. Do not recreate a hazard with a child to test the change.'
   azh+=' 把这一做法变成可检查的日常步骤，明确负责人，在安全日常使用或模拟中确认有效。不让儿童再次处于危险来检验整改。'
  elif vi==8:
   a='The legal answer is unresolved in this edition. Identify the state and local jurisdiction, exact license or registration category, relevant ages and roles, and any program participation. Obtain the issuing authority\'s effective primary text and check its scope, exceptions, required action, recipient and timing. A saved summary or another state\'s rule is not enough. Meanwhile, preserve the general safety action: '+action
   azh='本版尚不能确定法律答案。先确认州和当地辖区、准确许可或注册类别、相关年龄和岗位及项目参与情况，再取得签发机构有效原文，核对范围、例外、行动、对象和时限。旧摘要或外州规则不够。一般安全做法仍应保持：'+actionzh
  else:
   a+=' Give the actual timeline, action, result and remaining uncertainty. Use accurate records relevant to this event. Do not backdate a checklist, invent a fact, or imply that an explanation proves legal compliance.'
   azh+=' 如实说明时间、行动、结果和未知情况，提供本事件相关记录。不倒签、不编造，也不把解释得好当成已证明合法合规。'
  applicability='Check the exact license category; center/home are practice settings, not legal classifications.'
  applicabilityzh='须核实准确许可类别；中心和家庭只是练习场景，不是完整法律分类。'
  if fi in (77,78,79,80):
   applicability='Household context: relevant only where these household facts exist. A commercial center without this context needs an adapted example or a not-applicable decision; do not infer a household duty from this exercise.'
   applicabilityzh='住户情境只适用于确有这些家庭事实的场所。不具备该情境的商业中心须改写案例或判断不适用，不能由此推定住户义务。'
  rec=dict(core_id=old['core_id'],family_id=old['family_id'],version='0.2-editorial-draft',topic=old['topic'],topic_zh=old['topic_zh'],setting=old['setting'],decision_lens=lens,decision_lens_zh=lenszh,title=title+' — '+lens,title_zh=titlezh+' — '+lenszh,scenario=incident+' '+ctx,scenario_zh=incidentzh+ctxzh,question=f'For “{title}”: '+q,question_zh=f'针对“{titlezh}”：'+qzh,model_answer=a,model_answer_zh=azh,rationale=why,rationale_zh=whyzh,everyday_teaching_note=action,everyday_teaching_note_zh=actionzh,practice_task=f'Use fictional facts to explain or demonstrate the response to “{title}”. Name the concern, show a feasible action and explain why it helps. Do not create the actual hazard.',practice_task_zh=f'用虚构资料说明或演示“{titlezh}”的处理：指出问题、展示可行行动并解释原因。不制造真实危险。',local_verification=old['local_verification'],local_verification_zh=old['local_verification_zh'],applicability=applicability,applicability_zh=applicabilityzh,source_leads=source_ids[topic],source_status='not_retrieved_proxy_403',review_status='editorial_revision_legal_review_pending',state_rule_verified=False,training_credit=False,assessment_status='unscored legal research task' if vi==8 else 'formative practice; not a validated exam',translation_status='AI editorial revision; independent bilingual review pending')
  core.append(rec)
  change_rows.append(dict(core_id=rec['core_id'],family_id=rec['family_id'],setting=rec['setting'],old_question=old['question'],new_question=rec['question'],old_answer=old['model_answer'],new_answer=rec['model_answer'],old_rationale=old['rationale'],new_rationale=rec['rationale'],family_recommendation=note['change'],applicability=applicability,legal_review='Unresolved; no official text retrieved',translation_review='Independent review pending',old_chinese_answer=old['model_answer_zh'],new_chinese_answer=rec['model_answer_zh'],old_chinese_rationale=old['rationale_zh'],new_chinese_rationale=rec['rationale_zh']))
(DATA/'revised_curriculum_1000.json').write_text(json.dumps(core,ensure_ascii=False,indent=2))
with (DATA/'CHANGE_REGISTER_1000.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=list(change_rows[0]),lineterminator='\n');w.writeheader();w.writerows(change_rows)
css='''body{font:17px/1.65 system-ui,"Noto Sans CJK SC",sans-serif;color:#193d39;margin:0;background:#f7f8f3}main{max-width:1050px;margin:auto;padding:28px 24px}h1,h2,h3{line-height:1.3}h1{font-size:34px}h2{margin-top:40px}.notice{background:#fff0ce;padding:18px;border-left:5px solid #a16c12}.case{background:white;border:1px solid #c9d8d0;border-radius:10px;padding:22px;margin:22px 0}.meta{font-size:13px;color:#53645c}.zh{color:#38574d}details{padding:12px;background:#edf4ef;margin-top:12px}summary{cursor:pointer;font-weight:700}button,select,input{font:inherit;padding:8px;border:1px solid #78988b;border-radius:5px}button{cursor:pointer}input[type=search]{width:100%;box-sizing:border-box}nav{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0}a{color:#005e63}.toolbar{background:#f7f8f3;padding:12px 0}article[hidden]{display:none!important}.legal{background:#fff5df;padding:10px}.book-links{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px}.book-links a{padding:12px;background:white;border:1px solid #c9d8d0}h4{margin-bottom:4px}@media print{body{background:white;font-size:10pt}main{padding:0;max-width:none}.toolbar,.no-print{display:none!important}.case{border:0;border-top:1px solid #aaa;padding:14px 0;break-inside:avoid}details{background:none;padding:0}details>summary{display:none}.notice{border:1px solid #999;background:none}}'''
script='''const cards=[...document.querySelectorAll('.case')],search=document.querySelector('#search'),topic=document.querySelector('#topic'),setting=document.querySelector('#setting');function filter(){let count=0;for(const c of cards){const show=(!search.value||c.textContent.toLowerCase().includes(search.value.toLowerCase()))&&(!topic.value||c.dataset.topic===topic.value)&&(!setting.value||c.dataset.setting===setting.value);c.hidden=!show;if(show)count++}document.querySelector('#count').textContent=count+' exercises shown / 个练习显示'}search.oninput=topic.onchange=setting.onchange=filter;document.querySelector('#show').onclick=()=>cards.filter(c=>!c.hidden).forEach(c=>c.querySelector('details').open=true);document.querySelector('#hide').onclick=()=>cards.forEach(c=>c.querySelector('details').open=false);let beforePrint=[];window.addEventListener('beforeprint',()=>{beforePrint=cards.map(c=>c.querySelector('details').open);cards.filter(c=>!c.hidden).forEach(c=>c.querySelector('details').open=true)});window.addEventListener('afterprint',()=>cards.forEach((c,i)=>c.querySelector('details').open=beforePrint[i]));document.querySelector('#print').onclick=()=>window.print();'''
def page(title,body,js=''):return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+e(title)+'</title><style>'+css+'</style></head><body><main>'+body+'</main>'+(('<script>'+js+'</script>') if js else '')+'</body></html>'
notice='''<div class="notice"><strong>Version 0.2 — editorial revision; current legal-source verification incomplete.</strong><p>These books support general child-care staff practice. All 50 editions reuse the same 1,000 exercises in 100 situation families, with ten guided tasks per family. They do not represent 50,000 independent cases or verified state-law answers.</p><p>Current federal and state source verification is incomplete. Use this edition for provisional practice, not as verified state-law guidance. No agency approval, training credit, or validated exam is claimed. Legal research exercises are unscored.</p><p lang="zh-Hans" class="zh">本版是语言与教学改进稿，现行官方资料尚未成功读取，法律审核未完成。50州共用100个情境系列、1,000个练习，不是50,000个独立或已核实法律案例。不代表政府批准，不授予培训学时，不是经验证的正式考试。查规则练习不计分。</p></div>'''
manifest=[]
for state in states:
 name=state['state'];code=state['code'];filename=code+'_'+name.replace(' ','_')+'_Practice_Book.html'
 body=f'<p class="no-print"><a href="../START_HERE.html">All books / 全部练习册</a> · <a href="../REVIEW_REPORT.md">Review report</a></p><h1>{e(name)} · Child-care staff practice book</h1><p lang="zh-Hans" class="zh">托育人员学习与练习册 · 2026-10-15 · 编辑改进版</p>'+notice
 body+=f'<h2>Learn first, then practice</h2><p>Read the short teaching note. Explain your response before revealing the suggested answer. Then try the demonstration with fictional facts. Keep real children, names, health details and family records out of practice materials.</p><p lang="zh-Hans" class="zh">先读教学提示，再自行回答，最后看建议答案。演示使用虚构资料，不放入真实儿童、健康或家庭信息。</p><p><a href="../STAFF_FOUNDATIONS.html">Read the foundation lessons / 阅读基础教学课</a> · <a href="../PRACTICE_ASSESSMENT_12.html">Try 12 practice questions / 试做12题</a></p>'
 body+=f'<h2>{e(name)} source route — not yet verified</h2><p><a href="{e(state["url"],quote=True)}">Supplied licensing entry point</a>. This link is a research lead. It has not supplied case-level legal verification in this review. Identify the exact license category and applicable local, protective-reporting, health and subsidy authorities before relying on a legal answer.</p>'
 body+='<div class="toolbar no-print"><label for="search">Search / 搜索</label><input id="search" type="search"><nav><select id="topic" aria-label="Topic"><option value="">All topics / 全部主题</option>'
 for ti in range(25):body+=f'<option value="{ti}">{e(core[ti*40]["topic"])}</option>'
 body+='</select><select id="setting" aria-label="Setting"><option value="">Both practice settings / 两类场景</option><option value="center">Center / 中心</option><option value="home">Family home / 家庭托育</option></select><button id="show">Study: show answers / 学习</button><button id="hide">Practice: hide answers / 练习</button><button id="print">Print / 打印</button></nav><p id="count" role="status" aria-live="polite">1,000 exercises shown</p></div>'
 for i,c in enumerate(core):
  if i%40==0:body+=f'<h2>{i//40+1}. {e(c["topic"])} <span lang="zh-Hans">{e(c["topic_zh"])}</span></h2>'
  cid=f'{code}-{i+1:04}'
  body+=f'<article class="case" id="{cid}" data-topic="{i//40}" data-setting="{c["setting"]}"><p class="meta">{cid} · {c["core_id"]} · {c["family_id"]} · {c["setting"]} · EDITORIAL DRAFT</p><h3>{e(c["title"])}</h3><p lang="zh-Hans" class="zh">{e(c["title_zh"])}</p><h4>Teaching note / 学习提示</h4><p>{e(c["everyday_teaching_note"])}</p><p lang="zh-Hans" class="zh">{e(c["everyday_teaching_note_zh"])}</p><h4>Situation / 情境</h4><p>{e(c["scenario"])}</p><p lang="zh-Hans" class="zh">{e(c["scenario_zh"])}</p><h4>Try it / 先回答</h4><p>{e(c["question"])}</p><p lang="zh-Hans" class="zh">{e(c["question_zh"])}</p><details><summary>Suggested answer and explanation / 建议答案与解释</summary><h4>A practical response / 可行处理</h4><p>{e(c["model_answer"])}</p><p lang="zh-Hans" class="zh">{e(c["model_answer_zh"])}</p><h4>Why it matters / 为什么</h4><p>{e(c["rationale"])}</p><p lang="zh-Hans" class="zh">{e(c["rationale_zh"])}</p><h4>Demonstrate / 演示练习</h4><p>{e(c["practice_task"])}</p><p lang="zh-Hans" class="zh">{e(c["practice_task_zh"])}</p><div class="legal"><h4>Applicability and local rule check / 适用范围与规则核实</h4><p>{e(c["applicability"])}</p><p lang="zh-Hans" class="zh">{e(c["applicability_zh"])}</p><p>{e(c["local_verification"])}</p><p lang="zh-Hans" class="zh">{e(c["local_verification_zh"])}</p><p class="meta">Source leads, not verified citations: {e(", ".join(c["source_leads"]))}. See <a href="../sources/SOURCE_CATALOG.csv">source catalog</a>. State rule verified: no. Independent bilingual review: pending. Assessment: {e(c["assessment_status"])}.</p></div></details><p class="meta">In immediate danger, use the appropriate emergency response now. / 遇到即时危险，立即采用相应应急行动。</p></article>'
  # No live records or learner answers are collected.
 path=BOOKS/filename;path.write_text(page(name+' staff practice · editorial revision 0.2',body,script));manifest.append(dict(state=name,code=code,file='books/'+filename,cases=1000,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
index='<h1>Prosistant · revised staff practice books</h1>'+notice+'<p><a href="REVIEW_REPORT.md">Review report and specific changes</a> · <a href="STAFF_FOUNDATIONS.html">Foundation lessons</a> · <a href="PRACTICE_ASSESSMENT_12.html">12-question practice assessment</a> · <a href="data/CHANGE_REGISTER_1000.csv">1,000-row change register</a></p><p>Extract the ZIP with its folders together and open this file in a browser. No account or internet access is needed to read the books; source links require access. Browser answers are practice feedback, not a validated exam.</p><div class="book-links">'
for b in manifest:index+=f'<a href="{b["file"]}">{e(b["state"])} · 1,000 draft exercises</a>'
index+='</div>'
(ROOT/'START_HERE.html').write_text(page('Revised child-care staff practice books',index))
(ROOT/'manifest.json').write_text(json.dumps(dict(version='0.2-editorial-draft',prepared_date='2026-10-15',state_editions=50,shared_exercises=1000,situation_families=100,exercise_records=50000,state_rule_verified_cases=0,source_research='Blocked by proxy 403',books=manifest),indent=2))
print('Built',len(manifest),'state editions and',len(core),'shared editorial exercises.')
