# Washington and California books — daily-training style rewrite

## What this edition does

The supplied Washington DOCX is the writing and question/answer model. The supplied California HTML is the California layout baseline. The Washington baseline is the previously saved repository file, `reviews/revised-books-v0.2/books/WA_Washington_Practice_Book.html`. The `file:///Users/ruoyunzhen/Downloads/...` address points to the user's computer and could not be opened from this cloud environment. That local file was not silently claimed as inspected.

Both delivered HTML books retain 1,000 exercises, 25 topics, the existing case/core/family identifiers, and the center/home filter attributes. They retain the baseline CSS and JavaScript without changes. Search, topic and setting filters, show/hide answers, print behavior, responsive styling and links back to the book index remain available. The shared foundation and 12-question practice pages are retained as existing supplementary navigation, not newly rewritten or newly validated regulatory content.

## How the template was applied

The DOCX presents an incident with concrete facts, competing staff or family suggestions, and a decision for the director. It then separates required matters, practical handling, records/good practice, points to verify and official source references. The new books use that reading pattern rather than a short abstract incident plus a generic question.

- Wrote 100 fuller bilingual incident narratives, including a proposed shortcut or unresolved evidence.
- Wrote 100 matched English/Chinese questions about the actual incident.
- Retained ten guided decision tasks for each underlying situation: immediate response, working alone, pressure for an exception, handoff, conflicting accounts, an unverified helper, family explanation, prevention, an older rule summary and explaining the response.
- Each task adds facts and a follow-up decision. This preserves the original 1,000-exercise organization without pretending that every task is an independently authored underlying event.
- Each answer has five divisions: **必须事项（初稿） / Required actions (draft)**; **实务处理 / Practical approach**; **记录与最佳实践 / Records and best practice**; **待确认事项 / Items to verify**; **官方资料查阅入口 / Official source leads**.
- Chinese incident and question text is followed by its English version, as in the DOCX. English and Chinese answer paragraphs are paired in the same order.
- Removed the answer-revealing teaching note from before the question. The learner now reads the incident and question before opening the existing answer panel. The card-based layout and reveal interaction are retained.
- Adapted the working-alone doorway and bathroom versions so they do not rely on a nonexistent qualified second caregiver. Residential household scenarios and role-specific exercises retain applicability notes.
- Corrected named-person consistency in the doorway example and avoided inventing an adult intervention in the behavior record where the scenario says that outcome is unknown.

The DOCX places its answer key at the back. The HTML books deliberately retain answers inside their existing expandable panels, because the request also requires the original navigation and interactions. The question-first reading order and the answer divisions follow the DOCX; the location and operation of the answer panel follow the original books.

## Washington and California are separate jurisdictions

The Washington book uses relevant WAC/RCW discovery leads and refers to DCYF where appropriate. Washington provision numbers supplied in the DOCX are leads, not newly verified sources. Some topics require additional provisions not supplied by the template.

The California book uses California official discovery routes and identifies the actual license category and program for further review. Washington's WCCC, MERIT, DCYF-specific procedures, numeric training rules, drill intervals, mixing limits and reporting deadlines have not been copied into California answers. The absence of verified California detail is left unresolved rather than filled with a Washington rule.

## Verification dates and legal status

This task changes writing and presentation. The DOCX's statements that particular rules were checked on particular dates are supplied-document claims. They have not been adopted as current verification in the new books. `data/template_provenance.json` records the template's source links and stated check-date text with `independently_verified_here: false`.

Fresh access attempts to a Washington incident-rule URL and the California CDSS laws/regulations page again returned proxy `403 Forbidden`. No current primary text was read successfully in this task. No new checked dates, real reviewer approvals, training credits, official pass marks or government endorsements have been created. The new records keep `current_rule_verified: false` and `checked_date: null`.

The “Required actions (draft)” heading gives introductory safety and record-integrity safeguards. It is not a claim that every legal requirement, exception or local procedure has been mapped. Exact legal obligations still need effective primary text, applicability and qualified review. The official links are research starting points; loading or listing a link does not establish its current content.

## Files

Open `START_HERE.html` after extracting the ZIP with its folders intact. The two state books are in `books/`. Download HTML before opening it in a browser; GitHub normally shows HTML source rather than the interactive reader.

- `books/WA_Washington_Practice_Book.html`
- `books/CA_California_Practice_Book.html`
- `data/WA_curriculum_1000.json` and `data/CA_curriculum_1000.json`
- `data/CHANGE_REGISTER_2000.csv`
- `data/template_provenance.json`
- `validation_report.json` and `browser_validation.json`

Original inputs and prior editions are preserved. The retained authoring baselines and data allow the two new books to be rebuilt with `python authoring/build_books.py` (requires lxml). This rebuild does not verify legal sources. Technical validation results describe the actual structural and browser checks, not approval of the answers' legal accuracy or independent bilingual equivalence.
