# Spec: Login and Logout

## Overview
This feature implements real authentication for Spendly: a working `POST /login` handler that verifies credentials against the `users` table and starts a Flask session, and a working `GET /logout` that ends that session. Registration (Step 2) already creates hashed-password users but has no way to sign them in; `GET /login` currently just renders a form with nowhere to POST to, and `GET /logout` is a raw-string stub. This step wires the two together so a registered user can actually authenticate and the app has a session-based concept of "logged in," which every later step (profile, expenses) depends on.

## Depends on
- Step 1 (Database setup) — `users` table, `get_db()`, `PRAGMA foreign_keys = ON`
- Step 2 (Registration) — `create_user`, `get_user_by_email`, werkzeug password hashing conventions

## Routes
- `POST /login` — validate email/password against `users` table, start session on success, re-render `login.html` with an error on failure — public
- `GET /logout` — clear the session and redirect to the landing page — logged-in (safe no-op if no session exists)

`GET /login` stays as-is (already implemented, renders `login.html`).

## Database changes
No database changes. The existing `users` table (`id`, `name`, `email`, `password_hash`, `created_at`) and `get_user_by_email(email)` already provide everything needed to verify credentials. No new tables, columns, or `database/db.py` functions are required.

## Templates
- **Create:** none
- **Modify:**
  - `templates/login.html` — fix hardcoded `action="/login"` to `action="{{ url_for('login') }}"`; ensure the existing `auth-error` block renders a flashed/passed error message on failed login
  - `templates/base.html` — nav currently always shows "Sign in" / "Get started"; add a conditional (based on `session.get('user_id')`) so a logged-in user sees a "Logout" link (`url_for('logout')`) instead

## Files to change
- `app.py` — set `app.secret_key`; add `from flask import session`; implement `POST /login` (fetch user via `get_user_by_email`, verify with `check_password_hash`, set `session['user_id']` and `session['user_name']` on success, redirect to `url_for('index')`; on failure re-render `login.html` with an error and no session set); implement `GET /logout` (call `session.clear()`, redirect to `url_for('index')`)
- `templates/login.html` — fix form action, surface login error
- `templates/base.html` — conditional nav for logged-in/logged-out state

## Files to create
None.

## New dependencies
No new dependencies. `check_password_hash` comes from `werkzeug.security`, already a transitive Flask dependency and already used (as `generate_password_hash`) in registration.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug (`check_password_hash` for verification — never compare plaintext)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- `app.secret_key` must be set (e.g. read from an environment variable with a dev-only fallback) — never commit a real production secret
- Do not implement `/profile` or `/expenses/*` routes — they remain stubs until their own steps
- `GET /logout` must render/redirect properly, never a raw string return

## Definition of done
- [ ] Visiting `/login` and submitting `demo@spendly.com` / `demo123` (seeded user) logs in successfully and redirects to `/`
- [ ] Submitting `/login` with a wrong password re-renders `login.html` with a visible error and does not create a session
- [ ] Submitting `/login` with a non-existent email re-renders `login.html` with a visible error and does not create a session
- [ ] After a successful login, the nav in `base.html` shows "Logout" instead of "Sign in" / "Get started"
- [ ] Visiting `/logout` while logged in clears the session and redirects to `/`, and the nav reverts to "Sign in" / "Get started"
- [ ] Visiting `/logout` while not logged in does not error — it redirects to `/` cleanly
- [ ] Refreshing the page after login keeps the user logged in (session persists)
- [ ] `login.html`'s form no longer has a hardcoded `/login` action — it uses `url_for('login')`
- [ ] No plaintext passwords appear in logs, DB rows, or session data
