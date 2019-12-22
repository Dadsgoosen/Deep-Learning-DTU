def is_request(request: dict) -> bool:
    return is_correct_message(request) and request['type'] == 'request'


def is_result(request: dict) -> bool:
    return is_correct_message(request) and request['type'] == 'result'


def is_correct_message(request: dict) -> bool:
    return 'type' in request
