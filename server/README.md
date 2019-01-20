# Lumberjack Rest API Server

This server manages the CRUD operations for the data in the Lumberjack system.

### Endpoints

| Endpoint | |
| --------------------------:| -----:|
| /agents                             |supports GET and POST verbs|
| /agents/<agent_id>                  |supports PUT and DELETE verbs |
| /notification_channels              |supports GET and POST verbs |
| /notification_channels/<channel_id> |supports PUT and DELETE verbs |
| agents/<agent_id>/activation/<'start'&#124;'stop'> | supports POST verb |

