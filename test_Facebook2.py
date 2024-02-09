import requests
import json
import urllib.parse
from facebook_business.adobjects.lead import Lead
from facebook_business.api import FacebookAdsApi

PAGE_ACCESS_TOKEN = 'EAAMwrnrznv0BO6TzVYsOd0yXmc3t9y7GhmABWbQM4ZCCwU5gyi0bSvtq26Q63A25n5yT0QGfGxTSMOZByDXnZAYjQN3ADVZBKyL4mcGct0Q08r8ZChZCutBXJYWsgRwxMs1ZCHTO5ZAbxf8tXroAZBvmlVL4rh1Njr2UQiVgMtWCW45cQgdadhs3er8I0TaWOgfv8rz5xuvHahe0n1gJNP8g2uHlg7EiRQXlNOMyuRwkZD'  
app_secret = '35c63adac7ba1faa3dbd9998badf8d36'
app_id = '897950875361021'
id = '120204879784990472'

fields = urllib.parse.quote_plus("access_token,app_id,leadgen_forms")


FacebookAdsApi.init(access_token=PAGE_ACCESS_TOKEN)

fields = [
]
params = {
}
print (Lead(id).get())



