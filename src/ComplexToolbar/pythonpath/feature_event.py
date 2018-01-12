from com.sun.star.frame import ControlCommand
from com.sun.star.beans import NamedValue
from com.sun.star.frame import FeatureStateEvent


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
        # The listener acts based on type of the event.State
        # Any(bool) -> make visible and checked / unchecked
        # Any(string) -> SetItemText / SetQuickHelpText
        # Any(ItemStatus)
        # Any(ItemVisibility) -> toggle visibility
        # Any(ControlCommand) -> execute control command


    def get_event(self):
        return self.event

    def set_image(self, image_url):
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
        return self.event

    def add_entry(self, text ):
        args  = (CreateNamedValue("Text", text), )
        self.event.State = CreateControlCommand( "AddEntry", args )
        return self.event

    def set_dropdown_lines(self, lines ):
        args  = (CreateNamedValue("Lines", lines), )
        self.event.State = CreateControlCommand( "SetDropDownLines", args )
        return self.event

    def set_state(self, state ):
        self.event.State = state
        return self.event

def new_event(listener,url):
    return FeatureEventWrapper(listener, url, True, False)

