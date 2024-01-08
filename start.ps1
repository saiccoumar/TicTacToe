# Open first terminal and run main.py
Start-Process powershell -ArgumentList "-NoExit", "-Command python server.py" 

# Open second terminal and run main.py
Start-Process powershell -ArgumentList "-NoExit", "-Command python client.py" 

# Open third terminal and run test.py
Start-Process powershell -ArgumentList "-NoExit", "-Command python predict_position_nn.py" 