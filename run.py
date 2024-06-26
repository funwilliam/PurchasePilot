import os
import dotenv
from flask import Flask
from flask_migrate import Migrate
from app import utils, db, home as home_blueprint

dotenv.load_dotenv()


def create_app():
    app = Flask(__name__, template_folder='app/templates',
                static_folder='app/static')
    app.register_blueprint(home_blueprint)
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
    app.run(debug=True)
