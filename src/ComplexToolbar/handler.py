import logging
import unohelper

from com.sun.star.frame import XDispatchProvider
from com.sun.star.lang import XInitialization


#logging.basicConfig(filename='/tmp/complex_toolbar.txt', level=logging.DEBUG)

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
        if url.Protocol == "addons.ExtendingLibreOffice.ComplexToolbar.DummyProtocol:":
            smgr = self.ctx.getServiceManager()
            dispatch = smgr.createInstanceWithArgumentsAndContext(
                "addons.ExtendingLibreOffice.ComplexToolbar.SampleDispatch",
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
    "addons.ExtendingLibreOffice.ComplexToolbar.SampleHandler",
    ("com.sun.star.frame.ProtocolHandler",), )
