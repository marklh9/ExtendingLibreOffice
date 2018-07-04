import uno
import unohelper
from com.sun.star.task import XJob


class DummyJob(unohelper.Base, XJob):
    def __init__(self, ctx):
        self.ctx = ctx

    def execute(self, args):
        desktop = self.ctx.ServiceManager.createInstanceWithContext(
            "com.sun.star.frame.Desktop", self.ctx)

        doc = desktop.getCurrentComponent()

        o_current_controller = doc.getCurrentController()
        o_view_cursor = o_current_controller.getViewCursor()
        o_view_cursor.setString("Lorem ipsum dolor sit amet, consectetur adipiscing.")
        return ()

g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(
    DummyJob,
    "addons.ExtendingLibreOffice.Job1.DummyJob",
    ("com.sun.star.task.Job",),)

