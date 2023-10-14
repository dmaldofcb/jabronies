# Scan2Invest

Scan2Invest is an innovative mobile application that allows customers to easily access information about a product's company and related investment products through a simple picture scan. With Scan2Invest, customers can make informed investment decisions on the go.

# Demo 
You can find a quick demo of our application in this youtube link https://youtu.be/gOqkaxW6vo8

## Features

- **Product Scan**: Customers upload and image of a product using web application.
- **Company Information**: The application instantly provides detailed information about the company that produces the scanned product.
- **Investment Products**: Scan2Invest also presents customers with a curated list of related investment products associated with the company.
- **Investment Options**: Customers have the option to explore and invest in these related investment products directly through the web app.

## Run Local
Install Windows and Running Windows, first navigate to the folder *\Scan2Invest* and run the following commands:
    
    pip install virtualenv

    python -m venv venv

    .\venv\Scripts\activate

    pip install -r requirements.txt

    python .\run.py

You should now have a virtual environment folder setup that is the interpreter you want to use *\Scan2Invest\venv*

## Generate Prediction Model
Navigate to folder *\Scan2Invest\PredictionModel*, the data set used to train is only trained on 27 company logos
- **Download Data**: first download the dataset we are using flicker_logos_27_dataset which is avaliable to the public first run the script *download_dataset.py*
- **Clean/Process Data**: we must clean the data, so that it is formatted correct format to generate the model run the script *pre_process_data.py*
- **Generate the model**: now we can generate the prediction model by runnig the script *generate_prediction_model.py*
- **Test Model**: we can test the model by giving it a image path and running the script *logo_predictor.py*

# jabronies-ui
The ui is a angular application it is pretty simple so if you want to see it can be found in this repository https://github.com/AaronJAdler/jabronies-ui

