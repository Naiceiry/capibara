import os
from flask_admin import Admin
from .models import db, Country, Review, Presupuesto
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    admin.add_view(ModelView(Country, db.session))
    admin.add_view(ModelView(Review, db.session))
    admin.add_view(ModelView(Presupuesto, db.session))
     
    