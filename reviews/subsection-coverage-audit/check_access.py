from playwright.sync_api import sync_playwright
from pathlib import Path
import json,datetime,urllib.request
r=Path('/workspace/subsection_revision');rows=[]
urls=['https://app.leg.wa.gov/wac/default.aspx?cite=110-300-0345','https://www.cdss.ca.gov/inforesources/child-care-licensing/resources-for-providers/laws-and-regulations']
with sync_playwright() as w:
 b=w.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 for i,u in enumerate(urls):
  row={'url':u,'client':'Chromium default configured network','attempted_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()};p=b.new_page()
  try:
   response=p.goto(u,timeout=25000,wait_until='domcontentloaded');row.update(status=response.status if response else None,title=p.title(),text_excerpt=p.locator('body').inner_text()[:400]);(r/f'access_{i}.txt').write_text(p.locator('body').inner_text())
  except Exception as e:row['error']=str(e)[:700]
  rows.append(row);p.close()
 b.close()
for u in urls:
 row={'url':u,'client':'Python HTTPS after network grant'}
 try:
  with urllib.request.urlopen(u,timeout=20) as response:row.update(status=response.status,bytes=len(response.read()))
 except Exception as e:row['error']=str(e)
 rows.append(row)
(r/'access_diagnostics.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))
