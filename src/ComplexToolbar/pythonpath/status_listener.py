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
    def __init__(self, url, enabled, requery ):
        event = FeatureStateEvent()
        event.FeatureURL = url
        event.IsEnabled  = enabled
        event.Requery    = requery
        self.event = event

    def set_command(self, command, argname, argvalue):
        args  = (CreateNamedValue(argname, argvalue), )
        self.event.State = CreateControlCommand( command, args )
        return self.event

    def set_command_with_args(self, command, args):
        arglist = []
        for name, value in args.items():
            arglist.append( CreateNamedValue( name, value ) )
        self.event.State = CreateControlCommand( command, tuple(arglist) )
        return self.event

    def set_state(self, state ):
        self.event.State = state
        return self.event



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

