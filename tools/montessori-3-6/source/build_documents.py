from pathlib import Path
import json,csv
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
for name,file in [("MSSans","DejaVuSans.ttf"),("MSBold","DejaVuSans-Bold.ttf"),("MSSerif","DejaVuSerif.ttf")]:pdfmetrics.registerFont(TTFont(name,"/usr/share/fonts/truetype/dejavu/"+file))
R=Path(__file__).resolve().parents[1];d=json.loads((R/'curriculum.json').read_text());areas={a['id']:a for a in d['areas']}
with (R/'Curriculum_Library.csv').open('w',newline='') as f:
 w=csv.writer(f,lineterminator="\n");w.writerow(['ID','Area','Lesson','Flexible sequence','Direct aim','Materials','Readiness','Presentation outline','Point of interest','Feedback / control of error','What to observe','Possible next invitation','Safety and access'])
 for l in d['lessons']:w.writerow([l['id'],areas[l['area']]['title'],l['title'],l['stage'],l['aim'],l['materials'],l['readiness'],' / '.join(l['steps']),l['interest'],l['control'],l['observe'],l['nextStep'],l['safety']])
styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='BodyGreen',fontName='MSSans',fontSize=10,leading=15,textColor=colors.HexColor('#243d35'),spaceAfter=10));styles.add(ParagraphStyle(name='TinyGreen',fontName='MSSans',fontSize=8,leading=11,textColor=colors.HexColor('#40564b')));styles.add(ParagraphStyle(name='TitleGreen',fontName='MSSerif',fontSize=29,leading=33,textColor=colors.HexColor('#285346'),spaceAfter=16));styles.add(ParagraphStyle(name='SubGreen',fontName='MSBold',fontSize=13,leading=18,spaceBefore=9,spaceAfter=6,textColor=colors.HexColor('#285346')))
def P(t,style='BodyGreen'):return Paragraph(escape(t).replace('\n','<br/>'),styles[style])
def heading(t,subtitle=''):
 story.append(P(t,'TitleGreen'))
 if subtitle:story.append(P(subtitle))
def text(t):story.append(P(t))
def sub(t):story.append(P(t,'SubGreen'))
def lines(label,n=2):
 sub(label);table=Table([[''] for _ in range(n)],colWidths=[475],rowHeights=20);table.setStyle(TableStyle([('LINEBELOW',(0,0),(-1,-1),.4,colors.HexColor('#c7d2c7'))]));story.append(table);story.append(Spacer(1,3))
def table(headers,rows,widths,rowheight=None):
 data=[[P(str(x),'TinyGreen') for x in headers]]+[[P(str(x),'TinyGreen') for x in row] for row in rows]
 heights=None if rowheight is None else [30]+[rowheight]*len(rows)
 t=Table(data,colWidths=widths,rowHeights=heights,repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e7efe7')),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#c7d2c7')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]));story.append(t)
story=[]
heading('Growing Together','Montessori curriculum planning and record keeping | Ages 3-6 | Printable working packet')
text('Use this packet alongside Montessori_Planning_and_Records.html, or print blank copies for a paper-based workflow. The library contains 126 planning outlines and 766 photo-aligned tracking items. They support trained staff; they are not a complete Montessori training album or an endorsed certification course.')
sub('The working cycle')
for t in ['1. Observe: notice interests, movement, language and the support actually needed.','2. Plan: choose a few purposeful invitations linked to evidence. Keep familiar work available.','3. Present: invite, demonstrate clearly, allow a choice, and show restoration.','4. Step back: protect concentration and allow repetition; intervene for safety and meaningful support.','5. Record: write dated facts and a possible next opportunity. Revisit across time and contexts.']:text(t)
sub('Six connected areas')
for a in d['areas']:text(a['title']+': '+a['goal'])
sub('Privacy and storage')
text('The browser tool saves locally on the device, without accounts or automatic cloud backup. Export a full JSON backup regularly. Keep names and notes private. This system does not replace attendance, incident, medication, safeguarding or formal special-education records.')
text('Print to A4 or US Letter using “Fit to printable area.” Blank tracker dates are not age expectations or evidence of a learning gap.')
story.append(PageBreak())
heading('Sequence without deadlines','A mixed-age room offers different levels of work at the same time.')
for title,t in [('Exploring','Belonging, practical routines, coordinated movement, sensory comparison, oral language and concrete quantities. Offer accessible meaningful work and watch for readiness.'),('Developing','Longer sequences, finer comparisons, sound-symbol relationships, composing words, quantity-symbol connections and sustained inquiry. Keep earlier work available for repetition.'),('Extending','Reading for meaning, purposeful writing, concrete decimal operations, research, collaboration and creative projects. Greater complexity follows observable understanding, not a birthday.')]:sub(title);text(t)
sub('Observation labels')
for title,t in [('Interest observed','A child noticed or chose related work; this does not establish performance.'),('Presented','A lesson was demonstrated; further presentations may be useful.'),('Practicing','A child is working with the material. Record errors and the support used.'),('Independent in observation','The child worked without the recorded adult support in this event. Keep observing across days and contexts.'),('Revisit / offer support','Another invitation, a different material or additional support may help. Avoid labels about the child.')]:text(title+': '+t)
sub('Weekly review questions')
text('What did the child return to? What support helped? Which current plan is no longer useful? Where do we lack observations? Which materials need repair or adaptation? What family perspective would help?')
text('The separate three-year record book uses P for Presented, A for Assistance required, and I for Independent work in a dated observation. Year boundaries are set for each child, not fixed age bands.')
text('Do not turn coverage into a quota. “Not recorded” is a statement about the record, not the child’s ability. Include home languages and accessible communication, movement and materials.')
story.append(PageBreak())
heading('Child profile','Teaching information only. Use an identifier if a full name is unnecessary.')
lines('Child / identifier and date of birth',1);lines('Enrollment date and guide / key teacher',1);lines('Home languages and preferred communication',2);lines('Strengths and sources of confidence',3);lines('Current interests and repeated choices',3);lines('Useful access and teaching supports',3);lines('Family perspective and date of conversation',2)
text('Keep medical, safeguarding and formal support documents in the program’s approved systems. Review the profile when interests or supports change.')
story.append(PageBreak())
heading('Weekly invitations','Week of: ____________________   Guide / group: ____________________')
text('Plan a small number of purposeful invitations. Maintain complete familiar work, a protected work cycle, outdoor access and room for the child’s own choices.')
table(['Day / date','Child or small group','Invitation / evidence for readiness','Prepare / adapt','Outcome / follow-up'],[[day,'','','',''] for day in ['Monday','Tuesday','Wednesday','Thursday','Friday']],[60,80,145,90,100],75)
lines('Child-chosen work and emerging interests to revisit',3);lines('Environment preparation / repairs / family follow-up',2)
story.append(PageBreak())
heading('Individual lesson plan','Child / small group: ____________________   Date / guide: ____________________')
lines('Area, lesson and direct aim',2);lines('Observed readiness / relevant earlier work',2);lines('Materials, preparation and access supports',2);lines('Presentation sequence and restoration',4);lines('Point of interest and feedback / control of error',2);lines('Safety considerations and what to observe',2);lines('Possible next invitation, depending on the outcome',2)
story.append(PageBreak())
heading('Dated observation','Child / identifier: ____________________   Date / recorder: ____________________')
lines('Lesson / work and context of the invitation',2);lines('What was actually seen or heard? Include a brief quote if useful.',4);lines('Support actually given / how the child responded',3);lines('Engagement and self-chosen repetition',2)
sub('Status in this observation - circle one')
text('Interest observed | Presented | Practicing | Independent in observation | Revisit / offer support')
lines('Possible next invitation and when to revisit',3)
text('Example: “Poured twice. On the second attempt, stopped before the cup filled and wiped one spill without a reminder.” Avoid “Mastered water work.” A declined invitation is not a failure.')
def footer(canvas,doc):
 canvas.setFont('MSSans',8);canvas.setFillColor(colors.HexColor('#5d6f66'));canvas.drawString(45,25,'Growing Together | Montessori 3-6 | Staff working records');canvas.drawRightString(A4[0]-45,25,str(doc.page))
doc=SimpleDocTemplate(str(R/'Printable_Planning_and_Record_Packet.pdf'),pagesize=A4,rightMargin=45,leftMargin=45,topMargin=40,bottomMargin=42);doc.title='Montessori 3-6 Planning and Record Packet';doc.author='Growing Together';doc.build(story,onFirstPage=footer,onLaterPages=footer)
print('Created curriculum CSV and printable packet')
