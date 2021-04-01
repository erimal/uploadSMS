import uploadapp.dbSettings as st
import json
import requests
import logging
from datetime import datetime
from random import randint

from uploadapp.dbConfig import add_sms ,deliver_message
from django_test_curl import CurlClient


def send_Orange_SMS(phone):
    client = None
    url = 'https://api.orange.com/smsmessaging/v1/outbound/tel%3A%2B23100000000/requests'
    #df = dbConfig.read_messages()

    #Create an error  log file
    file_log = st.LOG_FILENAME + "_" + (datetime.now().strftime("%Y-%m-%d"))

    logging.basicConfig(format='Date-Time : %(asctime)s : %(message)s',
                        level=logging.INFO, filename=file_log, filemode='a')

    try:
        phone = phone
        msg = "Welcome to AccessBank Network"

        # first data value for JSON
        data = {}
        data['address'] = 'tel:+' + phone
        data['senderName'] = 'AccessBank'
        data['senderAddress'] = "tel:+23100000000"

        # Json data value
        data_msg = {}
        data_msg['message'] = msg

        #Add phone numbers ,sender name , sender address to the message
        data['outboundSMSTextMessage'] = data_msg

        # Add the first part of the message to the final outboundSMSMessageRequest message
        data_final = {}
        data_final['outboundSMSMessageRequest'] = data
        json_data_final = json.dumps(data_final)

        #print(json_data_final)
        token = "Bearer " + get_orange_token()

        #"Authorization": "Bearer bsOZFsuiPsL7dk1f2VAY9OR5vB3z",
        header = {
                   "Authorization": f"{token}",
                    "Content-Type": "application/json"
                 }

        response = requests.post(url, json_data_final, headers=header)
        #print(response.text)

        if response.status_code == 201:
            resp_text = json.loads(response.text)
            resource_url = resp_text['outboundSMSMessageRequest']['resourceURL']
            resource_id = resource_url[-36:]
            print("Message Delivered to Phone:" + phone + " with resource Id: " + resource_id)

            #update the imported and delivery SMS table
            row = {}
            row['mobilenumber'] = phone
            row['message'] = msg
            row['id'] = random_with_N_digits(5)
            print("utils:send_orange_SMS: other ID ", row['id'])
            add_sms(row)
            deliver_message(row, resource_id)
        else:
            print("Delivery failed Status code: ", response.status_code)

            logging.info('Delivery failed: response code:{} - phone:{}'.format(response.status_code, phone))

        #rest variable
        phone = ""

    except AssertionError as error:
        # Output expected AssertionErrors.
        #Logging.log_exception(error)
        print("AssertionError: ", error)
    except Exception as exception:
        #assert type(exception).__name__ == 'NameError'
        #assert exception.__class__.__name__ == 'NameError'
        #assert exception.__class__.__qualname__ == 'NameError'
        print("ExceptionError: ", exception)

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def get_orange_token():

    token = ""
    url = "https://api.orange.com/oauth/v3/token"
    data = {}
    data['grant_type'] = "client_credentials"

    header = {
        "Authorization": "Basic TGxKQVN0QklEdlhkM0J2eEVPRklrMXNjaWJvRmRHMkY6Z3hNQTNWUVpXV3N1a1hBWg==",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }

    response = requests.post(url, data, headers=header)
    print("Reposnse of the Json", response.text)
    if response.status_code == 200:
        resp_text = json.loads(response.text)
        token = resp_text['access_token']
        print("Orange_token", token)

    return token