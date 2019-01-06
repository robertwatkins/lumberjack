insert into notification_channels (channel_id, channel_name, channel_type, configuration)
values (1, 'Dev Slack', 'Slack', 'https://hooks.slack.com/services/')

insert into agents (agent_id, agent_name, agent_type, log_path, notification_channel, running_status, skill_type, training_status)
values (1, 'NASA Test Log Agent', 'Apache', '/var/log', 'Dev Slack' , 'Not Running','URL n-gram', 'Not Trained');

insert into agents (agent_id, agent_name, agent_type, log_path, notification_channel, running_status, skill_type, training_status)
values (2, 'Another Sample Agent', 'Apache', '/var/log', 'Dev Slack' , 'Not Running','Request Size', 'Not Trained');

