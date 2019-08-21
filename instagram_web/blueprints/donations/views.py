from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for
from instagram_web.util.braintree_helper import gateway
from instagram_web.util.helpers import send_email
from models.image import Image
from models.donation import Donation
from flask_login import current_user


donations_blueprint = Blueprint(
    'donations', __name__, template_folder='templates')


@donations_blueprint.route("/<image_id>/new", methods=["GET"])
def new(image_id):
    image = Image.get_by_id(image_id)
    client_token = gateway.client_token.generate()
    return render_template('donations/new.html', client_token=client_token, image=image)


@donations_blueprint.route("/<image_id>/payment", methods=["POST"])
def payment(image_id):
    nonce_from_the_client = request.form.get('payment_method_nonce')
    amount_from_the_client = request.form.get('donation_amount')
    image = Image.get_or_none(Image.id == image_id)

    if not amount_from_the_client or round(int(amount_from_the_client), 2) == 0:
        flash('Please donate a proper amount')
        return redirect(url_for('donations.new', image_id=image.id))

    if not nonce_from_the_client:
        flash('System error. Payment not made')
        return redirect(url_for('donations.new', image_id=image.id))

    result = gateway.transaction.sale({
        # "amount": 12,
        "amount": amount_from_the_client,
        "payment_method_nonce": nonce_from_the_client,
        "options": {
            "submit_for_settlement": True
        }
    })

    if not result.is_success:
        flash('Something went wrong. Contact your bank.')
        return redirect(url_for('donations.new', image_id=image.id))

    new_donation = Donation(
        user_id=current_user.id,
        amount=amount_from_the_client,
        image_id=image.id
    )

    new_donation.save()
    flash('Thank you for your donation')
    return redirect(url_for('users.show', image_id=image.id, username=current_user.username))

    # amount = amount_from_the_client
    # if result.is_success:
    #     flash(f'done! you have successfully donated {{amount}}')
    #     return redirect(url_for('donations.new'))
    # else:
    #     flash('error')
    #     return render_template('donations/new.html')

    # if donation.amount == "":
    #     return 'please enter a number'

    # if donation.save():
    #     flash('Donate Successful')
    #     return redirect(url_for('donations.new'))
