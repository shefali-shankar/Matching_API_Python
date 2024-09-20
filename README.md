# Matching_API_Python
Built a RESTful API in Python using FastAPI that takes a user input and matches it against a predefined list of items in a json file. This code takes a json user input consisting of two fields; trade and unit_of_measure, and matches these input fields to the data in items.json file to find the closest matching item.

Language: Python
API Framework: FastAPI
Data: items.json file contains the master list of items, including the trade, unit_of_measure and rate. The user input item is matched to the data in this field.
Sample Inputs: inputs.json file contains sample inputs that may be provided by the user while making an API request.
Testing: test_main.py file contains the unit tests for the API. fastapi.testclient, and pytest can be used for testing


Working:
  1. The main.py file has the main code that uses FastAPI to create an API Endpoint "/match" that accepts a post request and returns a response based on the closes match found from the user input to the list of items in the items.json file.
  2. The input request should contain two fields; i.e the "trade" and "unit_of_measure". The values in both of the fields are matched to the item values in the items.json file.
  3. The closest matching item in the file is obtained and a similarity score is calculated using Levenshtein Distance (fuzzy ratios).
  4. The API returns the closest match and similarity score in the response.
  5. Error handling is done in case No matches are found or invalid input is provided and respective Error Response is displayed.


To Run Locally:
  1. Download the files in this repository, and ensure they are stored locally in the same folder.
  2. Open the folder path and the main.py file in a Text Editor (Eg. VsCode).
  3. To start the server, open a terminal/command prompt with the correct folder path (For VsCode: View > Terminal)
  4. In the terminal window, enter $uvicorn main:app
  5. Next, open a tab in your browser and enter your localhost IP Address: http://127.0.0.1:8000/docs#
  6. Expand the POST Request and Click "Try It Out". 
  7. Enter your input strings under the Request Body and click Execute to make the API Call. Example input:
    {
      "trade": "Earthworks",
      "unit_of_measure": "M3"
    }

  8. The output can be viewed under the "Responses" section.
  9. To run the unit tests locally, ensure pytest in installed. pytest can be installed using pip.
  10. Open the test_main.py file in your text editor and open a terminal to this path (For VsCode: View > Terminal).
  11. In the terminal, enter; $pytest
  12. The test cases are run and the number of passed test cases can be seen in the terminal.
