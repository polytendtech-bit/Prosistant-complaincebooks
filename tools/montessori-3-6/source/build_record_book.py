"""Printable blank three-year record, using original typesetting rather than photo reproduction."""
from pathlib import Path
import json
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4,landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
R=Path(__file__).resolve().parents[1];d=json.loads((R/'curriculum.json').read_text())
for name,file in [('RecordSans','DejaVuSans.ttf'),('RecordBold','DejaVuSans-Bold.ttf'),('RecordSerif','DejaVuSerif.ttf')]:pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
ink=colors.HexColor('#243d35');green=colors.HexColor('#e7efe7');line=colors.HexColor('#bfcbbf')
styles={k:ParagraphStyle(k,fontName=font,fontSize=size,leading=leading,textColor=ink,spaceAfter=after) for k,font,size,leading,after in [('title','RecordSerif',24,29,12),('body','RecordSans',9,13,9),('small','RecordSans',7,10,3),('tiny','RecordSans',6.3,8.4,0),('label','RecordBold',7,10,0)]}
def P(s,k='body'):return Paragraph(escape(str(s)).replace('\n','<br/>'),styles[k])
story=[P('Montessori three-year curriculum record','title'),P('Ages 3–6 | Name / identifier: ____________________________________ | Admission: ____________________'),P('Use P for Presented to child, A for Assistance required, and I for Independent work in that dated observation. Enter an observation date in the correct period and keep a separate factual note. An independent event is not permanent mastery. A blank cell means no recorded evidence, not inability.'),P('Year 1 starts: ____________________   Year 2 starts: ____________________   Year 3 starts: ____________________\nAfter Year 3 / exclusive end boundary: ____________________\nAge at each year’s start: Year 1 __________   Year 2 __________   Year 3 __________'),P('Set these dates to match the child’s actual school or record periods. A boundary belongs to the later year. Do not make Year 1, 2 or 3 into required age levels. Repeated evidence and practical support matter more than filling a table.'),P('The 11 supplied inventory photographs informed 365 normalized source rows and 766 tracking items. Many rows contain named variations. Nine entries are disclosed guide additions; four interpret the source phrase “slice parade.” Item IDs connect this book to the application and the source mapping CSV. Blank book-title lines in the originals were not filled with invented requirements.'),P('Guide-added entries and uncertain wording have short notes below their titles. The photos list curriculum items and record columns; they do not provide presentation procedures. The application’s 126 outlines are planning aids for trained staff, including the 72 preserved earlier outlines.'),P('How to use this book','title'),P('1. Pick an exercise that fits current interest and prior experience.\n2. Record which variation was offered and the support actually used.\n3. Enter one P, A or I event date; do not fill other columns automatically.\n4. Keep the full observation in the application or approved paper observation sheet.\n5. Revisit across days and contexts. Avoid age-based comparisons and completion quotas.'),P('Confidential staff working record. Keep child information and downloaded backups secure. This curriculum tool does not replace required health, incident, safeguarding or licensing records.','small')]
for area in d['areas']:
 story.append(PageBreak());story.extend([P(area['title'],'title'),P('Child / identifier: ____________________________________  Admission: ____________________','small'),P('Year 1: ______________ to ______________ | Year 2: ______________ to ______________ | Year 3: ______________ to ______________','small'),P('P = Presented | A = Assistance required | I = Independent in this observation. Enter dates, not permanent mastery checks.','small')])
 rows=[];last=None
 for s in [s for s in d['skills'] if s['area']==area['id']]:
  if s['section']!=last:
   rows.append([P(s['section'],'label')]+['']*9);last=s['section']
  text=s['id']+' · '+s['title']
  if s['origin']!='Normalized source entry':text+='\n'+s['origin']
  rows.append([P(text,'tiny')]+['']*9)
 data=[[P('Exercise / variation','label'),P('Year 1','label'),'','',P('Year 2','label'),'','',P('Year 3','label'),'',''],[P('Source photo and detailed notes: see PHOTO_CURRICULUM_MAP.csv','tiny')]+[P(k,'label') for _ in range(3) for k in ['P','A','I']]]+rows
 t=Table(data,colWidths=[298]+[50]*9,repeatRows=2,hAlign='LEFT')
 commands=[('GRID',(0,0),(-1,-1),.35,line),('BACKGROUND',(0,0),(-1,1),green),('SPAN',(1,0),(3,0)),('SPAN',(4,0),(6,0)),('SPAN',(7,0),(9,0)),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]
 for i,row in enumerate(rows,2):
  if isinstance(row[0],Paragraph) and row[0].style.name=='label':commands.extend([('SPAN',(0,i),(-1,i)),('BACKGROUND',(0,i),(-1,i),green)])
 t.setStyle(TableStyle(commands));story.append(t);story.append(Spacer(1,10));story.append(P('Additional child-led work / custom lessons: _________________________________________________________________','small'))
def footer(c,doc):
 c.setFont('RecordSans',7);c.setFillColor(ink);c.drawString(38,20,'Growing Together · Photo-aligned curriculum · P / A / I evidence · Keep confidential');c.drawRightString(landscape(A4)[0]-38,20,str(doc.page))
doc=SimpleDocTemplate(str(R/'Three_Year_Curriculum_Record_Book.pdf'),pagesize=landscape(A4),leftMargin=38,rightMargin=38,topMargin=32,bottomMargin=35,title='Montessori Three-Year Curriculum Record',author='Growing Together');doc.build(story,onFirstPage=footer,onLaterPages=footer)
print('Created blank three-year record book for all',len(d['skills']),'items.')
