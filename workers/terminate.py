import datetime
from flumine.events.events import TerminationEvent

# worker to stop the flumine instance after the day's races have finished
def terminate(
    context: dict, flumine, today_only: bool = True, seconds_closed: int = 600
) -> None:
    """terminate framework if no markets
    live today.
    """
    markets = list(flumine.markets.markets.values())
    markets_today = [
        m
        for m in markets
        if m.market_start_datetime.date() == datetime.datetime.utcnow().date()
        and (
            m.elapsed_seconds_closed is None
            or (m.elapsed_seconds_closed and m.elapsed_seconds_closed < seconds_closed)
        )
    ]
    if today_only:
        market_count = len(markets_today)
    else:
        market_count = len(markets)
    if market_count == 0:
        flumine.handler_queue.put(TerminationEvent(flumine))