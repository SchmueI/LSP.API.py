
# LSP.API.py

This is an API to access the webserver of the LSP Website. Please use this API carefully as it may come with a lack of quality.
The API is still in an early state of development and is not suiteable for being used as a daily driver. This API was created
for an educational purpose. You may use and edit this code with care.

## General

The following documentation shows how to access the LSP Website using the Python Request module. In order to work with this API
you are requested to use STRINGS for every parameter you send. Dictionaries however have to be defined correctly. Please make
sure you follow the documentation as exact as possible.

## approve.py

approve.py uses the following method appr(< payload >). The Method can be used to prove if a set of username and password
is valid. The Output value is either True or False. Usage is as follows:

    import approve
    approve.appr({"user":USERNAME,"pwd":PASSWORD})

## vplan.py

vplan.py uses the following method get_plan(< payload >, < typus >). Both, PAYLOAD and TYPUS are required for the method to run
The Output value is a HTML formatted String that contains the substituation plan of the School. Usage is as follows:

    import vplan
    vplan.get_plan({"user":USERNAME,"pwd":PASSWORD}, "V")

Typus can be either V to get the entire substitute plan or a german Weekday. For example to fetch the substitution plan for
Monday, you need to call the method like this:

    import vplan
    vplan.get_plan({"user":"USERNAME","pwd":"PASSWORD"}, "Montag")

Use existing USERNAME and PASSWORD values from the LSP Website to get a response.

## iwe.py

This module can be imported like this:

    import iwe

### get_IWE(payload)

This method returns all existing registrations for the IWE that can be found on the LSP Website. Its payload parameter is idetical
to the payload parameter of vplan.py

    import iwe
    iwe.get_IWE({"user":"USERNAME","pwd":"PASSWORD"})

Use existing USERNAME and PASSWORD values from the LSP Website to get a response. The information is given in a HTML codec. It
contains the Full Name, the Grade and the Boarding House (with room number). There might be a verbose option one day that also shows
the comments for the registration if some exist.

### IWE_anmelden(USERNAME, PASSWORD, ATTRIBUTE):

This method will try to register the user to an IWE. You don't transmit the user data within a dictionary this time.

    import iwe
    iwe.IWE_anmelden("USERNAME", "PASSWORD", "ATTRIBUTE")

The Attribute is optional. It cotains any specific information about the registration. For example workshop registrations
or exceptional days and so on. 

The response would be a 1 if the registration was successfull or a 0 if the registration failed.
Please note that a return value of 0 doesnt necessarily mean that the password or username was wrong. A very common reason
is that the registration period for this week was already exceeded or the registration is not yet enabled by the LSP Admin.

### IWE_abmelden(USERNAME, PASSWORD):

This method will try to delete the registration of the user to an IWE. You don't transmit the user data within a dictionary this time.

    import iwe
    iwe.IWE_abmelden("USERNAME", "PASSWORD")

The response would be a 1 if the registration was successfull or a 0 if the registration failed.
Please note that a return value of 0 doesnt necessarily mean that the password or username was wrong. A very common reason
is that the registration period for this week was already exceeded or the registration is not yet enabled by the LSP Admin.

## bus.py

The module can be used to view and change registrations for the school bus. It can be imported like this:

    import bus

### registrations(payload)

This method returns all existing registrations for the Bus that can be found on the LSP Website. Its payload parameter is idetical
to the payload parameter of vplan.py

    import bus
    bus.registrations({"user":"USERNAME","pwd":"PASSWORD"})

Use existing USERNAME and PASSWORD values from the LSP Website to get a response. The information is given in a HTML codec. It
contains all bus registrations with full names and  descriptions.

### register(USERNAME, PASSWORD, TYPE)

This method will try to register the user to a bus line. You don't transmit the user data within a dictionary this time.

    import bus
    bus.register("USERNAME", "PASSWORD", TYPE)

The Type is *not* a string but a *number*. The numbver is referred to one of three cases:

    0: Bus to Naumburg
    1: Bus to Bad Kösen
    2: Bus to Bad Kösen with switch-option to Naumburg

Please note that the response of this method will be either 1 or 0. However 1 does not necessarily mean that a registration
was successful. It only means that the registration was sent. If you attempt to register a bus after the deadline, you will
receive a 1 as a response, because the registration was sent. THere is yet no way to automatically prove if the registration 
was successfull.
The Response will be 0 if the registrations are not yet opened. (On Weekends for example)

### deregister(USERNAME, PASSWORD)

This method will try to delete the registration of the user to a Bus.

    import bus
    bus.deregister("USERNAME", "PASSWORD")

The response will always be 1, even if the operation failed (see register method for more details)
