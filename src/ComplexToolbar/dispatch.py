import logging
import unohelper
import uno

from com.sun.star.frame import XDispatch
from status_listener import StatusListenerWrapper

#logging.basicConfig(filename='/tmp/complex_toolbar.txt', level=logging.DEBUG)

IMAGE_URL = "vnd.sun.star.extension://addons.ExtendingLibreOffice.ComplexToolbar/star.png"

class SampleDispatch(unohelper.Base, XDispatch):
    def __init__(self, ctx, args):
        self.ctx = ctx
        self.frame = args
        self.toolkit = ctx.getServiceManager(). \
            createInstanceWithContext("com.sun.star.awt.Toolkit", ctx)
        self.image_button = None
        self.list_item = None

    def dispatch(self, url, args):
        try:
            logging.debug("dispatch url.Path="+url.Path)
            if url.Path == "ImageButton" and self.image_button is not None:
                StatusListenerWrapper( listener, url ).send_command( "SetImage", "URL", IMAGE_URL )
        except:
            logging.exception("dispatch")
        finally:
            return


    def addStatusListener(self, listener, url):
        try:
            x = StatusListenerWrapper( listener, url )
            logging.debug("addStatusListener Path="+url.Path)
            if url.Path == "ImageButton":
                x.send_command( "SetImage", "URL", IMAGE_URL )
                self.image_button = listener

            if url.Path == "Combobox" or \
                    url.Path == "Dropdownbox" or \
                    url.Path == "DropdownButton" or \
                    url.Path == "ToggleDropdownButton":
                thelist = uno.Any( "[]string", ("Apple","Banana","Orange") )
                x.send_command( "SetList", "List", thelist )
                x.send_command( "AddEntry", "Text", "Peach" )
                x.send_command( "AddEntry", "Text", "Melon" )
                x.send_command( "SetDropDownLines", "Lines", 2 )

            if url.Path == "Spinfield":
                args = { "Value" : value, "Step" : step, "LowerLimit": lower, "UpperLimit" : upper }
                x.send_command_with_args( "SetValues", args )

            if url.Path == "Editfield" or url.Path == "Combobox":
                x.send_command( "SetText", "Text", "Dummy Text" )

            if url.Path == "DropdownButton" or url.Path == "ToggleDropdownButton":
                x.send_command( "CheckItemPos", "Pos", 2 )

        except:
            logging.exception("dispatch")
        finally:
            return

    def removeStatusListener(self, listener, url):
        try:
            logging.debug("removeStatusListener")
        except:
            logging.exception("dispatch")
        finally:
            return


g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(
    SampleDispatch,
    "addons.ExtendingLibreOffice.ComplexToolbar.SampleDispatch",
    ("com.sun.star.frame.XDispatch",), )
