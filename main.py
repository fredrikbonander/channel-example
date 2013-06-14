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
import json
import logging
from google.appengine.api import channel
import webapp2


class MainHandler(webapp2.RequestHandler):
    @webapp2.cached_property
    def jinja2(self):
        from webapp2_extras import jinja2
        # Returns a Jinja2 renderer cached in the app registry.
        j = jinja2.get_jinja2(app=self.app)
        j.environment.variable_start_string = '@{'
        j.environment.variable_end_string = '}@'
        return j

    def render_response(self, _template, **context):
        # Renders a template and writes the result to the response.
        rv = self.jinja2.render_template(_template, **context)
        self.response.write(rv)

    def get(self):
        self.render_response('index.html')


class ChannelHandler(webapp2.RequestHandler):
    def get(self, *args, **kwds):
        token = channel.create_channel(self.request.get('user_id'))
        self.response.write(json.dumps({'token': token}))

    def post(self, *args, **kwds):
        post_data = json.loads(self.request.body)
        channel.send_message(str(post_data['user_id']), 'Hello')

app = webapp2.WSGIApplication([
    #('/_ah/channel/connected/', ChannelHandler),
    #('/_ah/channel/disconnected/', ChannelHandler),
    ('/channel', ChannelHandler),
    ('/', MainHandler)
], debug=True)
