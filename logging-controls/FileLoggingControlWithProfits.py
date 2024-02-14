import os
import csv
import logging
from flumine.controls.loggingcontrols import LoggingControl

logger = logging.getLogger(__name__)

class FileLoggingControlWithProfits(LoggingControl):
    NAME = "FILE_LOGGING_CONTROL"
    FIELDNAMES = [
        "order_id",
        "bet_id",
        "customer_order_ref",
        "strategy_name",
        "date_time_created",
        "date_time_placed",
        "elapsed_seconds_executable",
        "market_id",
        "selection_id",
        "handicap",
        "trade_id",
        "side",
        "order_type",
        "price",
        "liability",
        "size",
        "persistence_type",
        "time_in_force",
        "min_fill_size",
        "bet_target_type",
        "bet_target_size",
        "average_price_matched",
        "size_matched",
        'size_remaining',
        'size_cancelled',
        'size_lapsed',
        'size_voided',
        'profit',
        "runner_status",
        "market_notes",
        "trade_notes",
        "order_notes",
        "trade_status",
        "trade_status_log",
        "order_status",
        "order_status_log",
        "violation_msg",
    ]

    def __init__(self, *args, **kwargs):
        self.orders_file = kwargs.pop("orders_file")
        self.markets_file = kwargs.pop("markets_file", None)
        self.append_to_logs = kwargs.pop("append_to_logs", False)
        super(FileLoggingControlWithProfits, self).__init__(*args, **kwargs)
        self._setup()

    def _setup(self):
        # create directory tree to contain log file
        os.makedirs("/".join(self.orders_file.split("/")[:-1]), exist_ok=True)

        if not os.path.exists(self.orders_file) or not self.append_to_logs:
            # create log file with headers (will overwrite any existing file with same name)
            with open(self.orders_file, "w") as m:
                csv_writer = csv.DictWriter(m, delimiter=",", fieldnames=self.FIELDNAMES)
                csv_writer.writeheader()

        if self.markets_file:
            os.makedirs("/".join(self.markets_file.split("/")[:-1]), exist_ok=True)
            if not os.path.exists(self.markets_file) or not self.append_to_logs:
                with open(self.markets_file, "w") as m:
                    csv_writer = csv.DictWriter(m, delimiter=",", fieldnames=["market_id", "bet_count", "profit", "commission"])
                    csv_writer.writeheader()

    def _process_cleared_orders_meta(self, event):
        orders = event.event
        if len(orders) > 0:
            with open(self.orders_file, "a") as m:
                for order in orders:
                    try:
                        order_data = self._prepare_order(order)
                        csv_writer = csv.DictWriter(m, delimiter=",", fieldnames=self.FIELDNAMES)
                        csv_writer.writerow(order_data)
                    except Exception as e:
                        logger.error(
                            "_process_cleared_orders_meta: %s" % e,
                            extra={"order": order, "error": e},
                        )

            logger.info("Orders updated", extra={"order_count": len(orders)})

    def _process_cleared_markets(self, event):
        cleared_markets = event.event
        for cleared_market in cleared_markets.orders:
            logger.info(
                "Cleared market",
                extra={
                    "market_id": cleared_market.market_id,
                    "bet_count": cleared_market.bet_count,
                    "profit": cleared_market.profit,
                    "commission": cleared_market.commission,
                },
            )
            if self.markets_file:
                with open(self.markets_file, "a") as m:
                    csv_writer = csv.DictWriter(m, delimiter=",", fieldnames=["market_id", "bet_count", "profit", "commission"])
                    csv_writer.writerow({
                        "market_id": cleared_market.market_id,
                        "bet_count": cleared_market.bet_count,
                        "profit": cleared_market.profit,
                        "commission": cleared_market.commission,
                    })

    def _prepare_order(self, order):
        return {
            "order_id": order.id,
            "bet_id": order.bet_id,
            "customer_order_ref": order.customer_order_ref,
            "strategy_name": str(order.trade.strategy),
            "date_time_created": str(order.date_time_created),
            "date_time_placed": str(order.responses.date_time_placed),
            "elapsed_seconds_executable": order.elapsed_seconds_executable,
            "market_id": order.market_id,
            "selection_id": order.selection_id,
            "handicap": order.handicap,
            "trade_id": order.trade.id,
            "side": order.side,
            "order_type": order.order_type.ORDER_TYPE.value,
            "price": order.order_type.price if hasattr(order.order_type, "price") else None,
            "liability": order.order_type.liability if hasattr(order.order_type, "liability") else None,
            "size": order.order_type.size if hasattr(order.order_type, "size") else None,
            "persistence_type": order.order_type.persistence_type if hasattr(order.order_type, "persistence_type") else None,
            "time_in_force": order.order_type.time_in_force if hasattr(order.order_type, "time_in_force") else None,
            "min_fill_size": order.order_type.min_fill_size if hasattr(order.order_type, "min_fill_size") else None,
            "bet_target_type": order.order_type.bet_target_type if hasattr(order.order_type, "bet_target_type") else None,
            "bet_target_size": order.order_type.bet_target_size if hasattr(order.order_type, "bet_target_size") else None,
            "average_price_matched": order.average_price_matched,
            "size_matched": order.size_matched,
            'size_remaining': order.size_remaining,
            'size_cancelled': order.size_cancelled,
            'size_lapsed': order.size_lapsed,
            'size_voided': order.size_voided,
            'profit': order.profit,
            "runner_status": order.runner_status,
            "market_notes": order.trade.market_notes,
            "trade_notes": order.trade.notes_str,
            "order_notes": order.notes_str,
            "trade_status": order.trade.status.value if order.trade.status else None,
            "trade_status_log": ",".join([s.value for s in order.trade.status_log]),
            "order_status": order.status.value if order.status else None,
            "order_status_log": ",".join([s.value for s in order.status_log]),
            "violation_msg": order.violation_msg,
        }
