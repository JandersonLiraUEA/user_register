from PyQt5.QtWidgets import QWidget, QGroupBox, QLineEdit, QDateEdit, \
    QVBoxLayout, QFormLayout, QLabel, QPushButton, QHBoxLayout, QComboBox, \
    QDialog, QMessageBox
from PyQt5.QtCore import QRegExp, pyqtSignal, QDate
from PyQt5.QtGui import QRegExpValidator, QFont
from methods.methods_main import MethodsMain


class ScreenMain(QWidget, MethodsMain):

    def __init__(self):
        super().__init__()
        self.init_validators()
        self.init_ui()
        self.set_connections()
        self.show()

    def init_validators(self):
        """
        Initialize regex validators

        Returns
        -------
        None
        """
        regex_only_letters = QRegExp("[a-z-A-Z_ ]+")
        self.validator_only_letters = QRegExpValidator(regex_only_letters)

        regex_only_numbers = QRegExp("[0-9]+")
        self.validator_only_numbers = QRegExpValidator(regex_only_numbers)

        regex_email = QRegExp('^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$')
        self.validator_email = QRegExpValidator(regex_email)

    def init_ui(self):
        """
        Create screen elements

        Returns
        -------
        None
        """
        self.setGeometry(0, 0, 700, 700)
        self.main_font = QFont('Times', 18)
        self.setFont(self.main_font)

        self.form_user_data = QGroupBox("User information")

        self.line_name = QLineEdit()
        self.line_name.setPlaceholderText("Only letters (min. 5)")
        self.line_name.setMaxLength(100)
        self.line_name.setValidator(self.validator_only_letters)

        self.date_birth_date = QDateEdit()
        self.date_birth_date.setMaximumDate(QDate.currentDate())
        self.date_birth_date.setDisplayFormat("dd/MM/yyyy")

        self.line_cpf = QLineEdit()
        self.line_cpf.setPlaceholderText("Only numbers")
        self.line_cpf.setMaxLength(11)
        self.line_cpf.setValidator(self.validator_only_numbers)

        self.line_cep = QLineEdit()
        self.line_cep.setPlaceholderText("Only number")
        self.line_cep.setMaxLength(8)
        self.line_cep.setValidator(self.validator_only_numbers)
        self.btn_search_cep = QPushButton("Search address from CEP")
        self.layout_cep = QHBoxLayout()
        self.layout_cep.setContentsMargins(0, 0, 0, 0)
        self.layout_cep.addWidget(self.line_cep)
        self.layout_cep.addWidget(self.btn_search_cep)
        self.widget_cep = QWidget()
        self.widget_cep.setLayout(self.layout_cep)

        self.line_type_street_location = QLineEdit()
        self.line_type_street_location.setPlaceholderText(
            "Beco, Rua, Avenida, etc"
        )
        self.line_type_street_location.setMaxLength(50)

        self.line_street_location = QLineEdit()
        self.line_street_location.setMaxLength(100)

        self.line_number = QLineEdit()
        self.line_number.setPlaceholderText("Number or S/N")
        self.line_number.setMaxLength(10)

        self.line_complement = QLineEdit()
        self.line_complement.setMaxLength(100)

        self.line_district = QLineEdit()
        self.line_district.setMaxLength(100)

        self.line_city = QLineEdit()
        self.line_city.setMaxLength(100)

        self.cbbox_state = QComboBox()
        self.cbbox_state.addItems(
            ["AC", "AL", "AP",
             "AM", "BA", "CE",
             "DF", "ES", "GO",
             "MA", "MT", "MS",
             "MG", "PA", "PB",
             "PR", "PE", "PI",
             "RR", "RO", "RJ",
             "RN", "RS", "SC",
             "SP", "SE", "TO"])
        self.cbbox_state.setEditable(False)
        self.btn_search_address = QPushButton("Search CEP by address")
        self.layout_search_address = QHBoxLayout()
        self.layout_search_address.setContentsMargins(0, 0, 0, 0)
        self.layout_search_address.addWidget(self.cbbox_state)
        self.layout_search_address.addWidget(self.btn_search_address)
        self.widget_search_address = QWidget()
        self.widget_search_address.setLayout(self.layout_search_address)

        self.line_email = QLineEdit()
        self.line_email.setMaxLength(100)
        self.line_email.setValidator(self.validator_email)

        self.layout_form = QFormLayout()
        self.layout_form.addRow(QLabel("Name"), self.line_name)
        self.layout_form.addRow(QLabel("Birth date"), self.date_birth_date)
        self.layout_form.addRow(QLabel("CPF"), self.line_cpf)
        self.layout_form.addRow(QLabel("CEP"), self.widget_cep)
        self.layout_form.addRow(QLabel("Type of location"), self.line_type_street_location)
        self.layout_form.addRow(QLabel("Street location"), self.line_street_location)
        self.layout_form.addRow(QLabel("Number"), self.line_number)
        self.layout_form.addRow(QLabel("Complement"), self.line_complement)
        self.layout_form.addRow(QLabel("District"), self.line_district)
        self.layout_form.addRow(QLabel("City"), self.line_city)
        self.layout_form.addRow(QLabel("State"), self.widget_search_address)
        self.layout_form.addRow(QLabel("E-mail"), self.line_email)
        self.form_user_data.setLayout(self.layout_form)

        self.btn_register_user = QPushButton("Register")

        self.layout_main = QVBoxLayout()
        self.layout_main.addWidget(self.form_user_data)
        self.layout_main.addWidget(self.btn_register_user)

        self.setLayout(self.layout_main)

    def set_connections(self):
        """
        Connect events (clicked, returnPressed, signals and others)

        Returns
        -------
        None
        """
        self.line_cep.returnPressed.connect(
            self.btn_search_cep.click
        )
        self.btn_search_cep.clicked.connect(
            lambda x: self.get_address_by_cep(
                self.line_cep.text()
            )
        )
        self.s_update_address.connect(self.set_address_by_cep)

        self.btn_search_address.clicked.connect(
            lambda x: self.get_cep_by_address(
                self.line_type_street_location.text(),
                self.line_street_location.text(),
                self.line_city.text(),
                self.cbbox_state.currentText()
            )
        )
        self.s_update_cep.connect(self.set_cep_by_address)

        self.btn_register_user.clicked.connect(
            lambda x: self.register_user(
                self.line_name.text(),
                self.date_birth_date.text(),
                self.line_cpf.text(),
                self.line_cep.text(),
                self.line_type_street_location.text(),
                self.line_street_location.text(),
                self.line_number.text(),
                self.line_complement.text(),
                self.line_district.text(),
                self.line_city.text(),
                self.cbbox_state.currentText(),
                self.line_email.text()
            )
        )

        self.s_register_error.connect(self.show_error_msg)
        self.s_register_success.connect(self.show_success_msg)

    def set_address_by_cep(
            self, type_location: str, stree_location: str, complement: str,
            district: str, city: str, state: str
    ):
        """
        Set partial address by CEP

        Parameters
        ----------
        type_location : Street type localtion
        stree_location : Stret location name
        complement : Complemente location
        district : District name
        city : City name
        state : State uf

        Returns
        -------
        None
        """
        self.line_type_street_location.setText(type_location)
        self.line_street_location.setText(stree_location)
        self.line_complement.setText(complement)
        self.line_district.setText(district)
        self.line_city.setText(city)
        index = self.cbbox_state.findText(state)
        self.cbbox_state.setCurrentIndex(index)

    def set_cep_by_address(self, addresses: list):
        """
        Set CEP by complete address

        Parameters
        ----------
        addresses : list of corresponding address

        Returns
        -------
        None
        """
        if len(addresses) == 1:
            self.set_cep(addresses[0]['cep'])
        else:
            self.select_address = AddressesPopup(addresses)
            self.select_address.setFont(self.main_font)
            self.select_address.s_select_address.connect(self.set_cep)
            self.select_address.exec_()

    def set_cep(self, cep: str):
        """
        Set CEP in screen

        Parameters
        ----------
        cep : string with 8 digits

        Returns
        -------
        None
        """
        self.line_cep.setText(cep)

    def show_error_msg(self, error_msg: str):
        """
        Show dialog with error message

        Parameters
        ----------
        error_msg :  Message error

        Returns
        -------
        None
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(error_msg)
        msg.setWindowTitle("Error")
        msg.exec_()

    def show_success_msg(self, success_msg: str):
        """
        Show dialog with success message

        Parameters
        ----------
        success_msg : Success message

        Returns
        -------
        None
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(success_msg)
        msg.setWindowTitle("Success")
        msg.exec_()


class AddressesPopup(QDialog):
    s_select_address = pyqtSignal(str)

    def __init__(self, addresses):
        super().__init__()
        self.addresses = addresses
        self.init_ui()
        self.set_connections()
        self.resize(700, 100)

    def init_ui(self):
        self.lbl_select_address = QLabel("Select Address")

        self.cbbox_addresses = QComboBox()
        for address in self.addresses:
            self.cbbox_addresses.addItem(
                address['complete'],
                address['cep']
            )

        self.btn_select_address = QPushButton("Confirm")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.lbl_select_address)
        self.layout.addWidget(self.cbbox_addresses)
        self.layout.addWidget(self.btn_select_address)

        self.setLayout(self.layout)

    def set_connections(self):
        self.btn_select_address.clicked.connect(
            lambda x: self.selected_address(
                self.cbbox_addresses.currentData()
            )
        )

    def selected_address(self, cep):
        self.s_select_address.emit(cep)
        print('cep dentro ', cep)
        self.close()
