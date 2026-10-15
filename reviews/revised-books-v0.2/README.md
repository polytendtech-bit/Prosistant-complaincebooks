# Revised child-care staff practice books — editorial edition 0.2

Open [START_HERE.html](START_HERE.html) after downloading and extracting the ZIP. GitHub normally displays HTML source rather than running these local reading tools.

Read [the review report](REVIEW_REPORT.md) for the findings, specific changes, source-access blocker, and remaining legal and bilingual review.

This edition contains 50 state-organized books sharing 1,000 guided exercises in 100 situation families, plus eight foundation lessons and 12 formative practice questions. It is a provisional editorial resource, not a completed current-law review, an approved training-credit course, or a validated exam.

The 1,000-row change register is in `data/CHANGE_REGISTER_1000.csv`. Source access outcomes are in `sources/SOURCE_CATALOG.csv`. No official text was successfully retrieved. No state-law verification or reviewer approval has been fabricated.

The books are self-contained HTML with relative links to shared lessons. They do not collect or send learner responses. Cloud-browser checks used an internal HTTP test server because that browser blocks direct file navigation. Test evidence is in `validation_report.json` and `browser_validation.json`.

`authoring/build_revised.py` rebuilds the shared curriculum and 50 books from the retained authoring data using Python's standard library. Shared supplemental pages are separately maintained editorial files. `authoring/validate_revised.py` reruns structural checks and requires lxml; it resets browser validation to pending until actual browser results are incorporated. Do not treat these checks as legal validation.
