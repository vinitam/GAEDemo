#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import ndb
import webapp2,json
from collections import OrderedDict

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

class ProductHandler(webapp2.RequestHandler):
    def post(self):
        product = mProduct()
        product.name = self.request.get('name')
        product.quantity = int(self.request.get('quantity'))
        product.price = float(self.request.get('price'))
        product.put()

    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        json.dump(mProduct.get_list(), self.response.out)

    def handle_exception(self, exception, debug):
        print(str(exception))
        self.response.set_status(500)
        self.response.write('something went wrong.')


class mProduct(ndb.Model):
    name = ndb.StringProperty()
    quantity = ndb.IntegerProperty()
    price = ndb.FloatProperty()

    def to_message(self):
        return OrderedDict([
            ("quantity", self.quantity),
            ("name", self.name),
            ("price", self.price)
        ])

    @classmethod
    def get_list(self):
        query = mProduct.query()
        productlist = []
        for product in query:
            productlist.append(product.to_message())

        return dict([("products", productlist)])

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/product',ProductHandler)
], debug=True)
