# Lumberjack Daemons

There are multiple Lumberjack Daemons.

### Lumberjack Training Daemon
The training daemon will poll the rest-api for new skills to train. If one is detected, then that skill will be trained.

### Lumberjack Agent Daemon
The agent daemo will poll the rest-api for enabled agents. When a trained agent is enabled for use, it is managed through the agent daemon.
