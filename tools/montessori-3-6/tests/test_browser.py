from playwright.sync_api import sync_playwright,expect
from pathlib import Path
import json,tempfile,os,hashlib
R=Path(__file__).resolve().parents[1]
T=Path(tempfile.mkdtemp(prefix='montessori-tests-'))
TEST_URL=os.environ.get('MONTESSORI_TEST_URL','http://127.0.0.1:8791/Montessori_Planning_and_Records.html')
results=[]
def ok(name):results.append(name);print('PASS',name,flush=True)
with sync_playwright() as w:
 b=w.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 p=b.new_page(viewport={'width':1440,'height':1000},accept_downloads=True);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
 p.goto(TEST_URL);expect(p.get_by_role('heading',name='Room to grow')).to_be_visible();assert p.evaluate('BASE.length')==126
 ok('Fresh startup with 126 lessons and no invented child records')
 p.get_by_role('button',name='Add a child',exact=True).click()
 f=p.locator('#childForm');f.locator('[name=name]').fill('Sam Test');f.locator('[name=dob]').fill('2022-05-12');f.locator('[name=teacher]').fill('Guide One');f.locator('[name=interests]').fill('Water, plants and stories');f.locator('[name=strengths]').fill('Careful observer');f.get_by_role('button',name='Save',exact=True).click();assert p.evaluate('state.children.length')==1
 cid=p.evaluate('state.children[0].id');ok('Child profile creation and persistence')
 p.get_by_role('button',name='Lesson library',exact=True).click();assert p.locator('article.card').count()==126
 p.locator('#lessonSearch').fill('Pouring water');assert p.locator('article.card').count()==1;p.get_by_role('button',name='Lesson details',exact=True).click();expect(p.locator('#dialog')).to_contain_text('Flow control, stopping and cleanup');p.get_by_role('button',name='Plan this lesson',exact=True).click()
 f=p.locator('#planForm');f.locator('input[name=childIds]').check();f.locator('[name=focus]').fill('Revisit the pouring work after watching interest yesterday.');f.get_by_role('button',name='Save',exact=True).click();assert p.evaluate('state.plans.length')==1;assert p.evaluate('state.observations.length')==0
 ok('Library search, lesson detail and linked plan without invented progress')
 p.get_by_role('button',name='Record outcome',exact=True).click();f=p.locator('#observationForm');f.locator('[name=status]').select_option('practicing');f.locator('[name=objective]').fill('Poured twice and wiped one spill after a reminder.');f.locator('[name=independence]').fill('One verbal reminder.');f.locator('[name=nextStep]').fill('Offer the same work and wait before prompting.');f.get_by_role('button',name='Save observation',exact=True).click();assert p.evaluate('state.observations.length')==1;assert p.evaluate('state.plans[0].status')=='planned';ok('Individual outcome records evidence without changing group status')
 p.get_by_role('button',name='Progress record',exact=True).click();expect(p.locator('tr').filter(has_text='Pouring water')).to_contain_text('Practicing');ok('Progress record reflects latest linked observation')
 # A factual earlier record must not replace the latest record.
 p.get_by_role('button',name='Observations',exact=True).click();p.get_by_role('button',name='Record observation',exact=True).click();f=p.locator('#observationForm');f.locator('[name=lessonId]').select_option('L004');old=p.evaluate('dayAdd(today(),-2)');f.locator('[name=date]').fill(old);f.locator('[name=status]').select_option('presented');f.locator('[name=objective]').fill('Watched the first presentation.');f.get_by_role('button',name='Save observation',exact=True).click();assert p.evaluate(f"latest('{cid}','L004').status")=='practicing';ok('Backdated observations retain chronological progress')
 # Add and edit a custom lesson.
 p.get_by_role('button',name='Lesson library',exact=True).click();p.get_by_role('button',name='Add a custom lesson',exact=True).click();f=p.locator('#lessonForm');f.locator('[name=title]').fill('Care of classroom herb');f.locator('[name=aim]').fill('Care for a living classroom plant.');f.locator('[name=materials]').fill('Basil plant, small pitcher, cloth');f.locator('[name=readiness]').fill('Interest in plant care');f.locator('[name=steps]').fill('Observe the soil.\nAsk if water is needed.\nProvide a small amount and restore.');f.locator('[name=observe]').fill('Checks before watering.');f.get_by_role('button',name='Save',exact=True).click();assert p.evaluate('state.customLessons.length')==1;assert p.evaluate('lessons().length')==127;ok('Custom curriculum lesson creation')
 # Text stays text even with HTML content and spreadsheet formulas.
 assert p.evaluate("esc('<img src=x onerror=alert(1)>')")== '&lt;img src=x onerror=alert(1)&gt;'
 assert p.evaluate("csvCell('=1+1')")== '"\'=1+1"';assert p.evaluate("csvCell(' @SUM(1)')").startswith('"\'')
 malicious=p.evaluate('JSON.parse(JSON.stringify(state))');malicious['children'][0]['id']='x" onclick="alert(1)';assert p.evaluate('(d)=>{try{validate(d);return false}catch(e){return true}}',malicious);ok('HTML escaping, safe record identifiers and spreadsheet formula neutralization')
 # Report range and actual CSV contents.
 p.get_by_role('button',name='Reports',exact=True).click();expect(p.locator('.report-sheet')).to_contain_text('Sam Test');expect(p.locator('.report-sheet')).to_contain_text('Poured twice');
 with p.expect_download() as dl:p.get_by_role('button',name='Export observations CSV',exact=True).click()
 csv=Path(dl.value.path()).read_text(encoding='utf-8-sig');assert 'Sam Test' in csv and 'Poured twice' in csv
 p.emulate_media(media='print');assert not p.locator('aside').is_visible();assert p.locator('.report-sheet').is_visible();p.pdf(path=str(T/'Montessori_Test_Report.pdf'),format='A4',print_background=True);p.emulate_media(media='screen');ok('Date-filtered report, CSV download and printable PDF')
 p.locator('#reportFrom').fill(p.evaluate('dayAdd(today(),1)'));p.locator('#reportFrom').dispatch_event('change');expect(p.locator('.notice.error')).to_contain_text('valid date range');assert p.locator('.report-sheet').count()==0;ok('Invalid report dates blocked')
 # Export full backup, reload persistence, import it after a new child.
 p.get_by_role('button',name='Guide & backups',exact=True).click()
 with p.expect_download() as dl:p.get_by_role('button',name='Export full backup',exact=True).click()
 backup=T/'Montessori_Functional_Backup.json';dl.value.save_as(backup);saved=json.loads(backup.read_text());assert len(saved['observations'])==2
 p.reload();assert p.evaluate('state.children.length')==1 and p.evaluate('state.customLessons.length')==1;ok('Full JSON backup and reload persistence')
 p.get_by_role('button',name='Children',exact=True).click();p.get_by_role('button',name='Add a child',exact=True).click();f=p.locator('#childForm');f.locator('[name=name]').fill('Temporary child');f.locator('[name=dob]').fill('2021-04-10');f.get_by_role('button',name='Save',exact=True).click();assert p.evaluate('state.children.length')==2
 p.get_by_role('button',name='Guide & backups',exact=True).click();p.once('dialog',lambda d:d.accept());p.locator('#importFile').set_input_files(str(backup));expect(p.locator('#toast')).to_contain_text('Backup restored');assert p.evaluate('state.children.length')==1;assert p.evaluate('state.observations.length')==2;ok('Confirmed restore replaces data and preserves linked records')
 invalid=T/'invalid_montessori.json';bad=json.loads(backup.read_text());bad['observations'][0]['childId']='missing';invalid.write_text(json.dumps(bad));messages=[];p.once('dialog',lambda d:(messages.append(d.message),d.accept()));p.locator('#importFile').set_input_files(str(invalid));p.wait_for_timeout(250);assert messages and 'not imported' in messages[0];assert p.evaluate('state.children.length')==1;ok('Invalid backups rejected without data loss')
 # Archive preserves evidence.
 p.get_by_role('button',name='Children',exact=True).click();p.once('dialog',lambda d:d.accept());p.get_by_role('button',name='Archive',exact=True).click();assert p.evaluate('state.children[0].archived') and p.evaluate('state.observations.length')==2;p.locator('#archivedToggle').check();p.once('dialog',lambda d:d.accept());p.get_by_role('button',name='Restore child',exact=True).click();assert not p.evaluate('state.children[0].archived');ok('Archive and restore keep child history')
 # Mobile and every route render without page exceptions.
 p.set_viewport_size({'width':390,'height':844})
 for name in ['Overview','Children','Lesson library','Weekly plan','Observations','Progress record','Reports','Guide & backups']:
  p.get_by_role('button',name=name,exact=True).click();assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+2'),name
 p.get_by_role('button',name='Overview',exact=True).click();p.screenshot(path=str(T/'Montessori_Mobile.png'),full_page=True);ok('All eight views usable at 390px without page overflow')
 # Verify no external dependency is needed, even with network access disabled.
 q=b.new_page();q.context.set_offline(True);q.route('**/*',lambda r:r.fulfill(path=str(R/'Montessori_Planning_and_Records.html'),content_type='text/html'));q.goto('https://offline-test.invalid/');expect(q.get_by_role('heading',name='Room to grow')).to_be_visible();assert q.evaluate('BASE.length')==126;q.close();ok('Self-contained application renders with network access disabled')
 # A future observation must be rejected and preserve state.
 future=p.evaluate('JSON.parse(JSON.stringify(state))');future['observations'][0]['date']=p.evaluate('dayAdd(today(),1)');assert p.evaluate('(d)=>{try{validate(d);return false}catch(e){return true}}',future);ok('Future observations rejected')
 # Device write failure must not silently update the displayed or saved state.
 before=p.evaluate('state.children.length');p.evaluate("()=>{Storage.prototype.setItem=function(){throw Error('Test storage full')}}");alerts=[];p.once('dialog',lambda d:(alerts.append(d.message),d.accept()));p.evaluate("commit(s=>s.children.push({...s.children[0],id:'test-quota-child'}))");assert p.evaluate('state.children.length')==before and alerts and 'not saved' in alerts[0];ok('Storage write failure preserves the previous dataset')
 assert errors==[],errors;b.close()
(R/'validation_report.json').write_text(json.dumps({'application_sha256':hashlib.sha256((R/'Montessori_Planning_and_Records.html').read_bytes()).hexdigest(),'functional_checks_passed':len(results),'checks':results,'javascript_errors':errors,'browser':'Chromium / Playwright','direct_file_url_check':'not executed: environment browser policy blocks file URLs; functional tests used local HTTP and an intercepted offline document','legal_or_professional_endorsement':False},indent=2)+'\n')
print('ALL',len(results),'FUNCTIONAL CHECKS PASSED')
