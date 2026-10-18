# Growing Together — Early Learning Curriculum, birth through age six

An **original play-based, whole-child curriculum draft**, with responsive caregiving for infants/toddlers and guided play, inquiry and intentional teaching for older children. The final pathway includes 5- and 6-year-olds, through 83 months.

## Start here

Download and extract `Early_Learning_Curriculum_Birth_to_Six.zip` from the repository.

- Read **Birth_to_Six_Curriculum_Guide.pdf** for the center-wide organization and implementation approach.
- Use **Activity_Plan_Library_98.pdf** for individual learning invitations.
- Open **Early_Learning_Curriculum_and_Records.html** in a current browser for planning and records. No installation, account or server is needed. GitHub displays HTML source, so download the file before using it.

This is a separate resource from the Montessori 3–6 tool. Existing Montessori files and records were not changed. Their backups cannot be imported into this new system; they have different curricula and application identities.

## Research status

The user requested an approach selected after searching popular U.S. childcare curricula. A popularity search plus nine government, professional, publisher and health-reference requests were attempted. All failed with proxy CONNECT 403 errors, as did an additional escalated government-site request. No source body was retrieved.

The Creative Curriculum, HighScope and Frog Street are recognizable comparison candidates, but **no current nationwide popularity ranking or current primary-source review was verified**. The approach and lessons here are independently written using general established early-childhood knowledge. They do not reproduce a commercial curriculum, claim an endorsement or provide a verified market-share ranking. See [research basis and unresolved checks](source/RESEARCH_BASIS.md) and [actual retrieval log](source/RESEARCH_ATTEMPTS.json).

The Head Start ELOF connection is an illustrative organizational map, not a verified code-by-code alignment. The 5-/6-year-old bridge needs local school and state-standard review. Qualified educator, health/access and local program review should precede formal adoption.

## Organization

| Pathway | Organizing age range | Invitations |
| --- | --- | ---: |
| Young infants | Birth–5 months | 14 |
| Older infants | 6–11 months | 14 |
| Young toddlers | 12–23 months | 14 |
| Older toddlers | 24–35 months | 14 |
| Preschool | 3 years / 36–47 months | 14 |
| Pre-K | 4 years / 48–59 months | 14 |
| Kindergarten bridge | 5- and 6-year-olds / 60–83 months | 14 |

Each pathway includes two original invitations in each of seven learning areas:

1. Relationships & regulation.
2. Communication & early literacy.
3. Movement & self-care.
4. Thinking & mathematics.
5. Science & inquiry.
6. Creative expression.
7. Community & belonging.

Interest, engagement, persistence, flexibility, communication, co-regulation, help seeking and access cut across these areas. Age ranges organize possibilities; they are not milestone deadlines or a completion checklist.

The 48-slot map uses twelve flexible inquiry connections, each with four planning moves. Four additional weeks of a 52-week calendar remain flexible for closures, transitions, repetition and local priorities. Infants do not receive a weekly academic theme; keep responsive care and familiar routines stable.

## Included materials

| File | Use |
| --- | --- |
| `Birth_to_Six_Curriculum_Guide.pdf` / `.docx` | 26-page PDF guide; editable Word version |
| `Activity_Plan_Library_98.pdf` / `.docx` | 98 one-page activity plans; editable Word version |
| `Printable_Planning_and_Observation_Forms.pdf` / `.docx` | Six paper forms for profiles, plans, observations, team review and family conversation |
| `Activity_Library_98.csv` | Spreadsheet-friendly activity bank |
| `Flexible_48_Week_Map.csv` | Flexible center planning connections |
| `Early_Learning_Curriculum_and_Records.html` | Complete browser tool with embedded curriculum |
| `curriculum.json` | Canonical curriculum, pathways and planning map |
| `source/RESEARCH_BASIS.md` / `RESEARCH_ATTEMPTS.json` | Decision rationale, failed retrieval evidence and verification limits |
| `validation_report.json` / `pathway_validation.json` | Actual workflow, infant-pathway and data checks |
| `source/` / `tests/` | Editable source, rebuild helpers and repeatable development checks |

Each activity has a purpose, materials, starting point/access note, three possible interaction steps, observation focus, next opportunity, adaptations, family connection and safety check. The interaction is an invitation, not a required performance.

## Use the planning tool

1. Add a child profile, family priorities, communication preferences and useful supports.
2. Browse **Age pathways** or filter the **Activity library** by pathway, area and interaction style.
3. Plan a few individual/small-group invitations linked to actual observations. The **Year map** can provide an older-child inquiry connection; drafts do not create completed records.
4. Record an actual event, the support given and the child’s response. Responsive help/co-regulation is expected, especially for infants.
5. Use **Progress record** to review evidence. It defaults to activities with observations, not every future activity. Other pathway/reference views are available explicitly; their blank rows do not establish a gap.
6. Review **Reports**, then print to paper/PDF or export observation CSV as needed. Report profile fields are current, while observations follow the selected date range.
7. Export a **full JSON backup** regularly using **Guide & backups**. CSV is not a restorable backup.

Profiles start empty. An optional demo button adds clearly fictional samples without replacing existing records. Plan statuses do not create observations or certify learning. An independent strategy in one event is not permanent mastery or an infant goal.

## Storage, privacy and care

Records stay in the current browser profile on the current device. The tool has no staff login, access controls, application-level encryption, cloud synchronization or automatic backups. Use a private classroom device, one active editing tab and secure backups.

Browser cleanup, private mode, browser changes or moving/renaming the HTML file can make records unavailable. Export before those changes and restore the JSON in the new file if necessary. Restore validates the application identity, dates and linked records, then replaces data after confirmation; it first requests a current-record backup download. Check Downloads before closing. Import limit: 10 MB.

A failed storage write does not replace the previous dataset. Unreadable storage is kept untouched; the tool visibly starts a temporary session and asks you to export before closing. Archive a child to retain linked history. Deleting an individual plan/observation requires confirmation.

Needed care, safe sleep, feeding, comfort, supervision and individual plans always take priority. Activity safety checks do not replace current health rules or professional judgment. Attendance, health orders, medication, incidents, safeguarding and formal support records belong in approved systems. Review sensitive information before sharing any report or file.

## Development and verification

The application has no runtime package dependencies. For development, tests use Python, Playwright and Chromium at `/usr/bin/chromium`. From this directory, start an internal server with `python -m http.server 8793 --bind 127.0.0.1`, then run `python tests/test_browser.py` and `python tests/test_pathways.py` in another terminal. These use isolated fictional records and do not access the classroom’s actual browser data.

Use `python source/build_app.py` after editing the canonical JSON/template. `python source/build_documents.py` rebuilds the PDF, Word and CSV materials using ReportLab, python-docx and DejaVu fonts at `/usr/share/fonts/truetype/dejavu`. Editing a CSV/JSON alone does not change an already-built HTML file. Custom activities added inside the app are included in backups.

The cloud browser blocks direct `file:` URLs, so that mode was not verified there. Functional tests use internal HTTP and an intercepted standalone document with networking disabled. The app needs no server or separate files at runtime. Technical tests do not establish developmental validity, professional endorsement, current-source verification or regulatory compliance.
