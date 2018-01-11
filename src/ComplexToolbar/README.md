# A Complex Toolbar Sample
## Structure of the sample

The sample is based on ToolbarSample, which illustrate how to create a simpmle toolbar with a button, and ProtocolHandler,
which create a dummy protocol that handles a specific url.

* ProtocolHandler.xcu
The file registered "addons.ExtendingLibreOffice.ComplexToolbar.DummyProtocol:\*" protocol scheme, associate the scheme with our protocol handler implementation "addons.ExtendingLibreOffice.ComplexToolbar.SampleHandler".

* Addons.xcu
The file defined a toolbar, with various kind of toolbar controls. Apart from generic options like URL, Title, Target, etc, the most important property here is ControlType, which specifies the type of the control.

* WriterWindowsState.xcu
This is essential for defining a toolbar, as what we did in ToolbarSample.

* handler.py 
Our protocol handler implementation "addons.ExtendingLibreOffice.ComplexToolbar.SampleHandler".

* dispatch.py
Our dispatch object that does the real job.

## Control Types

|ControlType          |Description                                                                      |
|---------------------|---------------------------------------------------------------------------------|
| ImageButton         | A normal toggle button, the width of the button depends on the image.           |
| Combobox            | A normal combo box with edit field inside.                                      |
| Dropdownbox         | A normal drop down box.                                                         |
| Spinfield           | A edit field with two buttons to increase/decrease numerical values.            |
| Editfield           | A normal edit field.                                                            |
| Button              | A simple button without any need for status updates.                            |
| DropdownButton      | A drop-down only button.                                                        |
| ToggleDropdownButton| A toggle button with a drop-down button. Each item can be checked individually. |
| ...                 | Any unlisted above become a "GenericToolbarController"                          |


## The dispatch object
The dispatch object implements the XDispatch interface. According to API document, it serves state information of objects which can be connected to controls. 

> Each state change should to be broadcasted to all registered status listeners. The first notification should be performed synchronously from XDispatch::addStatusListener(). The state consists of enabled/disabled and a short descriptive text of the function (e.g. "undo insert character"). It is to be broadcasted whenever this state changes or the control should re-get the value for the URL it is connected to. Additionally, a context-switch-event is to be broadcasted whenever the object may be out of scope, to force the state listener to requery the XDispatch. 

When addStatusListener is invoked, the dispatch object can obtain the instance of the toolbar control, and send control command to the control when status changes.

## Send control command to various contorls

All the complex toolbar button controls implements the com.sun.star.frame.XStatusListener interface. That means
you can invoke it's statusChanged method with a FeaturedStateEvent struct, with following member properties: 

| Struct Member    |  Description                                |
|------------------|---------------------------------------------|
| FeatureURL       | URL of the feature                          |
| FeatureDescriptor| Descriptive text of the function            |
| IsEnabled        | Whether dispatch has to be requeried.       |
| State            | State of the feature in this dispatch       |

Note that complex toolbar controllers act depending on the type of the State
* bool: make the item visible and set it to checked or unchecked.
* string: set item's text and quick help text. 
* ItemStatus: make it visible and set item state.
* Visibility: set visibility state.
* ControlCommand: send control command with a sequence of arguements, such as set text, set values, add entries, etc. to the control.

Control commands can be cateotriezed according to the type of the control. For example,
* "SetImage" ( URL:string ) : set image url for the ImageButton
* "SetValues" ( Value:long, Step:long, UpperLimit:long, LowerLimit:long ): for Spinfield
* "SetText" ( Text:string ): to set the text label for the control, such as 
Editfield, Combobox, Dropdownbox, Dropdownbutton, ToggleDropdownbox
* "AddEntry" ( Text:string ): for control types with a list, such as Combobox,
Dropdownbox, Dropdownbutton, ToggleDropdownbox
* "SetDropDownLines" ( Lines:long ): to set the number of visible lines of the drop down list
for Combobox and Dropdownbox.

## Receive control event from the contorl

## Reference
* [Generic UNO Interfaces for complex toolbar controls](http://wiki.openoffice.org/wiki/Framework/Article/Generic_UNO_Interfaces_for_complex_toolbar_controls)
* [XDispatch Interface Reference](https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1frame_1_1XDispatch.html)
* [XStatusListener Interface Reference](https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1frame_1_1XStatusListener.html)
* [FeaturedStateEvent Struct Reference](https://api.libreoffice.org/docs/idl/ref/structcom_1_1sun_1_1star_1_1frame_1_1FeatureStateEvent.html#a1545061c08231d50fabef7514f9584d3)
* [ControlCommand Struct Reference](https://api.libreoffice.org/docs/idl/ref/structcom_1_1sun_1_1star_1_1frame_1_1ControlCommand.html)
* [XControlNotificatioonlistener Interface Reference](https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1frame_1_1XControlNotificationListener.html)
