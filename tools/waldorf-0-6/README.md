# Waldorf-inspired curriculum: birth through age six

An original secular, inclusive adaptation for child-care settings. Not an accredited or endorsed Waldorf program.

Start with **Waldorf_Teacher_Guide.pdf** (26 pages). Use the seven age pathways from birth–5 months through five- and six-year-olds. Age bands guide planning, not child completion deadlines.

- **Waldorf_Activity_Library_70.pdf**: 70 original plans, ten per pathway. Each has purpose, materials, steps, adult role, observation, next opportunity, safety and access guidance.
- **Waldorf_Weekly_Rhythm_Menus.pdf**: seven age-matched weekly menus. Invitations remain flexible; infant care stays responsive.
- **Waldorf_Original_Stories_and_Verses.pdf**: six original short stories and seven optional verses, with age adaptations.
- **Waldorf_Planning_and_Observation_Forms.pdf**: five reproducible forms for planning, factual observations, family conversations, adaptations and project review.
- Matching `.docx` files are editable. Markdown guides are readable without a document application. The CSV and `curriculum.json` contain the 70 plans.

Core strands: relationships/rhythm; movement; useful work; oral language; imagination/social play; arts/music/handwork; nature/community. The approach protects free play and inclusion while supporting timely literacy, math, screening and individual services.

The three Waldorf organization sites could not be retrieved in this environment; see `source/RESEARCH_ATTEMPTS.json`. No verified alignment or endorsement is claimed. Review current local licensing, health and school requirements before implementation.

Rebuild with Python, ReportLab, python-docx and system DejaVu fonts:

```sh
python source/author_activities.py
python source/build_documents.py
python source/build_stories.py
```

The existing Montessori and play-based tools are separate and unchanged. No child records are included in this package.
