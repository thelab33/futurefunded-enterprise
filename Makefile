.PHONY: web api

web:
	cd apps/web && PYTHONPATH=../..:../../apps/web ../../.venv/bin/flask --app wsgi:app run --debug --host 127.0.0.1 --port 5000

api:
	cd apps/api && PYTHONPATH=../..:../../apps/api ../../.venv/bin/uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
