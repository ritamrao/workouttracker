from app import create_app, db
from app.seed import seed_data
import os

app = create_app()

with app.app_context():
    db.create_all()
    seed_data()

if __name__ == '__main__':
    app.run(
        host=os.environ.get('FLASK_RUN_HOST', '127.0.0.1'),
        port=int(os.environ.get('FLASK_RUN_PORT', 5000)),
        debug=os.environ.get('FLASK_DEBUG', '0') == '1'
    )