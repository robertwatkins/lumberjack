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


class Notification_Channels(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from main.notification_channels;")
        result = {'notification_channels': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)


class Agent_By_Id(Resource):
    def get(self, agent_id):
        conn = db_connect.connect()
        query = conn.execute("select * from main.agents where agent_id =%d;" % int(agent_id))
        result = {'agent': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)


api.add_resource(Agents, '/agents')  # Route_1
api.add_resource(Notification_Channels, '/notification_channels')  # Route_2
api.add_resource(Agent_By_Id, '/agents/<agent_id>')  # Route_3

if __name__ == '__main__':
    app.run(port='8888')
