# DAB Live! api
A simple Python client to obtain information about your connected pump and enable power shower.

## Installation
Just use `pip` to install this module
```
pip3 install dab-live-api
```
> [!NOTE]
> On Windows you should use `pip` instead of `pip3`


## How to use
Just instantiate the class `DAB`, it supports three optional parameters:
 - `email`: your DAB Live! email
 - `psw`: your DAB Live! password
 - `should_save_token`: a boolean to save token for future sessions (the default one lasts one year) or generate a new one each execution (default `True`).

 If you prefer to set credentials after the class instantiation, just use the `set_credentials` method, in this case it accepts two arguments:
 - `email`
 - `psw`

To get data for each of your installations you can use `request_installation_data`, it accepts an optional parameter, `installation_id`, to obtain data only for a pump.

> [!IMPORTANT]
> Give a look to the [init](dab_live_api/examples/getting_started.py) to better understand how it works