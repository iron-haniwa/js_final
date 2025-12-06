from flask import Flask
from scraper import *
from flask_restful import Resource, Api, request
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)


class AmiAmiProducts(Resource):

    def get(self):
        args = request.args
        if 'query' in args:
            products = scrapeAmiAmi(args['query'])
            return products
        else:
            return 'You must pass in a query'
class MandarakeProducts(Resource):

    def get(self):
        args = request.args
        if 'query' in args:
            products = scrapeMandarake(args['query'])
            return products
        else:
            return 'You must pass in a query'
class YahooProducts(Resource):

    def get(self):
        args = request.args
        if 'query' in args:
            products = scrapeYahoo(args['query'])
            return products
        else:
            return 'You must pass in a query'

api.add_resource(AmiAmiProducts, '/scrape/AmiAmi/')
api.add_resource(MandarakeProducts, '/scrape/Mandarake/')
api.add_resource(YahooProducts, '/scrape/Yahoo/')




if __name__ == "__main__":
    app.run(debug=True)