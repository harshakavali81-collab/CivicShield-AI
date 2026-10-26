.PHONY: setup test api web docker
setup:
	python -m pip install -e ".[dev]"
test:
	pytest -q
api:
	uvicorn backend.app.main:app --reload
web:
	cd frontend && npm run dev
docker:
	docker compose up --build
