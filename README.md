# [Fulbright] Deep Learning Final Project
Final Project for the Deep Learning course at Fulbright University Vietnam
Web interface: [here](https://dldbminh.cung.io.vn/page3/)
## What's inside?
- Raw dataset
- Python code to process the raw data
- Cleaned & processed data

There is nothing need to run this project. You can interact at the website, or see the model code in the notebook.

## How to reproduce the result?
### Data Processing
- Run all the `v1_data_process_*_all.py`. The Python script will read all `.csv` files from respective folders in `./raw-data` and save the processed tables to `./v1-data`.
- Finally, run the `v1_data_process_indexer.py` file to create the indexes files. These index files helps to see all files and their length, which is helpful to know what files are available and whether to read them depends on your conditions.
### Data Normalization
- Run all the `v1_data_normalizaiton_all_v1.py`. The Python script will read all `.csv` files from `./v1-data` and save the processed tables to `./v1-data-normalized`.
- Instead of another indexer script, you can just copy the index folder from `./v1-data` to `./v1-data-normalized`.
### Model Construction
- Please read the project report or associated notebooks in the `./v1-files` folder
### Deployment
There are 2 apps in the `./v1-deploy` folder:
- The `app` folder is for the PocketBase backend serving the app as a webpage.
- The `api` folder is for the Python backend serving the model as an endpoint.

Guide:
- Download the PocketBase executable for your respective OS and put in the `app` folder. Learn more about PocketBase [here](https://pocketbase.io/)
- Run the PocketBase executable manually, or using the prepared `.service` file to register a systemd service for automatic execution and restart.
- In the `api` folder, create a virtual environment (venv) for Python 3. Install the required libraries from `requirements.txt`
- Run the Python script manually, or using the prepared `.service` file to register a systemd service for automatic execution and restart.