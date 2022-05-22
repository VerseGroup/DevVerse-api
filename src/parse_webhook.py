def parse_check_run(json):

    return "reached"

    try:
        repo = json['repository']['name']
        sender = json['sender']['login']
        result = json['check_run']['conclusion']
        status = json['check_run']['status']
        output = json['check_run']['output']['title']
    except Exception as e:
        return str(e)

    if status != 'completed':
        return "not completed"

    message = f"Your code (by {sender}) check for {repo} has result: \'{result}\'!\n\n Output: {output}"

    return message

def parse_push(json):
    try:
        repo = json['repository']['name']
        sender = json['sender']['login']
        commit_message = json['head_commit']['message']
        commit_url = json['head_commit']['url']
        commit_time = json['head_commit']['timestamp']
    except Exception as e:
        return str(e)

    message = f"Your code (by {sender}) has been pushed to {repo}!\n\n Commit: {commit_message}\n\n More information: {commit_url} \n\n Time: {commit_time}"

    return message