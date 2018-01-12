# A Complex Toolbar Sample
## Structure of the Sample

The sample is based on ToolbarSample, which illustrate how to create a simpmle toolbar with a button, and ProtocolHandler,
which create a dummy protocol that handles a specific url.

* [*Addons.xcu*](Addons.xcu): The file defined a toolbar, with various kind of toolbar controls. Apart from generic options like URL, Title, Target, etc, the most important property here is ControlType, which specifies the type of the UI control. In URL you should use the protocol scheme so that it is handled by the protocol handler you implemented.

* [*WriterWindowsState.xcu*](WriterWindowsState.xcu): This is essential for defining a toolbar, creates the resource for the toolbar.

* [*ProtocolHandler.xcu*](ProtocolHandler.xcu): The file registered "addons.ExtendingLibreOffice.ComplexToolbar.DummyProtocol:\*" protocol scheme, associate the scheme with our protocol handler implementation "addons.ExtendingLibreOffice.ComplexToolbar.SampleHandler".

* [*handler.py*](handler.py): Our protocol handler implementation "addons.ExtendingLibreOffice.ComplexToolbar.SampleHandler", create dispatch object that actually handles the UI control.

* [*dispatch.py*](dispatch.py): Our dispatch object that does the real job. I send various control command to the UI control when addStatusListener is invoked for illustration.

## Control Types

Tye ControlType field I used in Addons.xcu defines the types of the control.

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


## The Dispatch Object
The dispatch object implements the XDispatch interface. According to API document, it serves state information of objects which can be connected to controls. 

> Each state change should to be broadcasted to all registered status listeners. The first notification should be performed synchronously from XDispatch::addStatusListener(). The state consists of enabled/disabled and a short descriptive text of the function (e.g. "undo insert character"). It is to be broadcasted whenever this state changes or the UI control should re-get the value for the URL it is connected to. Additionally, a context-switch-event is to be broadcasted whenever the object may be out of scope, to force the state listener to requery the XDispatch. 

When addStatusListener is invoked, the dispatch object can obtain the instance of the toolbar control, and send control command to the UI control when status changes.

## Send Control Command to Various Contorls

All the complex toolbar button controls implements the com.sun.star.frame.XStatusListener interface. That means
you can invoke it's statusChanged method with a FeaturedStateEvent struct, with following member properties: 

| Struct Member    |  Description                                |
|------------------|---------------------------------------------|
| FeatureURL       | URL of the feature                          |
| FeatureDescriptor| Descriptive text of the function            |
| IsRequery        | Whether dispatch has to be requeried.       |
| IsEnabled        | Whether the control is enabled.             |
| State            | State of the feature in this dispatch       |

Note that complex toolbar controllers act depending on the type of the State
* bool: make the item visible and set it to checked or unchecked.
* string: set item's text and quick help text. 
* ItemStatus: make it visible and set item state.
* Visibility: set visibility state.
* ControlCommand: send control command with a sequence of arguements, such as set text, set values, add entries, etc. to the UI control.



The only control command supported by *ImageButton* is SetImage.

| Supported Command | Arguments            |
|-------------------|----------------------|
| SetImage          | URL=string           |


While *Spinfield* support the commands below to control the behavior of the UI control:

| Supported Command | Arguments            |
|-------------------|----------------------|
| SetValue          | Value=number         |
| SetStep           | Step=number          |
| SetUpperLimit     | UpperLimit=number    |
| SetLowerLimit     | LowerLimit=number    |
| SetOutputFormat   | OutputFormat=string  |
| SetValues         | *All of the above*   |


*Combobox*, *Dropdownbox*, *DropdownButton*, *ToggleDropdownButton* support vairous list manipulation commands:

| Supported Command | Arguments            |
|-------------------|----------------------|
| SetList           | List=[]string        |
| AddEntry          | Text=string |
| InsertEntry       | Text=string<BR/>Pos=number |
| RemoveEntryPos    | Pos=number |
| RemoveEntryText   | Text=string |

Because both *Combobox* and *Editfied* have an editable text field, they support SetText.

| Supported Command | Arguments            |
|-------------------|----------------------|
| SetText           | Text=string


*DropdownButton* and *ToggleDropdownButton* allows you to check individual item by its position.

| Supported Command | Arguments            |
|-------------------|----------------------|
| CheckItemPos      | Pos=number           |


## Receive control event from the contorl
TBD

## Reference
* [Generic UNO Interfaces for complex toolbar controls](http://wiki.openoffice.org/wiki/Framework/Article/Generic*UNO_Interfaces_for_complex_toolbar*controls)
* [XDispatch Interface Reference](https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1frame_1_1XDispatch.html)
* [XStatusListener Interface Reference](https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1frame_1_1XStatusListener.html)
* [FeaturedStateEvent Struct Reference](https://api.libreoffice.org/docs/idl/ref/structcom_1_1sun_1_1star_1_1frame_1_1FeatureStateEvent.html)
* [ControlCommand Struct Reference](https://api.libreoffice.org/docs/idl/ref/structcom_1_1sun_1_1star_1_1frame_1_1ControlCommand.html)
* [XControlNotificatioonlistener Interface Reference](https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1frame_1_1XControlNotificationListener.html)
