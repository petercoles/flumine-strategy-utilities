# Flumine Strategy Utilities

A collection of utilities whose objective is to aid and DRY the development of Flumine strategies. Each utility is designed to be stand-alone, re-usable and easily integrated into a Flumine strategy or the code used to run that strategy, replacing pieces of code that are often used across multiple Flumine instances.

## Process Logging

It's in the very nature of streaming to produce huge numbers of events. Flumine being event-driven, amplifies this. When something goes wrong, we look to our process log files to find the issue and some clue as to its cause. The process logger (not to be confused with logging controls) can be initialised using the cunningly-named ```initialise_process_logger``` function.

It has a number of options. You can:

* set the *level* at which logging messages will be actioned (default CRITICAL)
* *stream* log entries to the console / terminal (default False)
* persist log entries to a *logfile* (default None)
* just in case you want to use multiple loggers, assign a *name* to the logger being initialised (default None)

Example usage:

``` python
from fsu.process_logger import initialise_logger

logger = initialise_logger(
    level=logging.DEBUG,
    stream=True,
    logfile="path/to/logfile",
    name="myLogger"
)

# log something important
logger.info("Yay, it's working")
```

## Logging Control

Flumine's logging control features are very useful for plugging into key stages of a strategy's execution as it processes markets. The logging control offered by this package, allow the capture of data at a market or individual order level. A particular useful use case is when simulating either backtesting over historical data, or capturing the results of paper trading in real-time.

This example is simular to the one in the Flumine repository's examples, but more extensive in the data that it collects. It also creates the logging control files if they exist. Note that by default it will overwrite the files if they already exist. This by design, so add version numbers or include a timestamp in the control filenames if you want to repeat the runs with different inputs or use the append flag explained below.

The control is designed primarily to capture order data, so the path to an orders log file is mandatory. Optional paramters are a path to a markets log file for the profit / loss per market and a boolean flag to indicate whether you wish to append to an existing log file of the same name. This is especially important when runninig 

Example Usage:

``` python
from fsu.logging-controls.FileLoggingControlWithProfits import FileLoggingControlWithProfits

framework.add_logging_control(
    FileLoggingControlWithProfits(
        orders_file="path/to-orders-log-file" # mandatory
        markets_file="path/to/markets-log-file" # optional
        append_to_logs=True # optional
    )
)
```
