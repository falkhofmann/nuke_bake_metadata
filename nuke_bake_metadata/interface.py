"""Interface module to be used from within Nuke."""

try:
    # < Nuke 11
    import PySide.QtCore as QtCore
    import PySide.QtGui as QtGui
    import PySide.QtGui as QtGuiWidgets
except ImportError:
    # >= Nuke 11
    import PySide2.QtCore as QtCore
    import PySide2.QtGui as QtGui
    import PySide2.QtWidgets as QtGuiWidgets

from nuke_bake_metadata.constants import STYLES
from nuke_bake_metadata import utils


METADATA_BOX = None


class Button(QtGuiWidgets.QPushButton):
    """Custom Pushbutton to change color when mouse enters adn leaves."""

    def __init__(self, text):
        super(Button, self).__init__()
        self.setMouseTracking(True)
        self.setText(text)
        self.setStyleSheet(STYLES['regular'])
        self.setMinimumWidth(100)
        self.setMaximumWidth(150)

    def enterEvent(self, event):  # pylint: disable=invalid-name,unused-argument
        """Signal event when mouse enters boundaries of button.

        Args:
            event: Unused Event but necessary

        """
        self.setStyleSheet(STYLES['orange'])

    def leaveEvent(self, event):  # pylint: disable=invalid-name,unused-argument
        """Signal event when mouse enters boundaries of button.

        Args:
            event: Unused Event but necessary

        """
        self.setStyleSheet(STYLES['regular'])


class SearchLine(QtGuiWidgets.QLineEdit):  # pylint: disable=too-few-public-methods
    """LineEdit with combined Completer"""

    def __init__(self, table, metadata):
        super(SearchLine, self).__init__()
        self.table = table
        self.metadata = metadata
        self.setPlaceholderText('search for metadata key...')
        self.completer = QtGuiWidgets.QCompleter(self.metadata.keys(), self)
        self.completer.setCompletionMode(QtGuiWidgets.QCompleter.PopupCompletion)
        self.setCompleter(self.completer)

        self.completer.activated.connect(self._complete)

    def _complete(self, item):
        """Call add_row method on table object.

        Args:
            item (str): Completed item.

        """
        self.table.add_row(self.metadata, item)


class RangeLine(QtGuiWidgets.QLineEdit):  # pylint: disable=too-few-public-methods
    """LineEdit validator to only accepts digits as input."""

    def __init__(self, placeholder):
        super(RangeLine, self).__init__()
        self.setPlaceholderText(placeholder)
        regex = QtCore.QRegExp(r"\d+")
        self.setValidator(QtGui.QRegExpValidator(regex, self))


class Table(QtGuiWidgets.QTableWidget):  # pylint: disable=too-few-public-methods
    """Table with specific settings and add_row method."""

    def __init__(self, node):
        super(Table, self).__init__()
        self.node = node
        header_items = ['Key', 'Type']

        self.setSortingEnabled(True)
        self.setColumnCount(len(header_items))
        self.setHorizontalHeaderLabels(header_items)
        self.setSelectionBehavior(QtGuiWidgets.QAbstractItemView.SelectRows)
        header = self.horizontalHeader()
        header.setMinimumSectionSize(100)
        header.setStretchLastSection(True)
        self.verticalHeader().setVisible(False)

    def add_row(self, metadata, item):
        """Add a single row to the table.

        Args:
            metadata (dict): Metadata from node.
            item (str): Completed item from user input.

        """

        key = TableItem(item, metadata)
        type_ = TableItem(utils.get_value_type(self.node, metadata[item]))

        row = self.rowCount()
        self.insertRow(row)
        self.setItem(row, 0, key)
        self.setItem(row, 1, type_)


class TableItem(QtGuiWidgets.QTableWidgetItem):  # pylint: disable=too-few-public-methods
    """Table iwdget to hold metadata dict."""

    def __init__(self, item, metadata=None):
        super(TableItem, self).__init__()
        self.metadata = metadata
        self.setText(item)


class Interface(QtGuiWidgets.QWidget):  # pylint: disable=too-many-instance-attributes
    """Interface in interact with user.

    Holds a search inout, table, range inputs and cancel/confirm buttons.

    """
    def __init__(self, node, metadata):
        super(Interface, self).__init__()
        self.node = node
        self. metadata = metadata
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setMinimumSize(800, 300)

        self.table = Table(self.node)
        self.line_edit = SearchLine(self.table, self.metadata)

        self.first = RangeLine('first')
        self.last = RangeLine('last')

        self.cancel_button = Button('cancel')
        self.bake_button = Button('bake')

        space = 500

        range_layout = QtGuiWidgets.QHBoxLayout()
        range_layout.addSpacing(space)
        range_layout.addWidget(self.first)
        range_layout.addWidget(self.last)

        button_layout = QtGuiWidgets.QHBoxLayout()
        button_layout.addSpacing(space)
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.bake_button)

        main_layout = QtGuiWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        main_layout.addWidget(self.line_edit)
        main_layout.addWidget(self.table)
        main_layout.addLayout(range_layout)
        main_layout.addLayout(button_layout)

        self.cancel_button.clicked.connect(self.cancel)
        self.bake_button.clicked.connect(self.bake_keys)

    def bake_keys(self):
        """Bake each item in table into keyframes."""

        for line in (self.first, self.last):
            if not line.text().strip():
                self.first.setStyleSheet(STYLES['red'])
                return

        noop = utils.create_node(self.node)
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            key = item.text()
            m_key = item.metadata[key]
            utils.create_numerical_animation(self.node,
                                             noop,
                                             m_key,
                                             key,
                                             int(self.first.text()),
                                             int(self.last.text())
                                            )
        self.cancel()

    def cancel(self):
        """Close the widget."""
        self.close()

    def keyPressEvent(self, event):  # pylint: disable=invalid-name
        """Catch user key press events and handle them."""
        if event.key() == QtCore.Qt.Key_Escape:
            self.cancel()


def start_from_nuke():
    """Start up function from within nuke."""
    node = utils.get_node()
    metadata = utils.get_metadata(node)
    if metadata:
        global METADATA_BOX  # pylint: disable=global-statement
        METADATA_BOX = Interface(node, metadata)
        METADATA_BOX.show()
