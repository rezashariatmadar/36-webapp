# React Migration Execution Plan (Archived)

This file is archived and reflects the older staged SPA migration strategy.
The repository now follows a hard-cutover architecture with frontend in `frontend/`.

Use these sources of truth instead:
- `plan.md` for the active migration scope and sequence.
- `README.md` for run/build/test commands.
- `config/urls.py` for backend route ownership.
- `frontend/src/App.tsx` for user-facing route ownership.

Legacy notes in this document that reference `theme/static_src`, template cutover flags,
or legacy shell routes are obsolete under the current architecture.
