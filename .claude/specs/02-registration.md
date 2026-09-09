# Spec: Registration

## Overview
This feature implements account creation for Spendly. `GET /register` already renders `register.html`, but the form does not submit anywhere functional yet. This step adds the `POST /register` handler that validates input, prevents duplicate emails, hashes the password, and persists a new row in the `users` table — laying the groundwork for the login/session work that follows in Step 3.

## Depends on
- Step 1 (Database setup) — requires `get_db()`, `init_db()`, and the `users` table to already exist.

## Routes
- `GET /register` — renders the registration form — public (already implemented, unchanged)
- `POST /register` — validates and creates a new user account — public

## Database changes
No schema changes. The `users` table (`id`, `name`, `email`, `password_hash`, `created_at`) already supports this feature.

New functions to add to `database/db.py` (logic only, never inline in routes):
- `get_user_by_email(email)` — returns the matching user row, or `None`, using a parameterized `SELECT`. Used to check for duplicate emails before insert.
- `create_user(name, email, password_hash)` — inserts a new row into `users` via a parameterized `INSERT` and returns the new user's `id`.

## Templates
- **Create:** none
- **Modify:** `templates/register.html` — change the form's hardcoded `action="/register"` to `action="{{ url_for('register') }}"` (currently violates the no-hardcoded-URL rule); keep the existing `{% if error %}` block for surfacing validation/duplicate-email errors.

## Files to change
- `app.py` — change `register()` to accept `GET` and `POST`; on `POST`, validate required fields, check for duplicate email via `get_user_by_email`, hash the password, call `create_user`, and redirect to `/login` on success or re-render `register.html` with an `error` on failure.
- `database/db.py` — add `get_user_by_email(email)` and `create_user(name, email, password_hash)`.
- `templates/register.html` — replace hardcoded form action with `url_for('register')`.

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug (`generate_password_hash`)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- No DB logic inline in `app.py` — all queries live in `database/db.py`
- Use `abort()` for HTTP errors, not bare string returns
- All internal links use `url_for()` — never hardcode URLs
- Do not implement session/login behavior — that belongs to Step 3

## Definition of done
- [ ] `GET /register` still renders the form correctly
- [ ] Submitting the form with valid name, email, and password creates a new row in `users` with a hashed (not plaintext) password
- [ ] Submitting with an email that already exists shows an error on the page and does not insert a duplicate row
- [ ] Submitting with a missing required field shows an error and does not insert a row
- [ ] After a successful registration, the browser is redirected to `/login`
- [ ] The form's `action` uses `url_for('register')` instead of a hardcoded path
- [ ] No new entries added to `requirements.txt`
- [ ] All new queries in `database/db.py` use `?` placeholders
