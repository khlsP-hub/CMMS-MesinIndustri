# views/UI/styles.py

GLOBAL_STYLESHEET = """
QWidget#sidebar {
    background-color: #E8E8E8;
}
QWidget#sidebar QLabel {
    color: #333333;
    background-color: transparent;
}
QWidget#sidebar QPushButton {
    background-color: #D0D0D0;
    color: #222222;
    border: none;
    padding: 12px;
    font-size: 16px;
    font-family: Roboto;
    text-align: left;
    border-radius: 5px;
}
QWidget#sidebar QPushButton:hover {
    background-color: #C0C0C0;
}
QWidget#sidebar QPushButton:pressed {
    background-color: #B0B0B0;
}
QWidget#contentArea {
    background-color: #F4F4F4;
    font-family: Roboto;
}
QWidget#contentArea QLabel {
    background-color: transparent;
}
QPushButton#machineButton {
    background-color: #FFFFFF;
    border: 1px solid #DDDDDD;
    border-radius: 5px;
    font-size: 15px;
}
QPushButton#machineButton:hover {
    background-color: #F0F0F0;
}
QFrame#historyItemFrame {
    background-color: #FFFFFF;
    border: 1px solid #E0E0E0;
    border-radius: 5px;
    padding: 10px;
    margin-bottom: 8px;
}
QFrame#imageCard {
    background-color: #FFFFFF;
    border: 1px solid #DDDDDD;
    border-radius: 8px;
}
QFrame#imageCard:hover {
    background-color: #F9F9F9;
    border: 1px solid #C0C0C0;
}
QFrame#textCard {
    background-color: #FFFFFF;
    border: 1px solid #DDDDDD;
    border-radius: 8px;
}
QFrame#textCard:hover {
    background-color: #F9F9F9;
    border: 1px solid #C0C0C0;
}
QScrollArea {
    border: none;
    background-color: #F4F4F4;
}
/* Konten di dalam area scroll */
QWidget#scrollAreaWidgetContents {
    background-color: #F4F4F4; 
}
QWidget {
    background-color: transparent;
    color: #333;
}
"""