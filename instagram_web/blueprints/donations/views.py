from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, escape
from models.image import Image
from models.donation import Donation
from instagram_web.util.braintree_helpers import gateway
from flask_login import current_user


donations_blueprint = Blueprint('donations',
                            __name__,
                            template_folder='templates')
                            
@donations_blueprint.route('/<image_id>/new', methods=['GET'])
def new(image_id):
    image = Image.get_by_id(image_id)
    client_token = gateway.client_token.generate()
    return render_template('donations/new.html', client_token = client_token, image=image)


@donations_blueprint.route('/<image_id>/payment', methods=['POST'])
def payment(image_id):
    donation_amount = (request.form.get('donation_amount'))
    payment_nonce = request.form.get('payment_method_nonce')
    image = Image.get_or_none(Image.id == image_id)

    if not donation_amount or int(donation_amount) == 0:
        flash('Please insert whole number')
        return redirect(url_for('donations.new', image_id=image.id))

    if not payment_nonce:
        flash('System Error')
        return redirect(url_for('donations.new', image_id=image.id))
    

    result = gateway.transaction.sale({
        "amount": donation_amount,
        "payment_method_nonce": payment_nonce,
        "options": {
            "submit_for_settlement": True
        }
    })


    if result.is_success or result.transaction:
        donation = Donation(
            user = current_user.id, 
            amount=result.transaction.amount, 
            image_id=image.id
        )
        
        donation.save()
        flash('Success')
        return redirect(url_for('donations.new', image_id=image.id))
    # else:
    #     for x in result.errors.deep_errors:
    #         flash('Error: %s: %s' % (x.code,x.message))
    #     return render_template('donations/new.html', image_id=image.id)

    
