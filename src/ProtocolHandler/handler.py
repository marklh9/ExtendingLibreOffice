import logging
import unohelper

from com.sun.star.frame import XDispatch
from com.sun.star.frame import XDispatchProvider
from com.sun.star.lang import XInitialization


# logging.basicConfig(filename='/tmp/protocl_handler.txt', level=logging.DEBUG)

def show_msg(title, msg, toolkit, frame):
    from com.sun.star.awt.MessageBoxType import INFOBOX
    from com.sun.star.awt.MessageBoxButtons import DEFAULT_BUTTON_OK
    msgbox = toolkit.createMessageBox(frame.getContainerWindow(), INFOBOX, \
                                      DEFAULT_BUTTON_OK, title, msg)
    msgbox.execute()


class SampleHandler(unohelper.Base, XDispatchProvider, XDispatch, XInitialization):
    def __init__(self, ctx):
        self.ctx = ctx
        self.frame = None
        self.toolkit = ctx.getServiceManager(). \
            createInstanceWithContext("com.sun.star.awt.Toolkit", ctx)

    def initialize(self, objs):
        logging.debug("initialize called.")
        if len(objs) > 0:
            self.frame = objs[0]
        return

    def dispatch(self, url, args):
        try:
            show_msg("dispatch", "do_something", self.toolkit, self.frame)
        except:
            logging.exception("dispatch")
        finally:
            return

    def addStatusListener(self, listener, url):
        logging.debug("addStatusListener:" + str(url))
        return

    def removeStatusListener(self, listener, url):
        logging.debug("removeStatusListener:" + str(url))
        return

    def queryDispatch(self, url, target, searchflags):
        logging.debug("queryDispatch url:" + str(url))
        if url.Protocol == "Dummy:" and url.Path == "do_something":
            return self
        return None

    def queryDispatches(self, requests):
        result = []
        for item in requests:
            result.append(self.queryDispatch(item.FeatureURL, item.FrameName, item.SearchFlags))
        return tuple(result)


g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(
    SampleHandler,
    "addons.ExtendingLibreOffice.ProtocolHandler.SampleHandler",
    ("com.sun.star.frame.ProtocolHandler",), )
