import logging

from tabulate import tabulate

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def pytest_runtest_logreport(report):
    log_records = []
    for record in logging.getLogger().records:
        log_records.append([record.asctime, record.levelname, record.message])

    # Display log records as a table in the test report
    table = tabulate(log_records, headers=["Timestamp", "Level", "Message"], tablefmt="pipe")
    report.node.repinfo.append(table)
