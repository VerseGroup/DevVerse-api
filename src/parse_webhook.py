def parse_check_run(json):
    try:
        repo = json['repository']['name']
        sender = json['sender']['login']
        result = json['check_run']['conclusion']
        status = json['check_run']['status']
        output = json['check_run']['output']['title']
    except:
        return None

    if status != 'completed':
        return None

    message = f"Your code (by {sender}) check for {repo} has result: \'{result}\'!\n\n Output: {output}"