#!/bin/bash

# Open first terminal and run main.py
gnome-terminal --tab --title="Terminal 1" --command="bash -c 'python server.py; exec bash'"

# Open second terminal and run main.py
gnome-terminal --tab --title="Terminal 2" --command="bash -c 'python rng-client.py; exec bash'"

# Open third terminal and run test.py
gnome-terminal --tab --title="Terminal 3" --command="bash -c 'python rng-client.py; exec bash'"