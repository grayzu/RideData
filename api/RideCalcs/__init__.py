import logging
import json

import azure.functions as func
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

KVUri = f"https://kv-core001.vault.azure.net/"

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger Strava function processed a request.')

    challenge_str = req.params.get('hub.challenge')
    
    # Handle web hook call back from strava
    secret_name = 'strava-verify-token'

    if challenge_str:
        verify_token = req.params.get('hub.verify_token')

        #  Get token from Key Vault
        try:
            credential = DefaultAzureCredential()
            client = SecretClient(vault_url=KVUri, credential=credential)
            token = client.get_secret(secret_name)

        except:
            token = ''

        if verify_token == token:
            res_body = json.dumps({"hub.challeng": challenge_str})

            return func.HttpResponse(
                mimetype = 'application/json',
                body = res_body,
                status_code = 200
            )
        else:
            func.HttpResponse(
                'Forbidden',
                status_code=403
            )
    
    # Handle web hook for activity changes

    # name = req.params.get('name')
    # if not name:
    #     try:
    #         req_body = req.get_json()
    #     except ValueError:
    #         pass
    #     else:
    #         name = req_body.get('name')

    # if name:
    #     return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    # else:
    #     return func.HttpResponse(
    #          "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
    #          status_code=200
    #     )
