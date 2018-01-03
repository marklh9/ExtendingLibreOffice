import logging
import unohelper

from com.sun.star.frame import XDispatch


def show_msg(title, msg, toolkit, frame):
    from com.sun.star.awt.MessageBoxType import INFOBOX
    from com.sun.star.awt.MessageBoxButtons import DEFAULT_BUTTON_OK
    msgbox = toolkit.createMessageBox(frame.getContainerWindow(), INFOBOX,
                                      DEFAULT_BUTTON_OK, title, msg)
    msgbox.execute()


class SampleDispatch(unohelper.Base, XDispatch):
    def __init__(self, ctx, args):
        self.ctx = ctx
        self.frame = args
        self.toolkit = ctx.getServiceManager(). \
            createInstanceWithContext("com.sun.star.awt.Toolkit", ctx)

    def dispatch(self, url, args):
        try:
            show_msg("dispatch", "Hello, there!", self.toolkit, self.frame)
        except:
            logging.exception("dispatch")
        finally:
            return

    def addStatusListener(self, listener, url):
        return

    def removeStatusListener(self, listener, url):
        return


g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(
    SampleDispatch,
    "addons.ExtendingLibreOffice.ProtocolHandler.SampleDispatch",
    ("com.sun.star.frame.XDispatch",), )
