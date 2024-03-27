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

## Disclaimer
All trademarks and copyright-written content found on this project belong to their respective owners. The team is in no way affiliated with DAB or DConnect.
This project displays trademarks and copy-written content such as company and products names. These different trademarks and copy-written content do not belong to us and are properties of their respective owners. This project is in no way affiliated with said companies or trademarks.
This custom integration is an unofficial integration born to read consumptions and enable power shower without arming DAB servers.
> [!IMPORTANT]
> This code is provided 'as is' and the author bears no responsibility for its misuse or any harm caused by its use.
