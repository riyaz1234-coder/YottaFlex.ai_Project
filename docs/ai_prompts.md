# AI Prompt History & Reflection

**Prompt Used:** "Write a Python/Pandas pipeline that generates synthetic data, deduplicates customers based on email keeping the most recent, quarantines rows with nulls, and includes Pytest tests."

**AI Contribution:** Generated the initial boilerplate for Pandas `merge()` and the Pytest structures.

**My Validation & Changes:**
* I reviewed the deduplication logic. I ensured that `pd.to_datetime()` was applied to the `updated_at` column before sorting, to prevent string-sorting errors.
* I removed a strict reconciliation `assert` statement because a left-join can duplicate rows if a customer has multiple accounts, which would incorrectly crash the pipeline.