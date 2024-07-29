import os
import dotenv
import argparse
from flask import Flask
from config import config
from waitress import serve
from flask_migrate import Migrate
from app import db, home as home_blueprint, api as api_blueprint

dotenv.load_dotenv()

def create_app():
    config_name = os.getenv('FLASK_ENV', 'default')
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    app.config.from_object(config[config_name])
    app.register_blueprint(home_blueprint, url_prefix='')
    app.register_blueprint(api_blueprint, url_prefix='/api')

    db.init_app(app)
    Migrate(app, db)

    return app
    
if __name__ == '__main__':
    app = create_app()

    parser = argparse.ArgumentParser(description='Run the Flask app.')
    parser.add_argument('--port', type=int, default=int(os.getenv('FLASK_RUN_PORT', 3636)), help='Port to run the Flask app on')
    args = parser.parse_args()
    
    serve(app, host='0.0.0.0', port=args.port, threads=8)
    # app.run(host='0.0.0.0', port=args.port, debug=True)
    # app.run(host='0.0.0.0', port=3636, debug=True)