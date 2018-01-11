import logging
import unohelper
import uno

from com.sun.star.frame import XDispatch
from feature_event import new_event

#logging.basicConfig(filename='/tmp/complex_toolbar.txt', level=logging.DEBUG)

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


    def init_list(self, listener, url):
        # Force typing to prevent it from becoming sequence of Any objects.
        thelist = uno.Any( "[]string", ("Apple","Banana","Orange") )
        listener.statusChanged( new_event(self, url).set_list( thelist ) )

        listener.statusChanged( new_event(self, url).add_entry( "She" ) )
        listener.statusChanged( new_event(self, url).add_entry( "Sell" ) )
        listener.statusChanged( new_event(self, url).add_entry( "Seashell" ) )
        listener.statusChanged( new_event(self, url).add_entry( "Seashore" ) )

        listener.statusChanged( new_event(self, url).set_dropdown_lines( 3 ) )

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
