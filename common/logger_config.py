#-*-coding:utf8;-*-
# qpy:3
'''
@author: 2017 jingl3s at yopmail dot com
'''

# license
# 
# This code is free software; you can redistribute it and/or modify it
# under the terms of the DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE (see the file
# LICENSE included with the distribution).


import os
# import time
import logging
# import logging.handlers

class LoggerConfig(object):
    '''
    classdocs
    '''

    def __init__(self, output_dir, file_basename):
        '''
        Constructor
        '''
        self.__logger = None
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        self.__initialize_logger(output_dir, file_basename)

    def __initialize_logger(self, output_dir, file_basename):
        '''
        Method permettant de definir le logger
        '''
        self.__logger = logging.getLogger()
        self.__logger.setLevel(logging.WARNING)
        formatter = logging.Formatter(
            "%(asctime)s-%(levelname)7s-%(funcName)s-%(message)s")

        # create console handler and set level to info
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.__logger.addHandler(handler)

        # create error file handler and set level to error
#         handler = logging.FileHandler(os.path.join(output_dir, file_basename + "_" +  time.strftime("%Y.%m.%d_%H.%M.%S") + ".log"),"w", encoding=None, delay="true")
#         handler.setFormatter(formatter)
#         self.__logger.addHandler(handler)

        # create error file handler rotating and set level to error
#         if os.path.exists(output_dir):
#             log_file = os.path.join(output_dir, file_basename + ".log")
#         else:
#             log_file = file_basename + ".log"
# 
#         handler = logging.handlers.RotatingFileHandler(log_file, "w", maxBytes=2097152,
#                                                        backupCount=2)
# 
#         handler.setFormatter(formatter)
#         self.__logger.addHandler(handler)

    def get_logger(self):
        '''
        Retourne le logger actuel
        '''
        return self.__logger
