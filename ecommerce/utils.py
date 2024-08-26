import requests
from rest_framework.response import Response
from rest_framework import status


def getVerdeValue():
        #hago la solicitud
        response = requests.get("https://pydolarve.org/api/v1/dollar?page=enparalelovzla")
        
        if response.status_code == 200:
            tareas = response.json()
            valor_dolar = tareas['monitors']['enparalelovzla']['price']
            return valor_dolar
        else:
            return Response({'mensaje':'no se ha logrado la conexion'}, status=status.HTTP_400_BAD_REQUEST)