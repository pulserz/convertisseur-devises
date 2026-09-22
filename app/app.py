from PySide6 import QtWidgets
import currency_converter

class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.c = currency_converter.CurrencyConverter()
        self.setWindowTitle("Convertisseur de devises")
        self.setup_ui()
        self.set_default_values()
        self.setup_connections()
        self.setup_css()
        self.resize(500, 50)

    def setup_ui(self):
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.cbb_devisesFrom = QtWidgets.QComboBox()
        self.spn_montant = QtWidgets.QDoubleSpinBox()
        self.cbb_devisesTo = QtWidgets.QComboBox()
        self.spn_montantConverti = QtWidgets.QDoubleSpinBox()
        self.btn_inverser = QtWidgets.QPushButton("Inverser devises")

        self.main_layout.addWidget(self.cbb_devisesFrom)
        self.main_layout.addWidget(self.spn_montant)
        self.main_layout.addWidget(self.cbb_devisesTo)
        self.main_layout.addWidget(self.spn_montantConverti)
        self.main_layout.addWidget(self.btn_inverser)

    def setup_css(self):
        self.setWindowIcon(self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_BrowserReload))
        self.btn_inverser.setObjectName("btn_inverser")
        self.setStyleSheet("""
           QWidget {
                background-color: #1e1e2e;
                color: #cdd6f4;
                font-size: 10pt;
            }
            QComboBox, QDoubleSpinBox {
                background-color: #313244;
                border: 1px solid #45475a;
                border-radius: 6px;
                padding: 6px;
            }
            QPushButton#btn_inverser {
                background-color: #89b4fa;
                color: #1e1e2e;
                font-weight: bold;
                border-radius: 6px;
                padding: 8px 14px;
            }
            QPushButton#btn_inverser:hover {
                background-color: #b4befe;
            }
        """)

    def set_default_values(self):
        self.cbb_devisesFrom.addItems(sorted(list(self.c.currencies or set())))
        self.cbb_devisesTo.addItems(sorted(list(self.c.currencies or set())))
        self.cbb_devisesFrom.setCurrentText("EUR")
        self.cbb_devisesTo.setCurrentText("EUR")

        self.spn_montant.setRange(1, 1000000000)
        self.spn_montantConverti.setRange(1, 1000000000)
        self.spn_montant.setValue(100)
        self.spn_montantConverti.setValue(100)
        
    def setup_connections(self):
        self.cbb_devisesFrom.activated.connect(self.compute)
        self.cbb_devisesTo.activated.connect(self.compute)
        self.spn_montant.valueChanged.connect(self.compute)
        self.btn_inverser.clicked.connect(self.inverser_devise)

    def compute(self):
        montant = self.spn_montant.value()
        devise_from = self.cbb_devisesFrom.currentText()
        devise_to = self.cbb_devisesTo.currentText()

        try: 
            result = self.c.convert(montant, devise_from, devise_to)
        except currency_converter.currency_converter.RateNotFoundError:
            print("La conversion n'a pas fonctionné.")
        else:
            self.spn_montantConverti.setValue(float(result))

    def inverser_devise(self):
        devise_from = self.cbb_devisesFrom.currentText()
        devise_to = self.cbb_devisesTo.currentText()

        self.cbb_devisesFrom.setCurrentText(devise_to)
        self.cbb_devisesTo.setCurrentText(devise_from)

        self.compute()

app = QtWidgets.QApplication([])
win = App()
win.show()
app.exec()