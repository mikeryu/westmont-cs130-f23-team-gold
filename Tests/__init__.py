import os

import Tests.SeleniumSetUp as SeleniumSetUp

# Based on the value of the environment variable SELENIUM_DRIVER_MODE,
# the variable Tests.SeleniumSetUp.driver_manager will be set to a different
# web driver that is browser specific.
try:
    web_driver_mode = os.environ["SELENIUM_DRIVER_MODE"]
    match web_driver_mode:
        case "FIREFOX":
            SeleniumSetUp.driver_manager = SeleniumSetUp.FirefoxManager
        case "CHROME":
            SeleniumSetUp.driver_manager = SeleniumSetUp.ChromeManager
        case _:
            raise NotImplementedError("The driver mode '{}' is not recognized. "
                                      "Expected values are 'FIREFOX' and 'CHROME'.")
except KeyError:
    raise EnvironmentError("Environment variable 'SELENIUM_DRIVER_MODE' must be set to run tests.")
