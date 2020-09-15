from werkzeug.security import safe_str_cmp
from models.customer import CustomerModel


def authenticate(customer_id, password):
    user = CustomerModel.find_by_id(customer_id)
    if user and safe_str_cmp(customer_id, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return CustomerModel.find_by_id(user_id)