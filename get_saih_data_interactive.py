# -------------------------------------------------------------------------
# Author: Angel Acevedo Sanchez. All rights reserved.
#
# Licensed under the GPL-v3.0 License. See LICENSE in the project root for
# license information.
# -------------------------------------------------------------------------

import requests
import json
import pandas as pd
import os

URL = "http://www.saihguadiana.com:8090"
DATA_PATH = os.path.join(os.getcwd(), "data")


def send_request(request, URL, data, cookies):

    if request == "GET":
        ret = requests.get(URL, data=data, cookies=cookies)

    elif request == "POST":
        ret = requests.post(URL, data=data, cookies=cookies)

    else:
        print("Request must be POST or GET")

    return ret


def get_json_values(strings, file):

    codes = []

    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for string in strings:
        for object in data[str(os.path.basename(file)).split('.')[0]]:
            if string == object["nombre"]:
                codes.append(object["cod"])

    return codes


def get_var_codes(codes):

    var_codes = []

    for cod in codes:
        var_codes.append(cod+'/VE1')

    return var_codes


if __name__ == "__main__":

    session = requests.Session()

    payload = {

        "user": "xxxx",
        "password": "xxxx"
    }

    request = send_request("GET", URL+"/sdim_sg/logon.do", data="", cookies="")
    session_cookie = request.cookies.get_dict()
    request = send_request("POST", URL+"/sdim_sg/logon.do",
                           data=payload, cookies=session_cookie)

    if request.status_code == 200:

        send_request("GET", URL+"/sdim_sg/editSubscription.do",
                     data=payload, cookies=session_cookie)

        payload = {
            "scrolly": 0,
            "add": "",
            "remove": "",
            "temp_level": "D",  # MIN, D,...
            "dynamic_filter": 1,
            "format": "T"
        }

        send_request("POST", URL+"/sdim_sg/editSubscription.do",
                     data=payload, cookies=session_cookie)

        payload = {
            "scrolly": 140,
            "add": "",
            "remove": "",
            "temp_level": "D",
            "dynamic_filter": 2,
            "format": "T"
        }

        send_request("POST", URL+"/sdim_sg/editSubscription.do",
                     data=payload, cookies=session_cookie)

        provincias = list(map(str, input(
            "Introduce las provincias de interés [A, B, C, ...]: ").split(', ')))
        cod_provincias = get_json_values(provincias, os.path.join(DATA_PATH, 'provincias.json'))

        payload = {
            "scrolly": 140,
            "add": "FILTRO_PROVINCIA",
            "remove": "",
            "temp_level": "D",
            "dynamic_filter": 2,
            "parameter(FILTRO_PROVINCIA_LIST)": cod_provincias,
            "x": 8,
            "y": 5,
            "format": "T"
        }

        send_request("POST", URL+"/sdim_sg/editSubscription.do",
                     data=payload, cookies=session_cookie)

        estaciones = list(map(str, input(
            "Introduce las estaciones de interés [A, B, C, ...]: ").split(', ')))
        cod_estaciones = get_json_values(estaciones, os.path.join(DATA_PATH, 'estaciones.json'))

        payload = {
            "scrolly": 140,
            "add": "FILTRO_ESTACION",
            "remove": "",
            "temp_level": "D",
            "dynamic_filter": 2,
            "parameter(FILTRO_ESTACION_LIST)": cod_estaciones,
            "x": 12,
            "y": 10,
            "format": "T"
        }

        send_request("POST", URL+"/sdim_sg/editSubscription.do",
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

        send_request("POST", URL+"/sdim_sg/editSubscription.do",
                     data=payload, cookies=session_cookie)

        payload = {
            "scrolly": 362,
            "add": "FILTRO_VARIABLE_LIST",
            "remove": "",
            "temp_level": "D",
            "dynamic_filter": 2,
            "parameter(FILTRO_VARIABLE__USER_LIST)": get_var_codes(cod_estaciones),
            "x": 13,
            "y": 7,
            "format": "T"
        }

        send_request("POST", URL+"/sdim_sg/editSubscription.do",
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

        send_request("POST", URL+"/sdim_sg/preExecuteSubscription.do",
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

        text = send_request("POST", URL+"/sdim_sg/executeSubscription.do",
                            data=payload, cookies=session_cookie).text

        if "Error" not in text:
            table = pd.read_html(text, decimal=',', thousands='.')
            print(table[2])

        else:
            print("La combinación de datos introducida no es correcta")

    else:
        print("Login error")
