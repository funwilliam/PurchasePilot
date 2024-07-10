import os
import dotenv
import argparse
from flask import Flask
from flask_migrate import Migrate
from waitress import serve
from app import utils, db, home as home_blueprint, api as api_blueprint

dotenv.load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    app.register_blueprint(home_blueprint, url_prefix='')
    app.register_blueprint(api_blueprint, url_prefix='/api')
    # app.config['SQLALCHEMY_DATABASE_URI'] = utils.make_postgresql_DBURL(
    #     os.getenv('DB_USER'),       # type: ignore
    #     os.getenv('DB_PASSWORD'),   # type: ignore
    #     os.getenv('DB_HOST'),       # type: ignore
    #     os.getenv('DB_PORT'),       # type: ignore
    #     os.getenv('DB_NAME'),       # type: ignore
    # )
    # app.config['SQLALCHEMY_DATABASE_URI'] = utils.make_access_DBURL('instance/DB-PurchasePilot.accdb') # 無法migrate
    app.config['SQLALCHEMY_DATABASE_URI'] = utils.make_sqlite_DBURL('DB-PurchasePilot.sqlite3')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    Migrate(app, db)

    return app
    
if __name__ == '__main__':
    app = create_app()
    parser = argparse.ArgumentParser(description='Run the Flask app.')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the Flask app on')
    args = parser.parse_args()
    serve(app, host='0.0.0.0', port=args.port, threads=8)
    # app.run(host='0.0.0.0', port=args.port, debug=True)