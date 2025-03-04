
#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Initialize the database if needed
python init_db.py

# Run the application
python app.py
