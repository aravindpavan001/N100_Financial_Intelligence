.PHONY: load validate test report clean ratios dashboard api

# ============================
# Load SQLite Database
# ============================

load:
	python src/database/create_database.py
	python src/etl/loader.py

# ============================
# Run Data Validation
# ============================

validate:
	python src/validation/validator.py

# ============================
# Run Unit Tests
# ============================

test:
	pytest tests -v

# ============================
# Generate Validation Report
# ============================

report:
	python src/validation/validator.py

# ============================
# Future Sprint Targets
# ============================

ratios:
	@echo Ratio calculations will be implemented in Sprint 2.

dashboard:
	@echo Dashboard will be implemented in Sprint 2.

api:
	@echo API will be implemented in Sprint 3.

# ============================
# Clean Generated Files
# ============================

clean:
	@if exist nifty100.db del nifty100.db
	@if exist output\load_audit.csv del output\load_audit.csv
	@if exist output\validation_failures.csv del output\validation_failures.csv
	@echo Project cleaned successfully.