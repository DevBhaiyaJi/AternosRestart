#!/bin/bash
cd /workspaces/$(basename $(pwd))
echo "Starting Minecraft server..."
java -Xmx16G -Xms15G -jar server.jar --nogui
