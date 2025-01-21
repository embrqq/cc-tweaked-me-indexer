build_app:
	docker compose build app

init_db: build_app
	docker compose run app python db_setup.py
	docker compose down

run: build_app
	docker compose up app

up_db:
	docker compose up -d db

clean:
	docker compose down
