# Final audit commit marker

This commit adds an audit script scripts/audit_and_fix.py to help verify
that the repository does not import undefined config variables and that there
are no remaining usages of the deprecated Text filter from aiogram.filters.

Run this script locally after pulling main: python scripts/audit_and_fix.py
