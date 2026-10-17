# Growing Together — Montessori planning & records, ages 3–6

A self-contained browser tool for a teacher or a single classroom device. No installation, account, subscription or server is needed to use it. It contains no external scripts, fonts, analytics or data uploads.

## Start here

1. Download `Montessori_Planning_and_Records_System.zip` from the repository and extract it.
2. Open **Montessori_Planning_and_Records.html** in a current desktop browser. GitHub’s file page shows the source, so download the file rather than trying to use it on GitHub.
3. Add a child profile. Dates of birth calculate age; ages do not trigger required lessons or deadlines.
4. Browse the lesson library and open a presentation outline. Choose **Plan** for an individual or a small group.
5. After an invitation, use **Record outcome** to record each child separately. Describe actual actions, words, support and a next opportunity. A plan’s status does not create a learning observation.
6. Review **Progress record** and **Reports**. Reports can be printed or saved as PDF using the browser’s print dialog.
7. In **Guide & backups**, export a **full JSON backup** regularly. CSV is a spreadsheet export, not a restorable backup.

The initial dataset has no children. The optional sample button adds clearly fictional records without replacing your own. Archive the sample children when finished.

## Included

| File | Purpose |
| --- | --- |
| `Montessori_Planning_and_Records.html` | Complete offline application, including the curriculum |
| `Printable_Planning_and_Record_Packet.pdf` | 12-page guide and blank paper forms |
| `Curriculum_Library_72.csv` | Spreadsheet-friendly lesson library |
| `curriculum.json` | Readable reference copy of the built-in curriculum |
| `validation_report.json` | Actual browser workflow checks and application hash |
| `tests/test_browser.py` | Reproducible development smoke tests |

The PDF includes a child profile, weekly plan, individual lesson plan, observation sheet and six area-specific progress records. The CSV and JSON reference files do not automatically update the HTML application. Add and edit your own lessons inside the application; custom lessons are included in full backups.

## Curriculum and planning approach

The 72 starter lessons cover practical life (14), sensorial (10), language (14), mathematics (16), cultural studies (12), and art/music/movement (6). Each outline has a direct aim, materials, readiness, presentation steps, point of interest, feedback/control of error, observation focus, possible next invitation, and safety/access considerations.

**Exploring → Developing → Extending** is a flexible teaching sequence, not a set of age bands. A child can work at different stages in different areas. Familiar work, repetition, child choice, inclusion and sustained work periods remain central. This is a broad introductory library, not a complete Montessori training album or an AMI/AMS-endorsed course. Trained staff should review and adapt presentations to their materials and tradition.

Status labels are **Interest observed**, **Presented**, **Practicing**, **Independent in observation**, and **Revisit / offer support**. “Independent” describes an event; it does not certify permanent mastery. “Not recorded” says nothing about a child’s ability. The progress bars show record coverage, not attainment or expected pace.

Progress uses the latest observation date for each child/lesson; same-day ties use record creation time. Editing an earlier entry preserves its original creation time. Reports include observations in the chosen period, and clearly label profile information as current rather than historical.

## Records and backups

- Records are stored in this browser profile on this device. There is no staff login, access control, encryption provided by the tool, cloud sync or automatic backup. Use one active editing tab at a time.
- Use a private classroom device and keep exported records secure. Device/browser privacy settings still apply. Keep medical, safeguarding, attendance, medication, incident and formal support records in approved systems.
- Browser cleanup, private browsing, a different browser, or moving/renaming the HTML file can make local records unavailable. Export before those changes. Local-file storage behavior varies by browser; if storage is unavailable, the app warns that the session is temporary.
- A failed storage write does not replace the previous dataset. If the app cannot read storage at startup, it keeps the unreadable saved data untouched and starts a temporary session with a visible warning.
- Restore checks structure, dates and linked records. It replaces the current dataset after confirmation, first requesting a backup download of the current records. Check that download before closing. Import limit: 10 MB. The built-in library is part of the HTML; backups contain profiles, plans, observations and custom lessons.
- Archiving a child keeps all linked records. Individual plans/observations can be deleted only after confirmation. Review accuracy and privacy before sharing a report.

## Verification

The functional suite checks creation and linking, chronological progress, custom lessons, report/CSV export, JSON backup and restore, invalid-backup rejection, archiving, mobile layout, offline rendering, invalid dates and storage failure. It uses fictional data in an isolated browser context. Test results do not establish professional endorsement or regulatory compliance.

For development only, install Playwright and Chromium, start an internal server from this directory with `python -m http.server 8771 --bind 127.0.0.1`, then run `python tests/test_browser.py` in a second terminal. The script uses `/usr/bin/chromium`; adapt that executable path for another development machine. Set `MONTESSORI_TEST_URL` if using a different internal test address. No server is needed by an end user.

The cloud browser blocks `file:` URLs by policy, so direct local-file behavior was not verified there. Functional checks used internal HTTP and a fulfilled standalone document with browser networking disabled. The HTML has no runtime dependency on the server or any separate file. The PDF was checked for 12 complete pages without orphaned form sections.
