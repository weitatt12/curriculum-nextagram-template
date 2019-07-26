from flask import Flask, Blueprint, render_template, redirect, flash, url_for
from flask_login import current_user
from models.user import User
from models.fan_idol import FanIdol

fans_idols_blueprint = Blueprint(
    'fans_idols', __name__, template_folder='templates')


@fans_idols_blueprint.route('/<idol_id>/create', methods=['POST'])
def create(idol_id):

    idol = User.get_or_none(User.id == idol_id) #this is to get everything from row from database 
    
    new_follower = FanIdol( #this is to create a new follower which takes in fan_id and idol_id (refer back to db)
        fan_id = current_user.id,
        idol_id = idol.id
    )

    new_follower.save()
    flash(f"You are now following {idol.name}")
    return redirect(url_for('users.show', username=idol.username)) #this need to refer back to users.show parameter, because it pass in username then here have to pass it into here


@fans_idols_blueprint.route('/<idol_id>/unfollow', methods=['POST'])
def unfollow(idol_id):

    idol = User.get_or_none(User.id == idol_id)

    relationship = FanIdol.get(FanIdol.idol==idol.id,FanIdol.fan==current_user.id)
    #this will help me wrap and get FanIdol (where, select your FanIdol.idol (from db) is equal to idol.id (from this funtion), select your FanIdol.fan (from db) comapre with current_user.id (from function))
    #this line 2 conditions need to be wrap it
    relationship.delete_instance() # this is something (using previous variable) delete using delete_instance() then save
    flash(f"You are now unfollow {idol.name}")
    return redirect(url_for('users.show', username=idol.username))
