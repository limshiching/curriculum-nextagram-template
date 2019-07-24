import os
from flask_wtf.csrf import CSRFProtect
from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, escape
from models.user import User
from models.image import Image
from instagram_web.util.braintree_helpers import gateway
from werkzeug.utils import secure_filename
from flask_login import current_user


donations_blueprint = Blueprint('donations',
                            __name__,
                            template_folder='templates/')
                            
@donations_blueprint.route('/new', methods=['GET'])
def new():
    client_token = gateway.client_token.generate()
    return render_template('donations/new.html', client_token = client_token)


@donations_blueprint.route('/payment', methods=['POST'])
def payment():
    donation_amount = request.form.get('donation_amount')
    payment_nonce = request.form.get('payment_method_nonce')

    result = gateway.transaction.sale({
        "amount": donation_amount,
        "payment_method_nonce": payment_nonce,
        "options": {
            "submit_for_settlement": True
        }
    })

    if result.is_success:
        flash('Success')
        return redirect(url_for('donations.new'))
    else:
        flash('Error')
        return render_template('donations/new.html')
