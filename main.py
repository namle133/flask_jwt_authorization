from router import account
from flask import Flask
from flask_jwt_extended import JWTManager
import os

app = Flask(__name__)
# Configuration for JWT
app.config['JWT_SECRET_KEY'] = os.getenv("SECRET_KEY")

jwt = JWTManager(app)
# Register blueprints
app.register_blueprint(account.bp)
    
if __name__ == '__main__':
    app.run(debug=True)
    
 
    