# golden-flow
Full stack application (not yet) to demonstrate a simulation of oil fracking. 

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
- user navigates to localhost:port_number/docs to access swagger
	- Create a new treatment
		- POST /treatments
			User supplies treatment data in csv format (One is provided in the solution simulation_data.csv). The server stores the details of the treatment
			in a local sqllite database and directs a background process to simulate the treatment.
			The background process reads the treatment data line by line at 1 second intervals and logs the progress.

			- 15:45:36 Treatment 19: timestamp=1768691738, volume=3794.0, pressure=8695.0
			- 15:45:37 Treatment 19: timestamp=1768691739, volume=3315.0, pressure=1610.0
			- 15:45:38 Treatment 19: timestamp=1768691740, volume=4880.0, pressure=7750.0
	
	- List all treatments
		- GET
			The server returns a list of all treatments in the database. 

	- TODO: Implement the rest of the endpoints
