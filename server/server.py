#!/usr/bin/python

#pip install flask flask-jsonify flask-sqlalchemy flask-restful flask-cache
import traceback
import sys
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
        return {'agents': [i[0] for i in query.cursor.fetchall()]}  # Fetches first column that is Agent ID

    @property
    def post(self):
        # This does not currently allow sending only some fields. All fields must be specified.
        try:
            new_agent_id = max(self.get().get('agents')) + 1
        except:
            new_agent_id = 1
        print(request.json)
        if not request.json:
            abort(400)

        try:
            if 'agent_name' in request.json and type(request.json['agent_name']) != unicode:
                abort(400)
            if 'agencurt_type' in request.json and type(request.json['agent_type']) != unicode:
                abort(400)
            if 'log_path' in request.json and type(request.json['log_path']) != unicode:
                abort(400)
            if 'notification_channel' in request.json and type(request.json['notification_channel']) != unicode:
                abort(400)
            if 'running_status' in request.json and type(request.json['running_status']) != unicode:
                abort(400)
            if 'skill_type' in request.json and type(request.json['skill_type']) != unicode:
                abort(400)
            if 'training_status' in request.json and type(request.json['training_status']) != unicode:
                abort(400)

            new_agent_name = request.json.get('agent')[0].get('agent_name')
            new_agent_type = request.json.get('agent')[0].get('agent_type')
            new_log_path = request.json.get('agent')[0].get('log_path')
            new_notification_channel = request.json.get('agent')[0].get('notification_channel')
            new_running_status = request.json.get('agent')[0].get('running_status')
            new_skill_type = request.json.get('agent')[0].get('skill_type')
            new_training_status = request.json.get('agent')[0].get('training_status')

            insert_query = ("insert into main.agents (agent_name, agent_type, log_path ,notification_channel, running_status, skill_type, training_status, agent_id ) "
            "values ('" + new_agent_name + "', '" +new_agent_type + "', '" +new_log_path + "', '" +new_notification_channel + "', '" + new_running_status + "', '" + new_skill_type + "', '" + new_training_status + "', '" + str(new_agent_id) + "');")

            print(insert_query)
            conn = db_connect.connect()
            query = conn.execute(insert_query)
            result_json = jsonify({'result': 'success'})
        except TypeError:
            print(traceback.format_exc())
            result_json = jsonify({'result': 'failure'})

        return result_json


class Agent_By_Id(Resource):
    def get(self, agent_id):
        conn = db_connect.connect()
        query = conn.execute("select * from main.agents where agent_id =%d;" % int(agent_id))
        result = {'agent': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)

    def put(self, agent_id):
        # This does not currently allow sending only some fields. All fields must be specified.
        if not request.json:
            abort(400)

        try:
            if 'agent_name' in request.json and type(request.json['agent_name']) != unicode:
                print("invalid agent_name")
                abort(400)
            if 'agent_type' in request.json and type(request.json['agent_type']) != unicode:
                print("invalid agent_type")
                abort(400)
            if 'log_path' in request.json and type(request.json['log_path']) != unicode:
                print("invalid log path")
                abort(400)
            if 'notification_channel' in request.json and type(request.json['notification_channel']) != unicode:
                print("invalid notification channel")
                abort(400)
            if 'running_status' in request.json and type(request.json['running_status']) != unicode:
                print("invalid running_status")
                abort(400)
            if 'skill_type' in request.json and type(request.json['skill_type']) != unicode:
                print("invalid skill type")
                abort(400)
            if 'training_status' in request.json and type(request.json['training_status']) != unicode:
                print("invalid training status")
                abort(400)

            new_agent_name = request.json.get('agent')[0].get('agent_name')
            new_agent_type = request.json.get('agent')[0].get('agent_type')
            new_log_path = request.json.get('agent')[0].get('log_path')
            new_notification_channel = request.json.get('agent')[0].get('notification_channel')
            new_running_status = request.json.get('agent')[0].get('running_status')
            new_skill_type = request.json.get('agent')[0].get('skill_type')
            new_training_status = request.json.get('agent')[0].get('training_status')

            update_query = ("update main.agents set agent_name = '"+ new_agent_name + "', " +
                            "agent_type = '"+new_agent_type + "', " +
                            "log_path  = '"+new_log_path + "', " +
                            "notification_channel = '" +new_notification_channel + "', " +
                            "running_status = '"+ new_running_status + "', " +
                            "skill_type = '"+ new_skill_type + "', " +
                            "training_status = '"+ new_training_status + "' " +
                            " where agent_id = '" + agent_id + "';")

            print(update_query)
            conn = db_connect.connect()
            query = conn.execute(update_query)
            result_json = jsonify({'result': 'success'})
        except TypeError:
            print(traceback.format_exc())
            result_json = jsonify({'result': 'failure'})

        return result_json



    def delete(self, agent_id):
        conn = db_connect.connect()
        query = conn.execute("delete from main.agents where agent_id =%d;" % int(agent_id))


class Agent_Activation(Resource):

    def post(self, agent_id, activation_action):
        print("Activation request: " + activation_action)
        conn = db_connect.connect()
        sql = ""
        if activation_action == "start":
            sql = "update main.agents set running_status = 'Pending Start' where agent_id = " + agent_id + ";"
        else:
            if activation_action == "stop":
                sql = "update main.agents set running_status = 'Not Running' where agent_id = " + agent_id + ";"
        if sql != "":
            print(sql)
            conn.execute(sql)

class Notification_Channels(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from main.notification_channels;")
        # result = {'notification_channels': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        # return jsonify(result)

        return {'notification_channels': [i[0] for i in query.cursor.fetchall()]}

    def post(self):
        # This does not currently allow sending only some fields. All fields must be specified.
        try:
            channel_id = max(self.get().get('notification_channels')) + 1
        except:
            channel_id = 1

        if not request.json:
            abort(400)
        if 'channel_name' in request.json and type(request.json['channel_name']) != unicode:
            abort(400)
        if 'channel_type' in request.json and type(request.json['channel_type']) is not unicode:
            abort(400)
        if 'configuration' in request.json and type(request.json['configuration']) is not unicode:
            abort(400)

        new_channel_name = request.json.get('notification_channels')[0].get('channel_name')
        new_channel_type = request.json.get('notification_channels')[0].get('channel_type')
        new_configuration = request.json.get('notification_channels')[0].get('configuration')
        try:
            insert_query = ("insert into main.notification_channels  (channel_name, channel_type, configuration, channel_id ) "
            "values ('" + new_channel_name + "', '" + new_channel_type + "', '" + new_configuration + "', '" + str(channel_id) + "');")

            print(insert_query)
            conn = db_connect.connect()
            query = conn.execute(insert_query)
            result_json = jsonify({'result': 'success'})
        except TypeError:
            result_json = jsonify({'result': 'failure'})

        return result_json

class Notification_Channels_By_Id(Resource):
    def get(self, channel_id):
        conn = db_connect.connect()
        query = conn.execute("select * from main.notification_channels where channel_id=%d;" % int(channel_id))
        result = {'notification_channels': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)

    def delete(self, channel_id):
        conn = db_connect.connect()
        query = conn.execute("delete from main.notification_channels where channel_id =%d;" % int(channel_id))


api.add_resource(Agents, '/agents')
api.add_resource(Agent_By_Id, '/agents/<agent_id>')
api.add_resource(Agent_Activation, '/agents/<agent_id>/activation/<activation_action>')
api.add_resource(Notification_Channels, '/notification_channels')
api.add_resource(Notification_Channels_By_Id, '/notification_channels/<channel_id>')


if __name__ == '__main__':
    app.run(port='8888')
