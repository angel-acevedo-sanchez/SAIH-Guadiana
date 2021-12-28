import requests
import json
import pandas as pd
import numpy as np

url = "http://www.saihguadiana.com:8090"


def send_request(request, url, data, cookies):

    if request == "GET":
        ret = requests.get(url, data=data, cookies=cookies)

    elif request == "POST":
        ret = requests.post(url, data=data, cookies=cookies)

    else:
        print("Request must be POST or GET")

    return ret


if __name__ == "__main__":

    session = requests.Session()

    payload = {

        "user": "xxxxx",
        "password": "xxxxx"
    }

    request = send_request("GET", url+"/sdim_sg/logon.do", data="", cookies="")
    session_cookie = request.cookies.get_dict()
    request = send_request("POST", url+"/sdim_sg/logon.do",
                           data=payload, cookies=session_cookie)

    if request.status_code == 200:

        send_request("GET", url+"/sdim_sg/editSubscription.do",
                     data=payload, cookies=session_cookie)

        payload = {
            "scrolly": 0,
            "add": "",
            "remove": "",
            "temp_level": "D",  # MIN, D,...
            "dynamic_filter": 1,
            "format": "T"
        }

        send_request("POST", url+"/sdim_sg/editSubscription.do",
                     data=payload, cookies=session_cookie)

        payload = {
            "scrolly": 140,
            "add": "",
            "remove": "",
            "temp_level": "D",
            "dynamic_filter": 2,
            "format": "T"
        }

        send_request("POST", url+"/sdim_sg/editSubscription.do",
                     data=payload, cookies=session_cookie)

        payload = {
            "scrolly": 140,
            "add": "FILTRO_PROVINCIA",
            "remove": "",
            "temp_level": "D",
            "dynamic_filter": 2,
            "parameter(FILTRO_PROVINCIA_LIST)": ["06", "10"],
            "x": 8,
            "y": 5,
            "format": "T"
        }

        send_request("POST", url+"/sdim_sg/editSubscription.do",
                     data=payload, cookies=session_cookie)

        payload = {
            "scrolly": 140,
            "add": "FILTRO_ESTACION",
            "remove": "",
            "temp_level": "D",
            "dynamic_filter": 2,
            "parameter(FILTRO_ESTACION_LIST)": ["E2-01", "E2-03", "E2-04", "E2-06", "E2-07"],
            "x": 12,
            "y": 10,
            "format": "T"
        }

        send_request("POST", url+"/sdim_sg/editSubscription.do",
                     data=payload, cookies=session_cookie)

        payload = {
            "scrolly": 362,
            "add": "FILTRO_TIPO_VARIABLE",
            "remove": "",
            "temp_level": "D",
            "dynamic_filter": 2,
            "parameter(FILTRO_TIPO_VARIABLE_LIST)": "0020",
            "x": 8,
            "y": 8,
            "format": "T"
        }

        send_request("POST", url+"/sdim_sg/editSubscription.do",
                     data=payload, cookies=session_cookie)

        payload = {
            "scrolly": 362,
            "add": "FILTRO_VARIABLE_LIST",
            "remove": "",
            "temp_level": "D",
            "dynamic_filter": 2,
            "parameter(FILTRO_VARIABLE__USER_LIST)": ["E2-01/VE1", "E2-03/VE1", "E2-04/VE1", "E2-06/VE1", "E2-07/VE1"],
            "x": 13,
            "y": 7,
            "format": "T"
        }

        send_request("POST", url+"/sdim_sg/editSubscription.do",
                     data=payload, cookies=session_cookie)

        payload = {
            "scrolly": 362,
            "add": "",
            "remove": "",
            "temp_level": "D",
            "dynamic_filter": 2,
            "format": "T",
            "edit": "Aceptar"
        }

        send_request("POST", url+"/sdim_sg/preExecuteSubscription.do",
                     data=payload, cookies=session_cookie)

        payload = {
            "dates_set": "S",
            "data_ini": "31/10/2021",
            "data_fi": "28/12/2021"
        }  # Para el filtro diario

        # payload = {
        #     "dates_set": "S",
        #     "data_ini": "31/10/2021",
        #     "hora_ini": "00",
        #     "min_ini": "00",
        #     "data_fi": "1/11/2021",
        #     "hora_fi": "23",
        #     "min_fi": "59"

        # } #para el filtro minutal

        text = send_request("POST", url+"/sdim_sg/executeSubscription.do",
                            data=payload, cookies=session_cookie).text
        table = pd.read_html(text, decimal=',', thousands='.')

        print(table[2])
