import logging
import unohelper
from com.sun.star.frame import ControlCommand
from com.sun.star.beans import NamedValue
from com.sun.star.frame import FeatureStateEvent

from com.sun.star.frame import XDispatch

#logging.basicConfig(filename='/tmp/protocol_handler.txt', level=logging.DEBUG)

# event.State act based on it's type
# Any(bool) -> checked / unchecked
# Any(string) -> SetItemText / SetQuickHelpText
# Any(ItemStatus)
# Any(ItemVisibility) -> toggle visibility
# Any(ControlCommand) -> execute control command

def CreateNamedValue(name, value):
    v = NamedValue()
    v.Name = name
    v.Value = value
    return v

def CreateControlCommand( command, arguments ):
    control_command = ControlCommand()
    control_command.Command = command
    control_command.Arguments = arguments
    return control_command

class FeatureEventWrapper():
    def __init__(self, source, url, enabled, requery ):
        event = FeatureStateEvent()
        event.Source = source
        event.FeatureURL = url
        event.IsEnabled  = enabled
        event.Requery    = requery
        self.event = event

    def get_event(self):
        return self.event

    def set_image(self, image_url):
        logging.debug("set_image image_url="+image_url)
        args  = (CreateNamedValue("URL", image_url), )
        self.event.State = CreateControlCommand( "SetImage", args )
        return self.event

    def set_values(self, value, step, lower, upper):
        a1 = CreateNamedValue( "Value", value)
        a2 = CreateNamedValue( "Step", step)
        a3 = CreateNamedValue( "UpperLimit", upper)
        a4 = CreateNamedValue( "LowerLimit", lower)
        args = (a1, a2, a3, a4, )
        self.event.State = CreateControlCommand( "SetValues", args )
        return self.event

    def set_text(self, text):
        args  = (CreateNamedValue("Text", text), )
        self.event.State = CreateControlCommand( "SetText", args )
        return self.event

    def set_list(self, thelist):
        args  = (CreateNamedValue("List", thelist), )
        self.event.State = CreateControlCommand( "SetList", args )
        logging.debug("set_list thelist="+str(thelist))
        return self.event

    def add_entry(self, text ):
        args  = (CreateNamedValue("Text", text), )
        self.event.State = CreateControlCommand( "AddEntry", args )
        return self.event

    def set_state(self, state ):
        self.event.State = state
        return self.event

def new_event(listener,url):
    return FeatureEventWrapper(listener, url, True, False)

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


    def init_list_x(self, listener, url):
        thelist =  ("Apple","Banana","Orange")
        listener.statusChanged( new_event(self, url).set_list( thelist ) )

    def init_list(self, listener, url):
        listener.statusChanged( new_event(self, url).add_entry( "Apple" ) )
        listener.statusChanged( new_event(self, url).add_entry( "Banana" ) )
        listener.statusChanged( new_event(self, url).add_entry( "Orange" ) )

    def init_text(self, listener, url,text):
        listener.statusChanged( new_event(self, url).set_text(text) )

    def set_values(self, listener, url, value, step, lower, upper):
        listener.statusChanged( new_event(self, url).set_values(value, step, lower, upper) )

    def set_image(self, listener, url, image_url):
        listener.statusChanged( new_event(self, url).set_image(image_url) )

    def addStatusListener(self, listener, url):
        try:
            #show_msg("dispatch", "Hello, there!", self.toolkit, self.frame)
            logging.debug("addStatusListener Path="+url.Path)
            if url.Path == "ImageButton":
                image_url = "vnd.sun.star.extension://addons.ExtendingLibreOffice.ComplexToolbar/star.png"
                self.set_image(listener, url, image_url )
                self.image_button = listener
            if url.Path == "Combobox":
                self.init_list(listener,url)
                self.init_text(listener, url, "Dummy text for combobox")
            if url.Path == "Dropdownbox":
                self.init_list(listener,url)
                self.list_item = listener
            if url.Path == "Spinfield":
                self.set_values(listener, url, 10, 2, 0, 20)
            if url.Path == "Editfield":
                self.init_text(listener, url, "Dummy text for editfield")
            if url.Path == "Dropdownbox":
                self.init_list(listener,url)
            if url.Path == "DropdownButton":
                self.init_list(listener,url)
            if url.Path == "ToggleDropdownButton":
                self.init_list(listener,url)

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
