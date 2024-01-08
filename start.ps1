# Open first terminal and run main.py
Start-Process powershell -ArgumentList "-NoExit", "-Command python server.py" 

# Open second terminal and run main.py
Start-Process powershell -ArgumentList "-NoExit", "-Command python combined_rules_agent.py" 

# Open third terminal and run test.py
Start-Process powershell -ArgumentList "-NoExit", "-Command python minimax_agent.py" 