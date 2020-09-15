from flask import request, redirect
from flask_restful import Resource


class ShowTable(Resource):
    def post(self, table_name):
        data = request.form
        table_name = data['table_name']
        return redirect('/table/'+ table_name)
