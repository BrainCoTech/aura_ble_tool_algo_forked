# -*- coding: utf-8 -*-
import inspect
import os

from PySide6.QtCore import QTranslator
from PySide6.QtWidgets import QApplication
from src.utils.path import APP_ROOT_PATH


class LanguageSupport(object):  # 只支持中文和英文
    def __init__(self, default_type='English'):
        self.language_type = default_type
        self.support_language = ['Chinese', 'English']
        self.translate_operator_list = []
        self.setup()

    def setup(self):
        translate_path = os.path.join(APP_ROOT_PATH, 'translate')

        if self.language_type == "Chinese":
            suffix = '.qm'
        else:
            suffix = '.ts'

        if os.path.exists(translate_path):
            if self.language_type == "Chinese":
                qm_files = []
                self.translate_operator_list.clear()
                for root, dirs, files in os.walk(translate_path):
                    for file in files:
                        if file.endswith('.qm'):
                            qm_files.append(os.path.join(root, file))

                for index, qm_file in enumerate(qm_files):
                    translate = QTranslator()
                    QApplication.installTranslator(translate)
                    translate.load(str(qm_file))
                    self.translate_operator_list.append(translate)
            else:
                for translate in self.translate_operator_list:
                    QApplication.removeTranslator(translate)

    def change_language(self, language_style: str):
        if language_style in self.support_language:
            self.language_type = language_style
            self.setup()

