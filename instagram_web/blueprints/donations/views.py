from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for
from instagram_web.util.braintree_helper import gateway


donations_blueprint = Blueprint(
    'donations', __name__, template_folder='templates')


@donations_blueprint.route("/new", methods=["GET"])
def new():
    client_token = gateway.client_token.generate()
    return render_template('donations/new.html', client_token=client_token)


@donations_blueprint.route("/payment", methods=["POST"])
def payment():
    nonce_from_the_client = request.form.get('payment_method_nonce')
    amount_from_the_client = request.form.get('donation_amount')

    result = gateway.transaction.sale({
        "amount": amount_from_the_client,
        "payment_method_nonce": nonce_from_the_client,
        "options": {
            "submit_for_settlement": True
        }
    })

    if result.is_success:
        flash('done')
        return redirect(url_for('donations.new'))
    else:
        flash('error')
        return render_template('donations/new.html')
