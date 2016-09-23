# Run a test server
from config import DEBUG
from app import app
app.run(host='0.0.0.0', port=3333, debug=DEBUG)
