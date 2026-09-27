# LinDelInt reporting protocol

LinDelInt implements the common issue-backed lifecycle in
`uibcdf/molsyssuite`'s `devguide/reporting_protocol.md`. That suite document
defines issue identity, statuses, closure evidence and bounded exceptions.

## Local paths and issue order

Open `uibcdf/lindelint#<number>` before adding a queued report. Use
`devguide/templates/report.md`, remove `severity` for a proposal and record
measurements in the developer guide. The GitHub issue holds public state and
settled facts. Suite-wide policy changes belong to `uibcdf/molsyssuite`.

- `devguide/pending_bugs/` holds open defects;
- `devguide/pending_proposals/` holds open proposals;
- `devguide/solved_bugs/` retains resolved historical defects;
- `devguide/archive/` holds other resolved, withdrawn and superseded reports.

The generated `devguide/archive/README.md` indexes both archive locations.
Broader design notes remain outside the queues until they describe one
independently closable theme.

## Closure

Set a closed status and date, name a relevant durable `guard` or `normative`
document, move the report to the appropriate archive and regenerate indexes.
Close the issue with the outcome, verification and archived path. Archive,
never delete. Correct a false archived claim with a dated appended note.

The default guard is a pytest selector in `tests/` or `devtools/tests/`; the
offline validator checks that the selected function, class method or test
module exists. A module selector must contain at least one test. Reviewers
still judge whether the assertion protects the reported mechanism.

The existing wheel-content guard has a local non-pytest profile: the sole
selector `devtools/scripts/check_wheel.py` means running
`python devtools/scripts/check_wheel.py <built-wheel.whl>` on the exact built
wheel. The validator requires the script's `main()` and executable entry
point; CI builds a wheel and invokes it. This profile applies only to that
script and does not admit arbitrary command text in report metadata.

## Offline checks

```bash
python devtools/devguide_index.py
python devtools/devguide_index.py --check
python -m unittest discover -s tests -p test_reporting_protocol.py
```

The index check and reporting tests run in the independent hosted governance
job, so unrelated scientific test failures do not hide a reporting defect.
