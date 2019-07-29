from flask import Flask, Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user
from models.user import User
from models.fan_idol import FanIdol


fans_idols_blueprint = Blueprint('fans_idols',
                            __name__,
                            template_folder='templates/')


@fans_idols_blueprint.route('/<idol_id>/create', methods=['POST'])
def create(idol_id):
    #people to follow you in instagram from db

    idol = User.get_or_none(User.id == idol_id) #this will take bring me the rows from db

    new_follower = FanIdol(
        fan_id = current_user.id,
        idol_id = idol.id
    )
    #new follower is creating me the fan_id and idol_id from me in db

    new_follower.save() #this will help us save
    flash(f"You are now following {idol.name}")
    return redirect(url_for('users.show', id=idol.id))

@fans_idols_blueprint.route('/<idol_id>/unfollow', methods=['POST'])
def unfollow(idol_id):
    idol = User.get_or_none(User.id == idol_id)

    relationship = FanIdol.get(FanIdol.idol==idol.id, FanIdol.fan==current_user.id)

    relationship.delete_instance()
    flash(f"Unfollowed {idol.name}")
    return redirect(url_for('users.show', id=idol.id))

# @fans_idols_blueprint.route('/<idol_id>/approve', methods=['POST'])


# current_user.id == idol_id
# retrieve names of fan === request - list of fans



    # follow_fans_idols = request.form.get('follow')

    # user = User.get_by_id(id)
    
    # if request.form.get('follow'):
    #     fans_idols.approved = False
    

    # fan = User.get_by_id(id)

    




