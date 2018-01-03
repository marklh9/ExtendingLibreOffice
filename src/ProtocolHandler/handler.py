import logging
import unohelper

from com.sun.star.frame import XDispatchProvider
from com.sun.star.lang import XInitialization


#logging.basicConfig(filename='/tmp/protocl_handler.txt', level=logging.DEBUG)

class SampleHandler(unohelper.Base, XDispatchProvider, XInitialization):
    def __init__(self, ctx):
        self.ctx = ctx
        self.frame = None
        self.toolkit = ctx.getServiceManager(). \
            createInstanceWithContext("com.sun.star.awt.Toolkit", ctx)

    def initialize(self, objs):
        if len(objs) > 0:
            self.frame = objs[0]
        return

    def queryDispatch(self, url, target, searchflags):
        if url.Protocol == "Dummy:" and url.Path == "do_something":
            smgr = self.ctx.getServiceManager()
            dispatch = smgr.createInstanceWithArgumentsAndContext(
                "addons.ExtendingLibreOffice.ProtocolHandler.SampleDispatch",
                (self.frame, ), self.ctx)
            return dispatch
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
