import logging
import unohelper
import uno

from com.sun.star.frame import XDispatch
from feature_event import FeatureEventWrapper

#logging.basicConfig(filename='/tmp/complex_toolbar.txt', level=logging.DEBUG)

class StatusListenerWrapper():
    def __init__(self, listener, url):
        self.listener = listener
        self.url = url

    def send_command(self, command, name, value):
        event = FeatureEventWrapper( self.url, True, False )
        self.listener.statusChanged( event.set_command( command, name, value ) )
        return self

    def send_command_with_args(self, command, args):
        event = FeatureEventWrapper( self.url, True, False )
        self.listener.statusChanged( event.set_command_with_args( command, args ) )
        return self

    def change_state(self, state):
        event = FeatureEventWrapper( self.url, True, False )
        self.listener.statusChanged( event.set_state( command, state) )
        return self

def init_list(x):
    # Force typing to prevent it from becoming sequence of Any objects.
    thelist = uno.Any( "[]string", ("Apple","Banana","Orange") )
    x.send_command( "SetList", "List", thelist )
    x.send_command( "AddEntry", "Text", "She" )
    x.send_command( "AddEntry", "Text", "Sell" )
    x.send_command( "AddEntry", "Text", "Seashell" )
    x.send_command( "AddEntry", "Text", "Seashore" )
    x.send_command( "SetDropDownLines", "Lines", 3 )

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
            #show_msg("dispatch", "Hello, there!", self.toolkit, self.frame)
            logging.debug("dispatch url.Path="+url.Path)
            if url.Path == "ImageButton" and self.image_button is not None:
                image_url = "vnd.sun.star.extension://addons.ExtendingLibreOffice.ComplexToolbar/star.png"
                self.set_image(self.image_button, url, image_url )
        except:
            logging.exception("dispatch")
        finally:
            return


    def init_text(self, listener, url,text):
        x = StatusListenerWrapper( listener, url )
        x.send_command( "SetText", "Text", text )

    def set_values(self, listener, url, value, step, lower, upper):
        args = { "Value" : value, "Step" : step, "LowerLimit": lower, "UpperLimit" : upper }
        x = StatusListenerWrapper( listener, url )
        x.send_command_with_args( "SetValues", args )

    def set_image(self, listener, url, image_url):
        x = StatusListenerWrapper( listener, url )

    def addStatusListener(self, listener, url):
        try:
            x = StatusListenerWrapper( listener, url )
            #show_msg("dispatch", "Hello, there!", self.toolkit, self.frame)
            logging.debug("addStatusListener Path="+url.Path)
            if url.Path == "ImageButton":
                image_url = "vnd.sun.star.extension://addons.ExtendingLibreOffice.ComplexToolbar/star.png"
                self.set_image(listener, url, image_url )
                self.image_button = listener
            if url.Path == "Combobox":
                init_list(x)
                self.init_text(listener, url, "Dummy text for combobox")
            if url.Path == "Dropdownbox":
                init_list(x)
                self.list_item = listener
            if url.Path == "Spinfield":
                self.set_values(listener, url, 10, 2, 0, 20)
            if url.Path == "Editfield":
                self.init_text(listener, url, "Dummy text for editfield")
            if url.Path == "Dropdownbox":
                init_list(x)
            if url.Path == "DropdownButton":
                init_list(x)
            if url.Path == "ToggleDropdownButton":
                init_list(x)

        except:
            logging.exception("dispatch")
        finally:
            return

    def removeStatusListener(self, listener, url):
        try:
            #show_msg("dispatch", "Hello, there!", self.toolkit, self.frame)
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
