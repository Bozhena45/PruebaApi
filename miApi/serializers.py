# Django restFramework
from rest_framework import serializers

# Python
import datetime
import re

class ContactoValido(serializers.BaseSerializer):
    def to_internal_value(self, json):
        # Necitamos coger los parametros del json que sean obligatorios
        name = json.get('name')
        id_contacto = json.get('id')
        phone_number = json.get('phone_number')
        birth_date = json.get('birth_date')
        email = json.get('email')
        
        # Comprobar si hay algun error y en el caso de que haya devuelve null
        if id_contacto and (not validarNie(id_contacto) and not validarNif(id_contacto)):
            return{}

        if birth_date and not validarFecha(birth_date):
            return {}
        
        if email and not validarEmail(email):
            return {}

        if not name or not id_contacto or not phone_number:
            return {}

        return json

class ContactoInvalido(serializers.BaseSerializer):

    def to_internal_value(self,json):
        # Necitamos coger los parametros del json que sean obligatorios
        name = json.get('name')
        id_contacto = json.get('id')
        phone_number = json.get('phone_number')
        birth_date = json.get('birth_date')
        email = json.get('email')
        
        # Gestion de errores

        jsonErrores = {}
        if not name:
            jsonErrores['name'] = 'No está el nombre'

        if not id_contacto:
            jsonErrores['id'] = 'No está el id'

        if not phone_number:
            jsonErrores['phone_number'] = 'No está el phone_number'
    
        if birth_date and not validarFecha(birth_date):
            jsonErrores['birth_date'] = 'La fecha no está en el formato que toca '

        if email and not validarEmail(email):
            jsonErrores['email'] = 'El email no está en el formato que toca '

        if id_contacto and (not validarNie(id_contacto) and not validarNif(id_contacto)):
            jsonErrores['id'] = 'El id no está en el formato que toca '

        # Envia los errores
        if jsonErrores:
            raise serializers.ValidationError(jsonErrores)
        return {}
        
# Validaciones 
def validarNie(nie):
    return re.findall(r'^[a-zA-Z]\s\d{7}-[a-zA-Z]$', nie)
    
def validarNif(nif):
    nif = nif.replace('-', '')
    tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
    numeros = "1234567890"
    if (len(nif) == 9):
        letraControl = nif[8].upper()
        dni = nif[:8]
        if ( len(dni) == len( [n for n in dni if n in numeros] ) ):
            if tabla[int(dni)%23] == letraControl:
                return True

    return False

def validarFecha(fecha):
    try:
        datetime.datetime.strptime(fecha,'%Y-%m-%d')
    except:
        return False
    return True    

def validarEmail(email):
    return re.findall(r'[\w\.-]+@[\w\.-]+(\.[\w]+)+',email)

