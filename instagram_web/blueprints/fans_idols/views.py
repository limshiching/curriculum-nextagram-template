from models.user import User
from models.fan_idol import Fan_Idol
from flask_login import current_user

fans_idols_blueprint = Blueprint('fans_idols',
                            __name__,
                            template_folder='templates/')

@fans_idols_blueprint.route('/new', methods=['GET'])
def new():
    users = User.select()
    return render_template('')

@fans_idols_blueprint.route('/<name>/follow', methods=['POST'])
def follow(name):



