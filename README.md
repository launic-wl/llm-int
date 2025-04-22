# Go to llm-int folder
cd <path-to>/llm-int/


# Create a new virtual environment
python3 -m venv venv

# Install Python Packages
pip install -r requirements.txt

# Install PyTorch for CPU
pip install torch --index-url https://download.pytorch.org/whl/cpu

# Start the python application (it will require time)
python main.py

