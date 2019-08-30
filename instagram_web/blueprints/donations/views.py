from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for
from instagram_web.util.braintree_helper import gateway
from instagram_web.util.helpers import send_email
from models.image import Image
from models.donation import Donation
from flask_login import current_user
import braintree

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

    result = gateway.transaction.sale( {
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
    # flash('Thank you for your donation')
    # return redirect(url_for('users.show', image_id=image.id, username=current_user.username))
    return redirect(url_for('donations.show_checkout', transaction_id=result.transaction.id))

#************************************************************************************************************************
TRANSACTION_SUCCESS_STATUSES = [
    braintree.Transaction.Status.Authorized,
    braintree.Transaction.Status.Authorizing,
    braintree.Transaction.Status.Settled,
    braintree.Transaction.Status.SettlementConfirmed,
    braintree.Transaction.Status.SettlementPending,
    braintree.Transaction.Status.Settling,
    braintree.Transaction.Status.SubmittedForSettlement
]

@donations_blueprint.route('/donate-to/<image_id>', methods=["GET"])
def new_checkout(image_id):
    client_token = generate_client_token()
    return render_template("donations/new.html", client_token=client_token, image_id=image_id)

@donations_blueprint.route("/checkouts/<transaction_id>", methods=["GET"])
def show_checkout(transaction_id):
    transaction = gateway.transaction.find(transaction_id)
    result = {}
    if transaction.status in TRANSACTION_SUCCESS_STATUSES:
        result = {
            'header': 'Thank you for your generosity, you kind soul!',
            'icon': 'success',
            'message': 'Your test transaction has been successfully processed. See the Braintree API response and try again.'
        }
    else:
        result = {
            'header': 'Transaction Failed',
            'icon': 'fail',
            'message': 'Transaction has a status of ' + transaction.status + '.'
        }
    return render_template('donations/show.html', transaction=transaction, result=result, user=current_user)

@donations_blueprint.route("/checkouts/<image_id>", methods=["POST"])
def create_checkout(image_id):
    result = transact({
        'amount': request.form.get('amount'),
        'payment_method_nonce': request.form.get('payment_method_nonce'),
        'option': {
            "submit_for_settlement": True
        }
    })

    if result.is_success or result.transaction:
        flash("Transaction successful! Thanks so much")
        return redirect(url_for('donations.show_checkout', transaction_id=result.transaction.id))
    else:
        flash("Transaction fail! Please try again")
        return redirect(url_for('donation.new'))