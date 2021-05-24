from PyQt5.QtCore import pyqtSignal

from methods import utils
from data.methods_db import MethodsDb


class MethodsMain:
    """
    Class to implement main screen method

    s_update_address: signal emit (str, str, str, str, str, str)
    s_update_cep: signal emit (list)
    s_register_error> signal emit (str)
    s_register_success: signal emit (str)
    """

    s_update_address = pyqtSignal(str, str, str, str, str, str)
    s_update_cep = pyqtSignal(list)
    s_register_error = pyqtSignal(str)
    s_register_success = pyqtSignal(str)

    def __init__(self):
        self.db = MethodsDb()
        self.db.start_conn()

    def get_address_by_cep(self, cep: str):
        """
        Get address by cep.

        Parameters
        ----------
        cep : CEP string

        Returns
        -------
        None
        s_update_address event emit
        """
        data = utils.get_address_by_cep(cep)
        if "invalid_address" in data.keys():
            print("ERROR: INVALID CEP.")
        else:
            if type(data) == list:
                data = data[0]
            type_location = data['logradouro'].split(" ")[0]
            street_location = " ".join(data['logradouro'].split(" ")[1:])
            complement = data['complemento']
            district = data['bairro']
            city = data['localidade']
            state = data['uf']

            self.s_update_address.emit(
                type_location, street_location, complement,
                district, city, state
            )

    def get_cep_by_address(
            self, type_location:str, street_location:str, city:str, state:str
    ):
        """
        Get CEP by partial address

        Parameters
        ----------
        type_location : Type location
        street_location : Street localtion name
        city : City name
        state : State uf

        Returns
        -------
        None
        s_update_cep event emit
        """
        data = utils.get_cep_by_address(state, city, type_location, street_location)
        addresses = []

        for d in data:
            complete_address = d['logradouro']
            complete_address += ", " + d['bairro']
            complete_address += ", " + d['localidade']
            complete_address += " - " + d['uf']
            complete_address += ". CEP " + d['cep']
            addresses.append({
                'complete': complete_address,
                'cep': d['cep'].replace("-", "")
            })
        self.s_update_cep.emit(addresses)

    def register_user(
            self, name:str, birth_date:str, cpf:str, cep:str, type_location:str,
            street_location:str, number:str, complement:str, district:str,
            city:str, state:str, email:str
    ):
        """
        Send user information to database and commit data

        Parameters
        ----------
        name : User name
        birth_date : User birth date
        cpf : User CPF
        cep : User CEP
        type_location : User type localtion
        street_location : User street location name
        number : User address number
        complement : Addressc complement
        district : User district name
        city : User city name
        state : User UF
        email : User e-mail

        Returns
        -------
        None
        s_register_error or s_register_error event emit
        """
        error_msg = ""
        if len(name) < 5:
            error_msg += "Invalid name.\n"

        if not utils.validate_cpf(cpf):
            error_msg += "Invalid CPF.\n"

        if not utils.check_address(
                cep, type_location, street_location,
                district, city, state
        ):
            error_msg += "CEP entered does not match address.\n"

        if not utils.validate_address_number(number):
            error_msg += "Invalid address number.\n"

        if not utils.validate_email(email):
            error_msg += "Invalid E-mail."

        if error_msg:
            self.s_register_error.emit(error_msg)
        else:
            cursor = self.db.conn.cursor()
            res = self.db.inset_user(
                name, birth_date, cpf, cep, type_location,
                street_location, number, complement, district,
                city, state, email, cursor
            )
            if res:
                self.db.conn.commit()
                self.s_register_success.emit(
                    "User successfully registered."
                )
            else:
                error_msg = "CPF and/or E-mail duplicate(s)."
                self.s_register_error.emit(error_msg)
