# DAB Live! client
A simple Python client to obtain information about your connected pump and enable power shower.

## How to use
Just instantiate the class `DAB`, it supports three optional parameters:
 - `email`: your DAB Live! email
 - `psw`: your DAB Live! password
 - `should_save_token`: a boolean to save token for future sessions (the default one lasts one year) or generate a new one each execution (default `True`).

 If you prefer to set credentials after the class instantiation, just use the `set_credentials` method, in this case it accepts two arguments:
 - `email`
 - `psw`

To get data for each of your installations you can use `request_installation_data`, it accepts an optional parameter, `installation_id`, to obtain data only for a pump.

Give a look to the [init](dab-live-api/examples/getting_started.py) to better understand how it works