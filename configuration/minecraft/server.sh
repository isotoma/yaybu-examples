#!/bin/sh
cd {{ path }}
java -Xmx1024M -Xms1024M -jar {{ path}}/minecraft_server.jar nogui
