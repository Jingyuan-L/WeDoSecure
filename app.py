import sqlite3
from flask import Flask, render_template, request
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.customer import CustomerLogin
from resources.enrollment import EnrollmentCustomer, AutoInvoiceModel, AutoInsuranceModel, CustomerModel, DriverModel, \
    HomeModel, HomeInvoiceModel, HomeInsuranceModel, VehicleModel
from resources.payment import MakePayment, AInsPaymentModel, HInsPaymentModel
from resources.admin import Admin, AdminModel
from resources.information import CustomerInformation
from resources.find_table import FindTableRes
from db import db
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'Jingyuan'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)


api.add_resource(CustomerLogin, '/login')
api.add_resource(EnrollmentCustomer, '/enrollment')
api.add_resource(MakePayment, '/payment/<int:customer_id>')
api.add_resource(Admin, '/admin_login')
api.add_resource(CustomerInformation, '/information/<int:customer_id>')
api.add_resource(FindTableRes, '/table')


@app.before_first_request
def create_tables():
    db.drop_all()
    db.create_all()
    AdminModel("admin", "admin").save_to_db()
    CustomerModel(10000001, 'test1', 'ANNA SMITH', '277 Gold St', 'F', 'S', 'H').save_to_db()
    CustomerModel(10000002, 'test2', 'CHRIS JOHNSON', '120 Nassau St', 'F', 'M', 'A').save_to_db()
    CustomerModel(10000003, 'test3', 'ERIC WILLIAMS', '1 Duffiled St', 'M', 'M', 'B').save_to_db()
    HomeInsuranceModel(10000001, datetime.strptime('2019-6-20', '%Y-%m-%d'), datetime.strptime('2020-6-20', '%Y-%m-%d'),
                       800.00, 'C').save_to_db()
    AutoInsuranceModel(10000002, datetime.strptime('2019-6-20', '%Y-%m-%d'), datetime.strptime('2020-6-20', '%Y-%m-%d'),
                       800.00, 'C').save_to_db()
    HomeInsuranceModel(10000003, datetime.strptime('2020-3-20', '%Y-%m-%d'), datetime.strptime('2021-3-20', '%Y-%m-%d'),
                       1000.00, 'C').save_to_db()
    AutoInsuranceModel(10000003, datetime.strptime('2020-3-20', '%Y-%m-%d'), datetime.strptime('2021-3-20', '%Y-%m-%d'),
                       500.00, 'C').save_to_db()
    HomeInvoiceModel(datetime.strptime('2019-6-20', '%Y-%m-%d'), datetime.strptime('2019-12-31', '%Y-%m-%d'), 800.00,
                     10000001).save_to_db()
    AutoInvoiceModel(datetime.strptime('2019-6-20', '%Y-%m-%d'), datetime.strptime('2019-12-31', '%Y-%m-%d'), 800.00,
                     10000002).save_to_db()
    HomeInvoiceModel(datetime.strptime('2020-3-20', '%Y-%m-%d'), datetime.strptime('2020-12-31', '%Y-%m-%d'), 1000.00,
                     10000003).save_to_db()
    AutoInvoiceModel(datetime.strptime('2020-3-20', '%Y-%m-%d'), datetime.strptime('2020-12-31', '%Y-%m-%d'), 500.00,
                     10000003).save_to_db()
    HomeModel(datetime.strptime('2019-3-20', '%Y-%m-%d'), 2000000, 700, 'S', 'Y', 'Y', 'I', 'Y', 10000001).save_to_db()
    VehicleModel('000111111111', '2010', 'O', 10000002).save_to_db()
    DriverModel('111111111111', 'ANNA SMITH', datetime.strptime('1995-1-1', '%Y-%m-%d'), '1').save_to_db()
    HomeModel(datetime.strptime('2011-3-20', '%Y-%m-%d'), 1000000, 500, 'C', 'Y', 'Y', 'N', 'N', 10000003).save_to_db()
    VehicleModel('099811111118', '2000', 'F', 10000003).save_to_db()
    DriverModel('111111111886', 'ERIC WILLIAMS', datetime.strptime('1990-1-1', '%Y-%m-%d'), '2').save_to_db()
    HInsPaymentModel(800, datetime.strptime('2019-6-20', '%Y-%m-%d'), 'Check', '1').save_to_db()
    AInsPaymentModel(800, datetime.strptime('2019-6-20', '%Y-%m-%d'), 'Debit', '1').save_to_db()
    HInsPaymentModel(800, datetime.strptime('2019-6-20', '%Y-%m-%d'), 'Credit', '2').save_to_db()
    AInsPaymentModel(400, datetime.strptime('2019-6-20', '%Y-%m-%d'), 'Paypal', '2').save_to_db()


jwt = JWT(app, authenticate, identity)  # /auth



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/information/<int:customer_id>')
def information(customer_id):
    customer = CustomerModel.find_by_id(customer_id)
    print(customer)
    return render_template('information.html', customer_form=customer)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/admin_login')
def admin_login():
    return render_template('admin_login.html')


@app.route('/enrollment')
def enrollment():
    # print("action")
    return render_template('enrollment.html')


@app.route('/product')
def product():
    return render_template('product.html')


@app.route('/admin_page')
def admin_page():
    return render_template('admin_page.html')


@app.route('/admin_delete_customer', methods=['POST'])
def admin_delete_customer():
    data = request.form
    user = CustomerModel.find_by_id(data['customer_id'])
    if not user:
        return render_template('/admin_page.html', msg="Customer not found!")
    user.delete_from_db()
    return render_template('/admin_page.html', msg="Delete customer successfully!")


@app.route('/table/<string:table_name>')
def table(table_name):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    if table_name:
        sql = "select * from " + table_name
        cursor.execute(sql)
        labels = [label[0] for label in cursor.description]
        content = cursor.fetchall()
    else:
        return render_template('table_page.html', msg="Please select a table!")
    return render_template('table_page.html', content=content, labels=labels, table_name=table_name)


@app.route('/payment/<int:customer_id>')
def payment(customer_id):
    h_cus = HomeInsuranceModel.find_by_id(customer_id)
    a_cus = AutoInsuranceModel.find_by_id(customer_id)
    h_pay = None
    a_pay = None
    if h_cus:
        h_inv = HomeInvoiceModel.query.filter_by(customer_id=customer_id).first()
        h_pay = HInsPaymentModel.query.filter_by(h_invoice_id=h_inv.h_invoice_id).all()
        print(h_pay)
    if a_cus:
        a_inv = AutoInvoiceModel.query.filter_by(customer_id=customer_id).first()
        a_pay = AInsPaymentModel.query.filter_by(a_invoice_id=a_inv.a_invoice_id).all()
        print(a_pay)
    h_need_pay = 0
    a_need_pay = 0

    if h_inv:
        paid = sum([x.h_pay_amount for x in h_pay])
        h_need_pay = h_inv.h_invoice_amount - paid
    if a_inv:
        paid = sum([x.a_pay_amount for x in a_pay])
        a_need_pay = a_inv.a_invoice_amount - paid

    return render_template('payment.html', h_pay=h_pay, a_pay=a_pay, h_need_pay=h_need_pay, a_need_pay=a_need_pay,
                           customer_id=customer_id, h_inv=h_inv, a_inv=a_inv)


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=8881, debug=True)
