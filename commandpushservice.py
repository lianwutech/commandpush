#!/usr/bin/env python
# -*- coding:utf-8 -*-

import win32serviceutil
import win32service   
import win32event

import logging  
import inspect

from setting import *
import commandpush

class CommandPushService(win32serviceutil.ServiceFramework):
    _svc_name_ = ""
    _svc_display_name_ = "Jambu Command Push Service"
    _svc_description_ = "This is a command push tools, run as a windows service."
  
    def __init__(self, args):   
        win32serviceutil.ServiceFramework.__init__(self, args)   
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)  
        self.logger = self._getLogger()
          
    def _getLogger(self):
        logger = logging.getLogger('[CommandPushService]')

        this_file = inspect.getfile(inspect.currentframe())  
        dirpath = os.path.abspath(os.path.dirname(this_file))  
        handler = logging.FileHandler(os.path.join(dirpath, "command_push_service.log"))

        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')  
        handler.setFormatter(formatter)  

        logger.addHandler(handler)  
        logger.setLevel(logging.INFO)
        return logger

    def SvcDoRun(self):  
        import time  
        self.logger.info("command push service is run....")
        commandpush.run()
              
    def SvcStop(self):   
        self.logger.info("command push service is stop....")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)   
        win32event.SetEvent(self.hWaitStop)   
        commandpush.stop()
  
if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(CommandPushService)