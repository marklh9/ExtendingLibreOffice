import uno
import unohelper
from com.sun.star.awt import XContainerWindowEventHandler

import logging

#logging.basicConfig(filename='d:\\temp.txt', level=logging.DEBUG)


class DialogHandler(unohelper.Base, XContainerWindowEventHandler):
    model_state = 0

    def __init__(self, ctx):
        self.ctx = ctx

    def getSupportedMethodNames(self):
        return ["external_event"]

    def callHandlerMethod(self, aWindow, aEventObject, sMethodName):
        try:
            if sMethodName == "external_event":
                control = aWindow.getControl("CheckBox1")
                model = control.getModel()
                logging.debug("callHandlerMethod:" +aEventObject )
                if aEventObject == "ok":
                    DialogHandler.model_state = model.State
                    return True
                elif aEventObject == "back" or aEventObject == "initialize":
                    model.State = DialogHandler.model_state
                    return True
        except Exception as e:
            #logging.exception("exception in callHandlerMethod")
            #logging.debug("Exception is " + str(e))
            pass
        finally:
            return False


g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(
    DialogHandler,
    "addons.ExtendingLibreOffice.OptionDialog.DialogHandler",
    ("com.sun.star.task.Job",), )
