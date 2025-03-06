.PHONY: install setup run clean

# Install Python dependencies
install:
	pip install -r requirements.txt

# Full setup (Install dependencies & guide user for Tesseract installation)
setup: install
	@echo "Setup complete. Ensure Tesseract OCR is installed and configured."

run:
	python main.py

# Clean virtual environment
clean:
	rm -rf .venv
