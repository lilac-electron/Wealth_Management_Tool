from monzo import MonzoOAuth2Client
from monzo.utils import load_token_from_file
#from pandas.io.json import json_normalize
import pandas as pd
from monzo import Monzo
#from monzo import MonzoOAuth2Client

def authenticate():
    oauth_client = MonzoOAuth2Client('oauth2client_0000AdfM5AeMUPFJkXTHnt', 'mnzconf.libMV5WRpToEiz+Q64aUwZCWMLUcr110p4OSgvEY5TwSxT+SoX0xcsM7fC0fciBUrBYZIkCFLj4akwpF2qpkwQ==', redirect_uri = 'https://localhost')

    auth_start_url = oauth_client.authorize_token_url() 

    print(auth_start_url)


#secret = 'mnzconf.libMV5WRpToEiz+Q64aUwZCWMLUcr110p4OSgvEY5TwSxT+SoX0xcsM7fC0fciBUrBYZIkCFLj4akwpF2qpkwQ=='
#id = 'oauth2client_0000AdfM5AeMUPFJkXTHnt'

#link = 'https://localhost/?code=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJlYiI6IkVvVDZoa1c0NCswaFFTM3o4TCtYIiwianRpIjoiYXV0aHpjb2RlXzAwMDBBZGZNbFFsMHplNmFpSXV2Z0giLCJ0eXAiOiJhemMiLCJ2IjoiNiJ9.mL07HABGQxZ_8xCHVo6zQUV_dEBVtGPxakjOeGhssTlQYGaSTyRPI3uPdWIVU6oPq9jPx5Yi-EJPj341MkbeOQ&state=6FelQ8pGggFGLQ7YFUWamrVH45x9QC%27%2C+%276FelQ8pGggFGLQ7YFUWamrVH45x9QC%27'

#code = eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJlYiI6IkVvVDZoa1c0NCswaFFTM3o4TCtYIiwianRpIjoiYXV0aHpjb2RlXzAwMDBBZGZNbFFsMHplNmFpSXV2Z0giLCJ0eXAiOiJhemMiLCJ2IjoiNiJ9.mL07HABGQxZ_8xCHVo6zQUV_dEBVtGPxakjOeGhssTlQYGaSTyRPI3uPdWIVU6oPq9jPx5Yi-EJPj341MkbeOQ

#oauth_client.fetch_access_token('eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJlYiI6IkVvVDZoa1c0NCswaFFTM3o4TCtYIiwianRpIjoiYXV0aHpjb2RlXzAwMDBBZGZNbFFsMHplNmFpSXV2Z0giLCJ0eXAiOiJhemMiLCJ2IjoiNiJ9.mL07HABGQxZ_8xCHVo6zQUV_dEBVtGPxakjOeGhssTlQYGaSTyRPI3uPdWIVU6oPq9jPx5Yi-EJPj341MkbeOQ')

#jsonfile = load_token_from_file(r'C:\Users\username\Desktop\Monzo\monzo.json')
#jsonfile['client_secret'] = 'mnzconf.libMV5WRpToEiz+Q64aUwZCWMLUcr110p4OSgvEY5TwSxT+SoX0xcsM7fC0fciBUrBYZIkCFLj4akwpF2qpkwQ=='
#with open(r'monzo.json', 'w') as js:
    #json.dump(jsonfile, js)

#oauth_client = MonzoOAuth2Client.from_json(r'monzo.json')
#client = Monzo.from_oauth_session(oauth_client)

#account_id = client.get_first_account()['id']
#transactions = client.get_transactions(account_id)

#tr_table = json_normalize(transactions['transactions'])
#tr_table = pd.DataFrame(tr_table, sort = False)
#tr_table.to_csv(r'C:\Users\username\Desktop\Monzo\Monzo_transactions.csv', sep=',', index = False)

code = "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJlYiI6Im5WSzhuMnh6SlIyZGJkM3E5dGcrIiwianRpIjoiYXV0aHpjb2RlXzAwMDBBZGZTSk5vdXYyUWdFeThQY2YiLCJ0eXAiOiJhemMiLCJ2IjoiNiJ9.XGBW0P6ztVre9LtVFOmNEhBNnU0tQHuEJoQxkq4bm2eu51Z6tm0G9nebCaRdZ-8c9suTAf1F0Yvwe4x2uTvY4g"
state = "0cl28mhcsBrLgmbIbbWtZvBTGhVAkq%27%2C+%270cl28mhcsBrLgmbIbbWtZvBTGhVAkq%27"

authenticate()

"https://api.monzo.com/oauth2/token" \
    "grant_type=authorization_code" \
    "client_id=oauth2client_0000AdfM5AeMUPFJkXTHnt" \
    "client_secret=mnzconf.libMV5WRpToEiz+Q64aUwZCWMLUcr110p4OSgvEY5TwSxT+SoX0xcsM7fC0fciBUrBYZIkCFLj4akwpF2qpkwQ==" \
    "redirect_uri=https://localhost" \
    "code=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJlYiI6Im5WSzhuMnh6SlIyZGJkM3E5dGcrIiwianRpIjoiYXV0aHpjb2RlXzAwMDBBZGZTSk5vdXYyUWdFeThQY2YiLCJ0eXAiOiJhemMiLCJ2IjoiNiJ9.XGBW0P6ztVre9LtVFOmNEhBNnU0tQHuEJoQxkq4bm2eu51Z6tm0G9nebCaRdZ-8c9suTAf1F0Yvwe4x2uTvY4g"

{
    "access_token": "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJlYiI6IkJ0c3RIWkRsNXYwK3RHUG5MY2VBIiwianRpIjoiYWNjdG9rXzAwMDBBZGZUaFFOUEFPSWFJb1F1NFEiLCJ0eXAiOiJhdCIsInYiOiI2In0.u_EvI8iKHU6PSOho7cXpOCZb32GOOEM09H5bao4-0zMb28av4_zDiMKF2jB90D3rCQw-Mx3m3IVL0jFe2Ej8bw",
    "client_id": "oauth2client_0000AdfM5AeMUPFJkXTHnt",
    "expires_in": 107999,
    "refresh_token": "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJlYiI6ImV6cktBd2t0YTNhdnNFVW53d2NZIiwianRpIjoicmVmdG9rXzAwMDBBZGZUaFFTaXFjaEN0WmxlNEkiLCJ0eXAiOiJydCIsInYiOiI2In0.7K6_CobQQDlcJ3ianHm-m-VzDwTErW-irRQ1RIOqyxDs4DF7IROG5kUMpj6KF_MyYanFwGUVS7r0IakqCFAFjg",
    "scope": "third_party_developer_app.pre_verification",
    "token_type": "Bearer",
    "user_id": "user_00009hPDVBoQ6BJJXislbV"
}

http "https://api.monzo.com/accounts" \
    "Authorization: Bearer eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJlYiI6IkJ0c3RIWkRsNXYwK3RHUG5MY2VBIiwianRpIjoiYWNjdG9rXzAwMDBBZGZUaFFOUEFPSWFJb1F1NFEiLCJ0eXAiOiJhdCIsInYiOiI2In0.u_EvI8iKHU6PSOho7cXpOCZb32GOOEM09H5bao4-0zMb28av4_zDiMKF2jB90D3rCQw-Mx3m3IVL0jFe2Ej8bw"

http "https://api.monzo.com/balance" \
    "Authorization: Bearer eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJlYiI6IkJ0c3RIWkRsNXYwK3RHUG5MY2VBIiwianRpIjoiYWNjdG9rXzAwMDBBZGZUaFFOUEFPSWFJb1F1NFEiLCJ0eXAiOiJhdCIsInYiOiI2In0.u_EvI8iKHU6PSOho7cXpOCZb32GOOEM09H5bao4-0zMb28av4_zDiMKF2jB90D3rCQw-Mx3m3IVL0jFe2Ej8bw" \
    "account_id==oauth2client_0000AdfM5AeMUPFJkXTHnt"

http "https://api.monzo.com/balance" \
    "Authorization: Bearer eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJlYiI6IkJ0c3RIWkRsNXYwK3RHUG5MY2VBIiwianRpIjoiYWNjdG9rXzAwMDBBZGZUaFFOUEFPSWFJb1F1NFEiLCJ0eXAiOiJhdCIsInYiOiI2In0.u_EvI8iKHU6PSOho7cXpOCZb32GOOEM09H5bao4-0zMb28av4_zDiMKF2jB90D3rCQw-Mx3m3IVL0jFe2Ej8bw" \
    "account_id=oauth2client_0000AdfM5AeMUPFJkXTHnt"

    http "https://api.monzo.com/balance" \  
    "Authorization: Bearer eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJlYiI6IkJ0c3RIWkRsNXYwK3RHUG5MY2VBIiwianRpIjoiYWNjdG9rXzAwMDBBZGZUaFFOUEFPSWFJb1F1NFEiLCJ0eXAiOiJhdCIsInYiOiI2In0.u_EvI8iKHU6PSOho7cXpOCZb32GOOEM09H5bao4-0zMb28av4_zDiMKF2jB90D3rCQw-Mx3m3IVL0jFe2Ej8bw" \
    "account_id=oauth2client_0000AdfM5AeMUPFJkXTHnt"

$ http "https://api.monzo.com/pots" \
    "current_account_id==" \
    "Authorization: Bearer $access_token"

http --form POST "https://api.monzo.com/oauth2/token" \
    "grant_type=refresh_token" \
    "client_id=oauth2client_0000AdfM5AeMUPFJkXTHnt" \
    "client_secret=mnzconf.libMV5WRpToEiz+Q64aUwZCWMLUcr110p4OSgvEY5TwSxT+SoX0xcsM7fC0fciBUrBYZIkCFLj4akwpF2qpkwQ==" \
    "refresh_token=$refresh_token"

http "https://api.monzo.com/transactions" \
    "Authorization: Bearer eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJlYiI6IkJ0c3RIWkRsNXYwK3RHUG5MY2VBIiwianRpIjoiYWNjdG9rXzAwMDBBZGZUaFFOUEFPSWFJb1F1NFEiLCJ0eXAiOiJhdCIsInYiOiI2In0.u_EvI8iKHU6PSOho7cXpOCZb32GOOEM09H5bao4-0zMb28av4_zDiMKF2jB90D3rCQw-Mx3m3IVL0jFe2Ej8bw" \
    "account_id==oauth2client_0000AdfM5AeMUPFJkXTHnt"