curl http://localhost:8888/notification_channels
curl -i -X POST -H "Content-Type:application/json" http://localhost:8888/notification_channels -d '{"notification_channels":[{"channel_id":2,"channel_name":"QA Slack","channel_type":"Slack","configuration":"https://hooks.slack.com/services/"}]}'



curl http://localhost:8888/agents
curl -i -X POST -H "Content-Type:application/json" http://localhost:8888/agents -d {"agent":[{"agent_id":1,"agent_name”:”Another Test Log Agent","agent_type":"Apache","log_path":"/var/log","notification_channel":"Dev Slack","running_status":"Not Running","skill_type":"URL n-gram","training_status":"Not Trained"}]}


