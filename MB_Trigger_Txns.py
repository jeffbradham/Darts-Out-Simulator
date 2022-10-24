import re


class result_t:
    PASS = 0
    FAIL = 1
    UNKOWN = 2


class error_t:
    NONE = 0
    REBOOT = 1
    INCOMPLETE = 2


class msg_t:
    OUT = 0
    IN = 1
    UNKNOWN = 2


class message:
    def __init__(self):
        self.URI: str = ''
        self.msg_type: msg_t = msg_t.UNKNOWN
        self.id = 0
        self.token: str = ''
        self.status: str = ''
        self.code: str = ''
        self.type: str = ''
        self.stop_time = 0

    def print_me(self):
        print(
            f"Message, {self.id}, {self.URI}, {self.msg_type}, {self.status},{self.code}")


class transaction:
    def __init__(self):
        self.id = 0
        self.URI: str = ''
        self.type: msg_t = msg_t.UNKNOWN
        self.start_time = 0
        self.stop_time = 0
        self.duration = 0
        self.msg = message
        self.ack = message
        self.error = False
        self.messages: message = []

    def print_me(self):
        print(
            f"Transaction, {self.id}, {self.URI}, {self.type}, {self.start_time}, {self.stop_time}")


class report:
    def __init__(self):
        self.reason = 0
        self.timestamp = 0
        self.result: result_t = result_t()
        self.error: error_t = error_t()
        self.start_time = 0
        self.stop_time = 0
        self.duration = 0
        self.transactions: transaction = {}

    def print_me(self):
        print(f"Report, {self.reason}, {self.start_time}, {self.stop_time}")

    def get_txn(self, id):
        if id in self.transactions.keys():
            return self.transactions[id]
        else:
            txn = transaction()
            txn.id = id
            self.transactions[id] = txn
            return txn


# globals
line_num = 0
report_re = re.compile(
    "\[(\S+\s\S+)\]\s.*reporting reason update value =\s+(\d+)")
start_msg_re = re.compile(
    "\[(\S+\s\S+)\]\s.*\[COAP\]:\s======== (Incoming|Outgoing) CoAP package.*")
stop_msg_re = re.compile(
    "\[(\S+\s\S+)\]\s.*\[COAP\]:\s======== End of CoAP package")

uri_re = re.compile(".*\[COAP\]: Uri-Path:\s+(\S+)")
status_re = re.compile(".*\[COAP\]: Status:\s+(\w+)")
code_re = re.compile(".*\[COAP\]: Code:\s+(\w+)")
type_re = re.compile(".*\[COAP\]: Type:\s+(\w+)")
id_re = re.compile(".*\[COAP\]: Id:\s+(\d+)")
token_re = re.compile(".*\[COAP\]: Token:\s+(\S+)")


# The idea is that parsing magic happens in the individual methods
# while bookkeeping and business logic happen in the main parse loop
def capture_report(report: report, line: str):
    global line_num
    match = report_re.search(line)
    report.start_time = match.group(1)
    report.reason = match.group(2)
    line_num += 1


def end_report(report: report):
    report.duration = report.stop_time = report.stop_time


def capture_msg(msg: message, lines):
    global line_num
    end = False

    # sometimes there are double prints of this header so just skip it
    if start_msg_re.match(lines[line_num + 1]):
        line_num += 1

    while (not end):
        line_num += 1
        if uri_re.match(lines[line_num]):
            match = uri_re.search(lines[line_num])
            msg.URI = match.group(1)
        elif status_re.match(lines[line_num]):
            match = status_re.search(lines[line_num])
            msg.status = match.group(1)
        elif code_re.match(lines[line_num]):
            match = code_re.search(lines[line_num])
            msg.code = match.group(1)
        elif type_re.match(lines[line_num]):
            match = type_re.search(lines[line_num])
            msg.type = match.group(1)
        elif id_re.match(lines[line_num]):
            match = id_re.search(lines[line_num])
            msg.id = match.group(1)
        elif token_re.match(lines[line_num]):
            match = token_re.search(lines[line_num])
            msg.token = match.group(1)
        elif stop_msg_re.match(lines[line_num]):
            match = stop_msg_re.search(lines[line_num])
            msg.stop_time = match.group(1)
            line_num += 1
            end = True
            # sometimes there are double prints of this header so just skip it
            if stop_msg_re.match(lines[line_num]):
                line_num += 1
        elif start_msg_re.match(lines[line_num]):
            txn.error = True
            end = True


def capture_txn(report: report, lines):
    global line_num
    msg = message()

    match = start_msg_re.search(lines[line_num])
    # this is the start of an inbound txn
    if match.group(2) == "Incoming":
        msg.msg_type = msg_t.IN
    # this is the start of an outbound txn
    elif match.group(2) == "Outgoing":
        msg.msg_type = msg_t.OUT

    # parse the next message
    capture_msg(msg, lines)

    txn = report.get_txn(msg.id)

    # only use the first message as a start_time
    if txn.start_time == 0:
        txn.type = msg.msg_type
        txn.URI = msg.URI
        txn.start_time = match.group(1)

    # keep over-writing stop_time to get the last one
    txn.stop_time = msg.stop_time
    report.stop_time = msg.stop_time
    txn.messages.append(msg)


def parse(log: str):
    global line_num
    reports: report = []
    this_report = report()
    report_cnt = 0
    last_txn_end_line_num = 0

    print(f"Hello World {log}\n")

    with open(log, "r") as file:
        lines = file.readlines()

        line_cnt = len(lines)
        while line_num < line_cnt:
            line = lines[line_num]

            if report_re.match(line):
                # everytime after the first wrap up report details before processing the next
                if report_cnt > 0:
                    # end_report(this_report)
                    reports.append(this_report)
                    this_report = report()

                capture_report(this_report, line)
                report_cnt += 1

            # a transaction is beginning, jump into methods and parse your way through the msg and the ack before returning here
            elif start_msg_re.match(line):
                capture_txn(this_report, lines)
                last_txn_end_line_num = line_num
            # since the capture_txn method is supposed to consume the transaction beginning to end, this should not be found in the main loop
            elif stop_msg_re.match(line):
                msg = message()
                line_num = last_txn_end_line_num
                capture_msg(msg, lines)
                if msg.id != 0:
                    txn = this_report.get_txn(msg.id)
                    txn.messages.append(msg)

            else:
                line_num += 1
            # -- End of While Loop
        # capture the last report too
        reports.append(this_report)

    for rep in reports:
        rep.print_me()
        for txn_id in rep.transactions:
            txn: transaction = rep.transactions[txn_id]
            txn.print_me()
            for msg in txn.messages:
                msg.print_me()


if __name__ == '__main__':

    parse("test_log.txt")

# Loop Through File


# -- start_transaction
# if Outgoing||InComing CoAP package
# -- && IN_REPORT && IN_TXN
# -- end_transaction
# ELSE -- Don't Know Yet


# Report
#    -- report_index
#    -- reporting_reason
#    -- timestamp
#    -- Pass/Fail
#    -- Error Type
#    -- start timestamp
#    -- stop timestamp
#    -- total time
#    Transaction
#      -- txn_index
#      -- URI
#      -- ToServer / FromServer
#      -- start timestamp
#      -- stop timestamp
#      -- total time
#      Msg
#      -- msg_index
#      -- ID
#      -- Token
#      -- Status
#      -- Code
#      -- Type
#      Ack
#      -- ack_index
#      -- ID
#      -- Token
#      -- Status
#      -- Code
#      -- Type
