# golden-flow
Full stack application to demonstrate a simulation of oil fracking. 

### run application locally in a virtual environment (create and activate)
- Navigate to the src folder in powershell
- Run python -m venv .venv
- Run .venv\Scripts\activate.bat

### install dependencies
- Navigate to the src folder in powershell
- Run pip install -r .\requirements.txt

### run the application in docker (Windows)
- Install docker desktop
- Navigate to the src folder in powershell
- Run docker compose up -d --build
- Run docker compose up -d --force-recreate

### how it works
- use navigates to localhost:port_number/docs to access swagger
- create a new treatment by using POST create a new resource (treatment) on the server
