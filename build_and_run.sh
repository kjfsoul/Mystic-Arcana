
#!/bin/bash

# Create a default .env file if it doesn't exist
if [ ! -f .env ]; then
  echo "Creating default .env file..."
  cat > .env << EOF
SECRET_KEY=mystic_arcana_secret_key
PASSWORD_SALT=mystic_arcana_salt
OPENAI_API_KEY=your_openai_api_key
STRIPE_SECRET_KEY=sk_test_your_test_key
STRIPE_WEBHOOK_SECRET=whsec_test_key
EOF
  echo ".env file created. Please update with your actual API keys."
fi

# Load environment variables
export $(grep -v '^#' .env | xargs)

# Initialize the database
echo "Initializing database..."
python init_db.py

# Start the application
echo "Starting Mystic Arcana application..."
python app.py
