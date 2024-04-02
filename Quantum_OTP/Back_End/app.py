#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 02:54:23 2024

@author: wardah
"""

# Commands used:
# pip install Flask
# pip install flask_restful
# pip install twilio
# pip install python-dotenv


from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from QuantumOTP import generate_random_number
import os
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Create Flask app
app = Flask(__name__)
api = Api(app)


class OpenAccount(Resource):
    def post(self):
        # Generate a random number
        OTP = [generate_random_number() for _ in range(4)]
        OTPString = ''.join(str(num) for num in OTP)
        
        # send it to the user's mobile
        # account_sid = os.environ['TWILIO_ACCOUNT_SID']
        # auth_token = os.environ['TWILIO_AUTH_TOKEN']
        
        # client = Client(account_sid, auth_token)
        # message = client.messages \
        #     .create(
        #         body='Revenge of the Sith was clearly the best of the prequel trilogy.',
        #         messaging_service_sid='MG9752274e9e519418a7406176694466fa',
        #         to='+966546836150'
        #         )
        # print(message.sid)
        
        
        # from twilio.rest import Client
        # account_sid = os.environ['TWILIO_ACCOUNT_SID']
        # auth_token = os.environ['TWILIO_AUTH_TOKEN']
        # client = Client(account_sid, auth_token)
        # message = client.messages.create(
        #     from_='+14159695840',
        #     body='Hi',
        #     to=''
        #     )
        # print(message.sid)
        



        # Find your Account SID and Auth Token at twilio.com/console
        # and set the environment variables. See http://twil.io/secure
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        client = Client(account_sid, auth_token)
        
        message = client.messages \
                        .create(
                             body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                             from_='+15017122661',
                             to='+966546836150'
                         )
        
        print(message.sid)


        # 
        # Get the text data from the POST request
        data = request.get_json()
        
        # Assuming the text is provided under the key 'text'
        user_text = data.get('text', '')
        print(user_text)
        
        # You can then process the user_text as per your requirements
        
        
        if (OTPString == user_text):
            
            # logic to open the account using OTP and user_text
            response = {'message': 'Account opened successfully with OTP: {}'.format(OTP), 'user_text': user_text}
            
        elif (OTPString != user_text):
            response = {'message': 'Wrong OTP: {}'.format(OTP), 'user_text': user_text}
            
        else:
            response = {'message': 'Invalid Data'}
            
        return jsonify(response)

api.add_resource(OpenAccount, '/open-account')

if __name__ == '__main__':
    app.run(debug=True)
