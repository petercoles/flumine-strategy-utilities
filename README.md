# Flumine Strategy Utilities

A collection of utilities whose objective is to aid and DRY the development of Flumine strategies. Each utility is designed to be stand-alone, re-usable and easily integrated into a Flumine strategy or the code used to run that strategy, replacing pieces of code that are often used across multiple Flumine instances.

## Logging

It's in the very nature of streaming to produce huge numbers of events. Flumine being event-driven, amplifies this. When something goes wrong, we look to our process log files to find the issue and some clue as to its cause. The process logger (not to be confused with logging controls) can be initialised using the cunningly-named ```initialise_process_logger``` function.

It has a number of options. You can:

* set the *level* at which logging messages will be actioned (default CRITICAL)
* *stream* log entries to the console / terminal (default False)
* persist log entries to a *logfile* (default None)
* just in case you want to use multiple loggers, assign a *name* to the logger being initialised (default None)

Example usage:

``` python
from fsu.process_logger import initialise_logger

logger = initialise_logger(level=logging.DEBUG, stream=True, logfile="path/to/logfile", name="myLogger")

logger.info("Yay, it's working")
```
