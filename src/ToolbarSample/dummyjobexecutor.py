import uno
import unohelper
from com.sun.star.task import XJobExecutor


class DummyJobExecutor(unohelper.Base, XJobExecutor):
    def __init__(self, ctx):
        self.ctx = ctx

    def trigger(self, args):
        desktop = self.ctx.ServiceManager.createInstanceWithContext(
            "com.sun.star.frame.Desktop", self.ctx)

        doc = desktop.getCurrentComponent()

        o_current_controller = doc.getCurrentController()
        o_view_cursor = o_current_controller.getViewCursor()
        o_view_cursor.setString("Lorem ipsum dolor sit amet, consectetur adipiscing.")

g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(
    DummyJobExecutor,
    "addons.ExtendingLibreOffice.ToolbarSample.DummyJobExecutor",
    ("com.sun.star.task.JobExecutor",),)

