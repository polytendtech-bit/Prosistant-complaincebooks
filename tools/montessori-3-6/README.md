# Growing Together — Montessori planning & records, ages 3–6

Version 2 adapts your eleven curriculum photographs into a detailed planning and record-keeping system. It is a self-contained browser tool for a teacher or single classroom device, with no installation, account, subscription or server required. No external scripts, fonts, analytics or data uploads are used.

## Download and open

Download `Montessori_Planning_and_Records_System.zip` from the repository, extract it, and open **Montessori_Planning_and_Records.html** in a current desktop browser. GitHub’s HTML file page shows source code; download rather than trying to use the application on GitHub.

**If you already used version 1:** export a full JSON backup from the old file before replacing or moving it. The new version accepts that backup. Use **Guide & backups → Restore a backup** if your records are not visible in the new file, then export a new version 2 backup. Restore replaces the current dataset after confirmation and first requests a download of the current records. If you have started new records in version 2, back them up before restoring anything; restore does not merge datasets.

The same browser origin and storage key can read and migrate the older stored format directly. Local-file storage can vary with browser and file location, so a downloaded backup is the reliable transfer route. Version 1 remains in `tools/archive/Montessori_Planning_and_Records_System_v1.zip` in the repository.

## What your photos added

- **126 planning outlines:** the original 72 and 54 new guide-authored outlines for missing material families.
- **766 tracking items in 59 sections**, connected to 365 normalized source rows across all 11 photos. Material variations are separate: jug-to-jug and jug-to-three-cups pouring, letter identities, reading sets, handwriting formats, static/dynamic operations, geography stages and biology language/label/definition/booklet work.
- **Three-year P/A/I records:** P = Presented to child, A = Assistance required, I = Independent work in that dated observation. Set four explicit date boundaries for each child; these are school/record periods, not ages or deadlines.
- Exact variation links in lesson plans and outcome forms, dated evidence history, support notes, follow-up reminders, filtered record printing/CSV and richer individual reports.
- Compatible loading and restore of version 1 records, preserving IDs, notes, dates, custom lessons and links without inventing new specific-skill evidence.

The 766 items are an adapted inventory, not 766 verbatim printed lines. Nine are disclosed guide additions, including q and x omitted in the photo’s alphabet list; four interpret “slice parade.” Names, set numbers and unclear content are documented rather than turned into invented procedures. See [source review notes](source/REVIEW_NOTES.md) and [item-to-photo mapping](source/PHOTO_CURRICULUM_MAP.csv).

| Area | Planning outlines | Tracking items |
| --- | ---: | ---: |
| Practical life | 26 | 98 |
| Sensorial | 18 | 77 |
| Language | 25 | 189 |
| Mathematics | 26 | 210 |
| Cultural studies | 21 | 178 |
| Art, music & movement | 10 | 14 |
| **Total** | **126** | **766** |

## A practical workflow

1. **Children:** add a profile with strengths, interests, language, useful supports and a key teacher. The system starts with no children. Optional sample records are clearly fictional.
2. **Set the record years:** edit the child’s profile and enter Year 1 start, Year 2 start, Year 3 start, and the exclusive end boundary after Year 3. You can suggest enrollment anniversaries, then edit them to match your school years. Leave all four blank until known.
3. **Three-year record:** choose an area/section or search a specific exercise. Use Details for its source and linked planning outline. Plan an individual or small-group invitation based on actual readiness.
4. **Weekly plan:** keep a few purposeful invitations within a protected work cycle and leave room for repetition and child-chosen work. Planned/presented plan statuses do not generate learning observations.
5. **Record an outcome:** select the exact variation, write what was seen/heard, note actual support and choose a P/A/I tag when appropriate. An A tag needs a support note. Changing P/A/I adjusts the broad observation status; practice alone does not imply assistance.
6. **Revisit:** review the latest dated evidence and follow-up reminders. “Plan next invitation” carries the exact variation and the observation’s evidence into a draft plan. Reminders are teacher invitations, not child performance deadlines.
7. **Share thoughtfully:** review an individual report before printing to paper/PDF or exporting CSV. For the wide three-year table, print in landscape; area/section filters let you print just the needed work.
8. **Back up:** export a full JSON backup regularly, before browser cleanup and before moving/replacing files. CSV exports cannot restore the system.

## Read the records accurately

The broader observation statuses remain Interest observed, Presented, Practicing, Independent in observation, and Revisit / offer support. The original progress view gives the newest dated evidence linked to a planning outline; one specific variation does not establish independence across that whole material family.

The three-year table shows separate P/A/I columns for each exact tracking item. Each cell shows the latest event date for that tag/period, with × when more than one event exists. Open a date for the full history. CSV exports include all matching dates. A boundary date belongs to the later period; evidence outside the configured periods remains in the observation history. Changing boundaries never rewrites observation dates.

Older broad lesson records keep blank specific-variation, P/A/I and year fields until you deliberately add the information. An independent observation is one event, not permanent mastery. Blank cells mean no linked record in that period, not inability, absence, delay or a requirement to catch up. Coverage bars are not attainment scores. Exploring, Developing and Extending remain flexible sequences, not age bands.

## Included files

| File | Purpose |
| --- | --- |
| `Montessori_Planning_and_Records.html` | Complete application, including all curriculum data |
| `Printable_Planning_and_Record_Packet.pdf` | Six-page guide and blank profile, weekly plan, lesson plan and observation forms |
| `Three_Year_Curriculum_Record_Book.pdf` | 45-page landscape blank record book for all 766 items |
| `Curriculum_Library.csv` | Spreadsheet-friendly 126-outline library |
| `curriculum.json` | Editable canonical curriculum, source rows and tracking items |
| `source/PHOTO_CURRICULUM_MAP.csv` | Every item linked to its source photo and normalization notes |
| `source/PHOTO_REVIEW_MANIFEST.json` | Names, hashes, per-photo counts and source-review scope |
| `source/REVIEW_NOTES.md` | Exact adaptation choices and limits |
| `validation_report.json`, `photo_record_validation.json` | Actual browser workflow and migration test results |
| `source/build_*.py`, `source/app_template.html` | Editable template and rebuild helpers |
| `tests/` | Reproducible browser checks with fictional data |

Editing JSON or CSV alone does not change an already-built HTML file. Use **Add a custom lesson** in the application for classroom additions; they are included in backups. Developers can edit the canonical JSON/template and rebuild the HTML.

## Device storage and privacy

Records stay in this browser profile on this device. This tool has no shared staff login, access controls, encryption provided by the application, cloud sync or automatic backup. Use a private classroom device, one active editing tab and secure backups. Browser cleanup, private browsing, browser changes or moving/renaming the HTML file can make saved data unavailable.

A failed storage write does not replace the previous dataset. If storage cannot be read on startup, the old saved value is kept untouched and the app visibly starts a temporary session; export before closing it. Restore validates dates, IDs and links before replacing records. Import limit: 10 MB. Backups contain profiles, plans, observations and custom lessons; the built-in library is part of the HTML.

Archive a child to retain linked history. Deleting an individual plan/observation requires confirmation. Review names, quotations and sensitive context before sharing reports. Medical, safeguarding, attendance, medication, incident and formal support records belong in the program’s approved systems, not this curriculum tool.

## Professional scope

The photos provide an inventory and P/A/I columns, not a complete training album. All presentation outlines are planning aids for trained staff to review against actual materials, language and training tradition. No AMI/AMS endorsement, standardized assessment or regulatory approval is claimed. Advanced extensions and tools are optional and subject to individual readiness and safety review. Respect the child’s choice, home languages, communication, mobility, sensory preferences and dignity.

## Development checks

No server or packages are needed by an end user. For development, the supplied browser scripts use Python, Playwright and Chromium at `/usr/bin/chromium`. From this directory, start `python -m http.server 8791 --bind 127.0.0.1` for internal testing, then run `python tests/test_browser.py` and `python tests/test_photo_records.py` in a second terminal. Set `MONTESSORI_TEST_URL` for another internal address. These tests use isolated fictional records and never access a user’s classroom browser data.

Rebuild the application with `python source/build_app.py`. The optional PDF/CSV helpers are `python source/build_documents.py` and `python source/build_record_book.py`; they use ReportLab and installed DejaVu fonts at `/usr/share/fonts/truetype/dejavu`. Review outputs after editing content. Rebuilding does not itself rerun tests or update the downloadable archive.

The cloud browser blocks `file:` URLs by policy, so direct local-file behavior was not verified there. Functional tests use internal HTTP and an intercepted standalone document with browser networking disabled. The HTML has no runtime dependency on that server or separate files. The two PDFs were checked for all expected forms and tracking IDs.
