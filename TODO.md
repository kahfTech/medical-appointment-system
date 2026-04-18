# Render Deploy Fix Progress

## Render Error: psycopg-binary==3.2.1 not available on Python 3.14 (Render default ignoring runtime.txt?)

**Next Steps (Updated):**
- [x] Previous local tests
- [ ] 1. Fix requirements.txt: psycopg[binary]==3.2.12 (available wheel)
- [ ] 2. Update runtime.txt: python-3.12.7 (stable, wheel support)
- [ ] 3. git add . && git commit -m "Fix psycopg Python 3.12" && git push
- [ ] 4. Render: Set env PYTHON_VERSION=3.12.7 + SECRET_KEY + DEBUG=False
- [ ] 5. Manual deploy "latest commit"

**Run locally first:** python manage.py migrate (Postgres needs DATABASE_URL env for full test)

