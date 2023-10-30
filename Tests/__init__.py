import os

import Tests.SeleniumSetUp as SeleniumSetUp

try:
    web_driver_mode = os.environ["SELENIUM_DRIVER_MODE"]
    match web_driver_mode:
        case "FIREFOX":
            SeleniumSetUp.driver_manager = SeleniumSetUp.FirefoxManager
        case "CHROME":
            raise NotImplementedError("The Chrome driver has not been set up yet. "
                                      "Please be patient or add it yourself in SeleniumSetUp.py.")
        case _:
            raise NotImplementedError("The driver mode '{}' is not recognized. "
                                      "Expected values are 'FIREFOX' and 'CHROME'.")
except KeyError:
    raise EnvironmentError("Environment variable 'SELENIUM_DRIVER_MODE' must be set to run tests.")
