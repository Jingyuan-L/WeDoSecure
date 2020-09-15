from flask import request, redirect
from flask_restful import Resource


class FindTableRes(Resource):
    def post(self):
        data = request.form
        table_name = data['table_name']
        return redirect('/table/' + table_name)
