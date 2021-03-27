# Django
from django.shortcuts import render, HttpResponse
from django.conf import settings
import json

# Django restFramework
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Serializers
from miApi.serializers import ContactoValido, ContactoInvalido

# Devolver json válidos
@api_view(['GET'])
def getList(request):
    
    json = getJson()

    # Cogemos la clase del archivo serializers.py y le pasamos los parametros data(El json) -> de esta manera solo recorre el primer json y si ponemos many= true te recorre todo el json

    serializer = ContactoValido(data=json,many=True)
    serializer.is_valid()

    # Los json que no están vacios
    arrayJsons = []

    for x in serializer.validated_data:
        if x:
            arrayJsons.append(x)

    return Response(arrayJsons)

# Devolver los jsno inválidos
@api_view(['GET'])
def getFailed(request):
    json = getJson()

    serializer = ContactoInvalido(data=json,many=True)
    serializer.is_valid()

    arrayJsons = []

    for x in serializer.errors:
        if x:
            arrayJsons.append(x)

    return Response(arrayJsons)

# Coger el fichero data.json
def getJson():
    pathJson = str(settings.BASE_DIR) + "/jsons/data.json"

    with open(pathJson) as f:
        fichero = json.load(f)
    return fichero['data']