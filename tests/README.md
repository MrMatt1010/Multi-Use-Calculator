# Tests Directory

This directory contains unit tests for the calculator project.

## Structure

- `test_main.py` — branch-specific unit tests for the current calculator implementation.

## Running tests

From the project root, run:

```powershell
python -m unittest discover -s tests
```

## Notes

- Each branch may have its own version of `tests/test_main.py` tailored to the branch-specific implementation.
- One test in each branch is intentionally written to fail and one to pass, as requested.
