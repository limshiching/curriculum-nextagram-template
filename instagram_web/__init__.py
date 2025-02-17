from app import app
from flask import render_template
from instagram_web.util.google_helpers import oauth
from flask_assets import Environment, Bundle
from .util.assets import bundles

assets = Environment(app)
assets.register(bundles)
oauth.init_app(app)

from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.images.views import images_blueprint
from instagram_web.blueprints.donations.views import donations_blueprint
from instagram_web.blueprints.fans_idols.views import fans_idols_blueprint

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(images_blueprint, url_prefix="/images")
app.register_blueprint(donations_blueprint, url_prefix="/donations")
app.register_blueprint(fans_idols_blueprint, url_prefex="fans_idols")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403

@app.errorhandler(410)
def page_not_found(e):
    return render_template('410.html'), 410

@app.errorhandler(500)
def internal_server_error(e):
    app.logger.error('Server Error: %s', (error))
    return render_template('500.html'), 500


@app.route("/")
def home():
    return render_template('home.html')
