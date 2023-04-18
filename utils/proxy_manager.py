


import requests


def get_enumproxy():
    url = "https://ephemeral-proxies.p.rapidapi.com/v2/datacenter/proxy"

    headers = {
        "X-RapidAPI-Key": "60f7bdf787msh61ddbd43812c12cp1059a4jsnd4564938be2c",
        "X-RapidAPI-Host": "ephemeral-proxies.p.rapidapi.com"}
    response = requests.request("GET", url, headers=headers).json()
    host = response["proxy"]["host"]
    port = response["proxy"]["port"]
    return f"{host}:{port}"