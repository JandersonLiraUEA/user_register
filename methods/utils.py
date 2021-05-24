import json
import requests
import re
from validate_docbr import CPF


def get_address_by_cep(cep):
    url_api = ('http://www.viacep.com.br/ws/%s/json' % cep)
    return get_address(url_api)


def get_cep_by_address(state, city, type, street):
    url_api = ('http://www.viacep.com.br/ws/%s/%s/%s %s/json' % (state, city, type, street))
    return get_address(url_api)


def get_address(url_api):
    req = requests.get(url_api)
    if req.status_code != 200:
        data_json = {'invalid_address': True}
        return data_json
    else:
        data_json = json.loads(req.text)
        return data_json


def validate_cpf(cpf_string):
    cpf_method = CPF()
    return cpf_method.validate(cpf_string)


def check_address(
        cep, type_location, street_location,
        district, city, state
):
    data = get_address_by_cep(cep)

    if "invalid_address" in data.keys():
        return False

    complete_street_name = type_location + " " + street_location
    if complete_street_name != data['logradouro']:
        return False

    if district != data['bairro']:
        return False

    if city != data['localidade']:
        return False

    if state != data['uf']:
        return False

    return True


def validate_address_number(number):
    has_number = any(char.isdigit() for char in number)
    is_sn = number.upper() == "S/N"
    return has_number | is_sn


def validate_email(email):
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

    if (re.search(regex, email)):
        return True
    else:
        return False