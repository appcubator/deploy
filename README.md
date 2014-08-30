Apps live on servers in docker containers.
Containers get created, put to sleep, woken up, destroyed.
These actions also trigger proxy configuration to route requests to the containers.
There is a deployer service to allow 3rd parties to call trigger these scripts remotely.

Architecture
------------

1. One Redis/Webdis which has the domain/backend mapping
2. One modified Hipache instance which reads from Redis to proxy requests
3. Several CoreOS hosts (they have docker installed) to host the apps
4. One deployer service to ssh into the CoreOS instances and run these sysadmin scripts

Directories
-----------

1. Container: bash scripts for manipulating docker containers locally
2. Remote: scripts which ssh to call Container scripts in bulk operations
3. Controller: python scripts which converge containers, use Remote to do it
