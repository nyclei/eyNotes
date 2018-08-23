import requests

url = "http://10.196.105.158:10131/subjects/testTTT-value/versions"

payload = "{\"schema\":\"{\\\"type\\\":\\\"record\\\",\\\"name\\\":\\\"Guest1\\\",\\\"namespace\\\":\\\"com.rccl.ss.avro\\\",\\\"fields\\\":[{\\\"name\\\":\\\"msg_id\\\",\\\"type\\\":[\\\"null\\\",\\\"string\\\"],\\\"default\\\":\\\"\\\"},{\\\"name\\\":\\\"voyage_id\\\",\\\"type\\\":[\\\"null\\\",\\\"string\\\"],\\\"default\\\":\\\"\\\"}]}\"}"
headers = {
    'Accept': "application/vnd.schemaregistry.v1+json, application/vnd.schemaregistry+json, application/json",
    'Content-Type': "application/json",
    'Cache-Control': "no-cache",
    'Postman-Token': "ec5e1444-f417-467f-b69e-4e04aa36ac2c"
    }
print(payload)
response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)
