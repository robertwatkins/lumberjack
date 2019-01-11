#pip install flask flask-jsonpify flask-sqlalchemy flask-restful flask-cache
from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
#from flask.ext.jsonpify import jsonify
from flask_cors import CORS
from flask.json import jsonify
from flask_restful import Resource, Api

db_connect = create_engine('sqlite:///lumberjack.db')
app = Flask(__name__)
CORS(app)
api = Api(app)


class Agents(Resource):
    def get(self):
        conn = db_connect.connect()  # connect to database
        query = conn.execute("select * from main.agents;")  # This line performs query and returns json result
        return {'agents': [i[0] for i in query.cursor.fetchall()]}  # Fetches first column that is Employee ID

class Agent_By_Id(Resource):
    def get(self, agent_id):
        conn = db_connect.connect()
        query = conn.execute("select * from main.agents where agent_id =%d;" % int(agent_id))
        result = {'agent': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)

    def put(self):
        pass

    def post(self):
        pass

class Notification_Channels(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from main.notification_channels;")
        result = {'notification_channels': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)

class Notification_Channels_By_Id(Resource):
    def get(self, channel_id):
        conn = db_connect.connect()
        query = conn.execute("select * from main.notification_channels where channel_id=%d;" % int(channel_id))
        result = {'notification_channels': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)

    def put(self, channel_id):
        # notification = [notification for notification in notifications if notification['id'] == channel_id]
        # if len(notification) == 0:
        #    abort(404)

        # notification = self.get(channel_id)
        notification = {"notification_channels":[{"channel_id":1,"channel_name":"Dev Slack","channel_type":"Slack","configuration":"https://hooks.slack.com/services/"}]}

        if not request.json:
            abort(400)
        if 'channel_name' in request.json and type(request.json['channel_name']) != unicode:
            abort(400)
        if 'channel_type' in request.json and type(request.json['channel_type']) is not unicode:
            abort(400)
        if 'configuration' in request.json and type(request.json['configuration']) is not unicode:
            abort(400)
        # notification[0]['channel_name'] = request.json.get('channel_name', notification[0]['channel_name'])
        # notification[0]['channel_type'] = request.json.get('channel_type', notification[0]['channel_type'])
        # notification[0]['configuration'] = request.json.get('configuration', notification[0]['configuration'])
        conn = db_connect.connect()
        new_channel_name = request.json.get('notification_channels')[0].get('channel_name')
        new_channel_type = request.json.get('notification_channels')[0].get('channel_type')
        new_configuration = request.json.get('notification_channels')[0].get('configuration')
        update_query = ("update main.notification_channels set "
        "channel_name = '" + new_channel_name + "', "
        "channel_type = '" + new_channel_type + "', "
        "configuration = '" + new_configuration + "' "
        "where channel_id = " + str(channel_id) + ";")
        print(update_query)
        query = conn.execute(update_query)
        result_json = jsonify({'result': 'success'})
        return result_json

    def post(self, channel_id):
        pass


api.add_resource(Agents, '/agents')
api.add_resource(Agent_By_Id, '/agents/<agent_id>')
api.add_resource(Notification_Channels, '/notification_channels')
api.add_resource(Notification_Channels_By_Id, '/notification_channels/<channel_id>')


if __name__ == '__main__':
    app.run(port='8888')
