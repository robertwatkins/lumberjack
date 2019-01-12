CREATE TABLE IF NOT EXISTS agents(
   agent_id int PRIMARY KEY,
   agent_name text,
   agent_type text,
   log_path text,
   skill_type text,
   training_status text,
   running_status text,
   notification_channel text
);

CREATE TABLE IF NOT EXISTS notification_channels(
   channel_id int PRIMARY KEY,
   channel_name text,
   configuration text,
   channel_type text
);