from app import db, create_app
from config import ProductionConfig, DevelopmentConfig
from flask_migrate import Migrate
import sys


# if "--debug" in sys.argv:
#     app = create_app(DevelopmentConfig)
# else:
#     app = create_app(ProductionConfig)

app = create_app(DevelopmentConfig)

migrate = Migrate(app, db, compare_type=True)

if __name__ == '__main__':
    app.run()
