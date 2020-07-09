# -*- coding: utf-8 -*-
"""

    mslib.msui.mscolab_project
    ~~~~~~~~~~~~~~~~~~~~~

    Mscolab project window, to display chat, file change

    This file is part of mss.

    :copyright: 2019 Shivashis Padhi
    :license: APACHE-2.0, see LICENSE for details.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
import datetime
import json

import requests
from markdown import Markdown
from markdown.extensions import Extension
from werkzeug.urls import url_join

from mslib.msui import MissionSupportSystemDefaultConfig as mss_default
from mslib.msui.mss_qt import Qt, QtCore, QtGui, QtWidgets, ui_mscolab_project_window as ui
from mslib.utils import config_loader


# We need to override the KeyPressEvent in QTextEdit to disable the default behaviour of enter key.
class MessageTextEdit(QtWidgets.QTextEdit):
    def keyPressEvent(self, event):
        # Shift + Enter for new line
        if event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter) and event.modifiers() & QtCore.Qt.ShiftModifier:
            cursor = self.textCursor()
            cursor.insertText("\n")
            self.setTextCursor(cursor)
            return
        # Only Enter for send/edit message
        elif event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
            chat_window = self.parent().parent().parent()
            if chat_window.active_edit_id is None:
                chat_window.send_message()
            else:
                chat_window.edit_message()
            return
        super().keyPressEvent(event)


class MSColabProjectWindow(QtWidgets.QMainWindow, ui.Ui_MscolabProject):
    """Derives QMainWindow to provide some common functionality to all
       MSUI view windows.
    """
    name = "MSColab Project Window"
    identifier = None

    viewCloses = QtCore.pyqtSignal(name="viewCloses")
    reloadWindows = QtCore.pyqtSignal(name="reloadWindows")

    def __init__(self, token, p_id, user, project_name, access_level, conn, parent=None,
                 mscolab_server_url=config_loader(dataset="default_MSCOLAB", default=mss_default.default_MSCOLAB)):
        """
        token: access_token
        p_id: project id
        user: logged in user
        project_name: active project name,
        access_level: access level of user logged in
        conn: to send messages, recv messages, if a direct slot-signal can't be setup
            to be connected at parents'
        parent: widget parent
        mscolab_server_url: server url for mscolab
        """
        super(MSColabProjectWindow, self).__init__(parent)
        self.setupUi(self)

        self.mscolab_server_url = mscolab_server_url
        self.token = token
        self.user = user
        self.p_id = p_id
        self.project_name = project_name
        self.conn = conn
        self.access_level = access_level
        self.text = ""
        self.messages = []
        self.active_edit_id = None
        self.markdown = Markdown(extensions=['nl2br', 'sane_lists', DeregisterSyntax()])
        self.messageText = MessageTextEdit(self.centralwidget)
        self.setup_message_text()
        # Signals
        self.previewBtn.clicked.connect(self.toggle_preview)
        self.sendMessageBtn.clicked.connect(self.send_message)
        self.editMessageBtn.clicked.connect(self.edit_message)
        self.cancelEditBtn.clicked.connect(self.cancel_message_edit)
        # Socket Connection handlers
        self.conn.signal_message_receive.connect(self.handle_incoming_message)
        self.conn.signal_message_edited.connect(self.handle_message_edited)
        self.conn.signal_message_deleted.connect(self.handle_deleted_message)
        # Set Label text
        self.set_label_text()
        # Hide Edit Message section
        self.cancel_message_edit()
        # load all users
        self.load_users()
        # load messages
        self.load_all_messages()

    # UI SET UP METHODS
    def setup_message_text(self):
        self.messageText.setAcceptRichText(False)
        self.messageText.setTextInteractionFlags(
            QtCore.Qt.LinksAccessibleByKeyboard | QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextBrowserInteraction |
            QtCore.Qt.TextEditable | QtCore.Qt.TextEditorInteraction | QtCore.Qt.TextSelectableByKeyboard |
            QtCore.Qt.TextSelectableByMouse)
        self.messageText.setPlaceholderText("Enter message here.\nPress enter to send.\nShift+Enter to add a new line.")
        self.messageText.setObjectName("messageText")
        vbox_layout = QtWidgets.QVBoxLayout()
        vbox_layout.addWidget(self.messageText)
        vbox_layout.setSpacing(0)
        vbox_layout.setContentsMargins(0, 0, 0, 0)
        self.messageTextContainer.setLayout(vbox_layout)

    def set_label_text(self):
        self.user_info.setText(f"Logged in: {self.user['username']}")
        self.proj_info.setText(f"Project: {self.project_name}")

    # Signal Slots
    def toggle_preview(self):
        # Go Back to text box
        if self.messageText.isReadOnly():
            self.messageText.setHtml("")
            self.messageText.setText(self.text)
            self.messageText.moveCursor(QtGui.QTextCursor.End)
            self.messageText.setReadOnly(False)
            self.messageText.setStyleSheet("")
            self.previewBtn.setDefault(False)
            self.previewBtn.setText("Preview")
        # Show preview
        else:
            self.text = self.messageText.toPlainText()
            html = self.markdown.convert(self.text)
            self.messageText.setHtml(html)
            self.messageText.setReadOnly(True)
            self.messageText.setStyleSheet("background: #eff0f1")
            self.previewBtn.setDefault(True)
            self.previewBtn.setText("Write")

    def send_message(self):
        """
        send message through connection
        """
        message_text = self.messageText.toPlainText()
        if message_text == "":
            return
        message_text = message_text.strip()
        self.conn.send_message(message_text, self.p_id)
        self.messageText.clear()

    def start_message_edit(self, message_text, message_id):
        self.active_edit_id = message_id
        self.messageText.setText(message_text)
        self.messageText.setFocus()
        self.messageText.moveCursor(Qt.QTextCursor.End)
        self.editMessageBtn.setVisible(True)
        self.cancelEditBtn.setVisible(True)
        self.sendMessageBtn.setVisible(False)

    def cancel_message_edit(self):
        self.active_edit_id = None
        self.messageText.clear()
        self.editMessageBtn.setVisible(False)
        self.cancelEditBtn.setVisible(False)
        self.sendMessageBtn.setVisible(True)

    def edit_message(self):
        new_message_text = self.messageText.toPlainText()
        if new_message_text == "":
            self.conn.delete_message(self.active_edit_id, self.p_id)
        else:
            new_message_text = new_message_text.strip()
            self.conn.edit_message(self.active_edit_id, new_message_text, self.p_id)
        self.cancel_message_edit()

    # API REQUESTS

    def load_users(self):
        # load users to side-tab here
        # make request to get users
        data = {
            "token": self.token,
            "p_id": self.p_id
        }
        url = url_join(self.mscolab_server_url, 'authorized_users')
        r = requests.get(url, data=data)
        if r.text == "False":
            # show QMessageBox errors here
            pass
        else:
            self.collaboratorsList.clear()
            users = json.loads(r.text)["users"]
            for user in users:
                item = QtWidgets.QListWidgetItem("{} - {}".format(user["username"],
                                                 user["access_level"]),
                                                 parent=self.collaboratorsList)
                item.username = user["username"]
                self.collaboratorsList.addItem(item)

    def load_all_messages(self):
        # empty messages and reload from server
        data = {
            "token": self.token,
            "p_id": self.p_id,
            "timestamp": datetime.datetime(1970, 1, 1).strftime("%Y-%m-%d, %H:%M:%S")
        }
        # returns an array of messages
        url = url_join(self.mscolab_server_url, "messages")
        res = requests.get(url, data=data).json()
        messages = res["messages"]
        # clear message box
        for message in messages:
            self.render_new_message(message, scroll=False)
        self.messageList.scrollToBottom()

    def render_new_message(self, message, scroll=True):
        message_item = MessageItem(message, self)
        list_widget_item = QtWidgets.QListWidgetItem(self.messageList)
        list_widget_item.setSizeHint(message_item.sizeHint())
        self.messageList.addItem(list_widget_item)
        self.messageList.setItemWidget(list_widget_item, message_item)
        if scroll:
            self.messageList.scrollToBottom()

    # SOCKET HANDLERS
    @QtCore.Slot(str)
    def handle_incoming_message(self, message):
        message = json.loads(message)
        self.render_new_message(message)

    @QtCore.Slot(str)
    def handle_message_edited(self, message):
        message = json.loads(message)
        message_id = message["message_id"]
        new_message_text = message["new_message_text"]
        # Loop backwards because it's more likely the message is new than old
        for i in range(self.messageList.count() - 1, -1, -1):
            item = self.messageList.item(i)
            message_widget = self.messageList.itemWidget(item)
            if message_widget.id == message_id:
                message_widget.update_text(new_message_text)
                item.setSizeHint(message_widget.sizeHint())
                break

    @QtCore.Slot(str)
    def handle_deleted_message(self, message):
        message = json.loads(message)
        message_id = message["message_id"]
        # Loop backwards because it's more likely the message is new than old
        for i in range(self.messageList.count() - 1, -1, -1):
            item = self.messageList.item(i)
            message_widget = self.messageList.itemWidget(item)
            if message_widget.id == message_id:
                self.messageList.takeItem(i)
                break

    def closeEvent(self, event):
        self.viewCloses.emit()


class MessageItem(QtWidgets.QWidget):
    def __init__(self, message, chat_window):
        super(MessageItem, self).__init__()
        self.id = message["id"]
        self.u_id = message["u_id"]
        self.username = message["username"]
        self.message_text = message["text"]
        self.system_message = message["system_message"]
        self.time = message["time"]
        self.chat_window = chat_window
        self.messageTextBox = QtWidgets.QTextBrowser()
        self.context_menu = QtWidgets.QMenu(self)
        self.textArea = QtWidgets.QWidget()
        self.setup_message_box()
        self.setup_message_box_layout()
        self.setup_context_menu()

    def setup_message_box(self):
        html = self.chat_window.markdown.convert(self.message_text)
        self.messageTextBox.setHtml(html)
        self.messageTextBox.setOpenLinks(False)
        self.messageTextBox.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.messageTextBox.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.messageTextBox.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.messageTextBox.setAttribute(103)
        self.messageTextBox.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.messageTextBox.customContextMenuRequested.connect(self.open_context_menu)
        self.messageTextBox.anchorClicked.connect(self.on_link_click)
        self.messageTextBox.show()
        self.messageTextBox.setFixedHeight(
            self.messageTextBox.document().size().height() + self.messageTextBox.contentsMargins().top() * 2
        )

    def setup_message_box_layout(self):
        container_layout = QtWidgets.QHBoxLayout()
        text_area_layout = QtWidgets.QVBoxLayout()
        if self.chat_window.user["username"] == self.username:
            text_area_layout.addWidget(self.messageTextBox)
            self.textArea.setLayout(text_area_layout)
            container_layout.addStretch()
            container_layout.addWidget(self.textArea)
        else:
            username_label = QtWidgets.QLabel(f"{self.username}")
            username_label.setContentsMargins(2, 5, 5, 0)
            label_font = QtGui.QFont()
            label_font.setBold(True)
            username_label.setFont(label_font)
            text_area_layout.addWidget(username_label)
            text_area_layout.addWidget(self.messageTextBox)
            self.textArea.setLayout(text_area_layout)
            container_layout.addWidget(self.textArea)
            container_layout.addStretch()
        self.textArea.layout().setSpacing(0)
        self.textArea.layout().setContentsMargins(5, 0, 5, 0)
        container_layout.setSpacing(0)
        container_layout.setContentsMargins(5, 5, 5, 5)
        self.set_message_style()
        self.setLayout(container_layout)

    def set_message_style(self):
        sent_msg_color = "#dcf8c6"
        recv_msg_color = "#eff0f1"
        system_msg_color = "#a9d3e0"
        if self.chat_window.user["username"] == self.username:
            border = "border-top-left-radius: 5px; border-bottom-left-radius: 5px; border-bottom-right-radius: 5px"
            color = sent_msg_color
        else:
            border = "border-top-right-radius: 5px; border-bottom-left-radius: 5px; border-bottom-right-radius: 5px"
            color = recv_msg_color
        if self.system_message:
            color = system_msg_color
        self.messageTextBox.setStyleSheet("background: transparent; border: none;")
        self.textArea.setStyleSheet(f"background: {color}; {border}")

    def setup_context_menu(self):
        copy_action = self.context_menu.addAction("Copy")
        edit_action = self.context_menu.addAction("Edit")
        delete_action = self.context_menu.addAction("Delete")
        copy_action.triggered.connect(self.handle_copy_action)
        edit_action.triggered.connect(self.handle_edit_action)
        delete_action.triggered.connect(self.handle_delete_action)
        if self.username != self.chat_window.user["username"] or self.system_message is True:
            if self.system_message is True:
                copy_action.setVisible(False)
            edit_action.setVisible(False)
            delete_action.setVisible(False)

    def open_context_menu(self, pos):
        self.context_menu.exec_(self.messageTextBox.mapToGlobal(pos))

    def handle_copy_action(self):
        Qt.QApplication.clipboard().setText(self.message_text)

    def handle_edit_action(self):
        self.chat_window.start_message_edit(self.message_text, self.id)

    def handle_delete_action(self):
        # disable edit message section if it's active before deleting
        self.chat_window.cancel_message_edit()
        self.chat_window.conn.delete_message(self.id, self.chat_window.p_id)

    def update_text(self, message_text):
        self.message_text = message_text
        html = self.chat_window.markdown.convert(self.message_text)
        self.messageTextBox.setHtml(html)
        self.messageTextBox.setFixedHeight(
            self.messageTextBox.document().size().height() + self.messageTextBox.contentsMargins().top() * 2
        )
        self.textArea.adjustSize()

    def on_link_click(self, url):
        if url.scheme() == "":
            url.setScheme("http")
        Qt.QDesktopServices.openUrl(url)


# Deregister all the syntax that we don't want to allow
# Can't find any part in documentation where all the syntax names are mentioned
# For future reference to syntax name refer to:
# https://github.com/Python-Markdown/markdown/blob/a06659b62209de98cbc23715addb2b768a245788/markdown/core.py#L100
class DeregisterSyntax(Extension):
    """
    Current Supported syntax:
    *text* : emphasis
    **text** : bold
    - text : unordered list
    1. text : ordered list
    # text : Heading
    [text](link) : link
    <link> : clickable link
    """
    def extendMarkdown(self, md):
        # Deregister block syntax
        md.parser.blockprocessors.deregister('setextheader')
        md.parser.blockprocessors.deregister('hr')
        md.parser.blockprocessors.deregister('quote')

        # Deregister inline syntax
        md.inlinePatterns.deregister('reference')
        md.inlinePatterns.deregister('image_link')
        md.inlinePatterns.deregister('image_reference')
        md.inlinePatterns.deregister('short_reference')
        md.inlinePatterns.deregister('automail')
        md.inlinePatterns.deregister('linebreak')
        md.inlinePatterns.deregister('html')
        md.inlinePatterns.deregister('entity')
