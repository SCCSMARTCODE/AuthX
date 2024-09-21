import logging
import os
from logging.handlers import SMTPHandler
from enum import Enum


class AuthXLogger:
    class Handlers:
        def __init__(self):
            self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - '
                                               'File: %(filename)s, Function: %(funcName)s, Line: %(lineno)d - %(message)s')

        class HandlerTypes(Enum):
            STREAM = 'stream'
            FILE = 'file'
            SMTP = 'smtp'

        def manage_stream(self):
            handler = logging.StreamHandler()
            handler.setLevel(logging.DEBUG)
            handler.setFormatter(self.formatter)
            return handler

        def manage_file(self, filename):
            handler = logging.FileHandler(filename)
            handler.setLevel(logging.INFO)
            handler.setFormatter(self.formatter)
            return handler

        def manage_smtp(self):
            """
            Placeholder for SMTP handling
            :return: SMTPHandler instance
            """
            pass

    def __init__(self, name='AuthXLogger', set_channels=None, level=logging.DEBUG, filename=None):
        """
        :param set_channels: list of channels to set, e.g., ['stream', 'file']
        :param level: logging level
        :param filename: file to log to (if file logging is enabled)
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        self.handler_manager = self.Handlers()

        # Default to both file and stream logging if no specific channels provided
        if set_channels is None:
            set_channels = ['stream', 'file']

        # Ensure each channel is only added once
        for channel in set_channels:
            if channel == self.handler_manager.HandlerTypes.STREAM.value:
                handler = self.handler_manager.manage_stream()
                self.logger.addHandler(handler)
            elif channel == self.handler_manager.HandlerTypes.FILE.value:
                filename = filename or f"{name}.log"
                handler = self.handler_manager.manage_file(filename)
                self.logger.addHandler(handler)
            # elif channel == self.handler_manager.HandlerTypes.SMTP.value:
            #     handler = self.handler_manager.manage_smtp()
            #     if handler:
            #         self.logger.addHandler(handler)
