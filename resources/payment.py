from flask_restful import Resource
from flask import request, redirect
from datetime import datetime
from models.a_ins_payment import AInsPaymentModel
from models.h_ins_payment import HInsPaymentModel


class MakePayment(Resource):
    def post(self, customer_id):
        data = request.form
        if data['ins_type'] == "A":
            AInsPaymentModel(data['payment_amount'], datetime.now(), data['payment_method'],
                             data['invoice_id']).save_to_db()
        elif data['ins_type'] == "H":
            HInsPaymentModel(data['pay_amount'], datetime.now(), data['payment_method'],
                             data['invoice_id']).save_to_db()

        return redirect("/payment/" + str(customer_id))


