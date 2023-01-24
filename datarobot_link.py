import os
import sys
import json
import requests
from pandas import read_csv
from keys import *
import eel

API_URL = 'https://app2.datarobot.com/api/v2/deployments/{deployment_id}/predictions/'

# Don't change this. It is enforced server-side too.
MAX_PREDICTION_FILE_SIZE_BYTES = 52428800  # 50 MB

eel.init('gui')

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class DataRobotPredictionError(Exception):
    """Raised if there are issues getting predictions from DataRobot"""


def make_datarobot_deployment_predictions(data, deployment_id):
    """
    Make predictions on data provided using DataRobot deployment_id provided.
    See docs for details:
         https://app2.datarobot.com/docs/predictions/api/dr-predapi.html

    Parameters
    ----------
    data : str
        If using CSV as input:
        Feature1,Feature2
        numeric_value,string

        Or if using JSON as input:
        [{"Feature1":numeric_value,"Feature2":"string"}]

    deployment_id : str
        The ID of the deployment to make predictions with.

    Returns
    -------
    Response schema:
        https://app2.datarobot.com/docs/predictions/api/dr-predapi.html#response-schema

    Raises
    ------
    DataRobotPredictionError if there are issues getting predictions from DataRobot
    """
    # Set HTTP headers. The charset should match the contents of the file.
    headers = {
        # 'Content-Type': 'text/plain; charset=UTF-8',
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': 'Bearer {}'.format(API_KEY),
    }

    url = API_URL.format(deployment_id=deployment_id)

    params = {
    }
    # Make API request for predictions
    predictions_response = requests.post(
        url,
        data=data,
        headers=headers,
    )
    _raise_dataroboterror_for_status(predictions_response)
    # Return a Python dict following the schema in the documentation
    return predictions_response.json()


def _raise_dataroboterror_for_status(response):
    """Raise DataRobotPredictionError if the request fails along with the response returned"""
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        err_msg = '{code} Error: {msg}'.format(
            code=response.status_code, msg=response.text)
        raise DataRobotPredictionError(err_msg)

@eel.expose
def load_unique_field_values():

    '''
        Reads all the possible values for the Platform, Genre, Publisher and Rating columns
        in the data set.

        You may see the dataset from this folder or at https://www.kaggle.com/datasets/migeruj/videogames-predictive-model 
    '''

    data = read_csv(resource_path('videogame-sales-score.csv'))

    platforms = data['Platform'].tolist()
    genres = data['Genre'].tolist()
    publishers = data['Publisher'].tolist() 
    ratings = data['Rating'].tolist()

    # Filter unique values from the column 

    platforms_unique = set(platforms)
    genres_unique = set(genres)
    publishers_unique = set(publishers)
    ratings_unique = set(ratings)
    
    data = {
        'platforms' : list(platforms_unique),
        'genres' : list(genres_unique),
        'publishers' : list(publishers_unique),
        'ratings' : list(ratings_unique),
    }

    eel.load_lists(data)

@eel.expose
def get_prediction(
    platform: str,
    genre: str,
    publisher: str,
    na_sales: str,
    eu_sales: str,
    jp_sales: str,
    other_sales: str,
    rating: str,
):

    '''
        Gets a prediction for the model deployed at DataRobot based on the arguments received and
        returns a dictionary containing a message type and the tag-confidence pair with the greatest
        condifence value*. If there are missing arguments or there is an error during the prediction,
        returns a dictionary containing a message type and the error's description.

        *See #make_datarobot_deployment_predictions(data, deployment_id) to understand the response schema.
    '''
    
    if (
        not platform or not genre or not publisher or not rating or
        not na_sales or not eu_sales or not jp_sales or not other_sales
    ):
        data = {
            'message' : 'error',
            'error' : 'There are missing values.',
        }
        eel.display_prediction(data)
        return
    
    na_sales = float(na_sales)
    eu_sales = float(eu_sales)
    jp_sales = float(jp_sales)
    other_sales = float(other_sales)

    data = {
        'Platform' : platform,
        'Genre' : genre,
        'Publisher' : publisher,
        'NA_Sales' : na_sales,
        'EU_Sales' : eu_sales,
        'JP_Sales' : jp_sales,
        'Other_Sales' : other_sales,
        'Global_Sales' : na_sales + eu_sales + jp_sales + other_sales,
        'Rating' : rating,
    }

    try:
        prediction = make_datarobot_deployment_predictions(json.dumps([data]), DEPLOYMENT_ID)

        # We only send a single json file at a time, so we read the first (and only) result.
        # See make_datarobot_deployment_predictions documentation to understand the response schema
        prediction_values = prediction['data'][0]['predictionValues'];

        # Find the label-value pair with the greatest value (confidence)
        greatest_value = 0.0
        label = ''
        # A list that stores the possible results to be returned by the API
        possible_tags = []

        for lv_pair in prediction_values:

            value = lv_pair['value']

            if value > greatest_value:
                greatest_value = value
                label = lv_pair['label']
            
            possible_tags.append(lv_pair['label'])

        data =  {
            'message' : 'success',
            'prediction' : {
                'value' : greatest_value,
                'label' : label,
            },
            'possibilities' : possible_tags,
        }
    except Exception:
        data = {
            'message' : 'error',
            'error' : 'There was an error while making the prediction. Please check your internet connection or try again later.',
        }
    
    eel.display_prediction(data)
    return

try:
    eel.start('index.html', mode='chrome')
except:
    try:
        eel.start('index.html', mode='edge', app_mode=True)
    except:
        eel.start('index.html', mode='default')
