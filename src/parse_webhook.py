def parse_check_run(json):

    try:
        repo = json['repository']['name']
        sender = json['sender']['login']
        result = json['check_run']['conclusion']
        status = json['check_run']['status']
        output = json['check_run']['output']['title']
        time = json['check_run']['completed_at']
        url = json['check_run']['html_url']
    except Exception as e:
        return None

    if status != 'completed':
        return None

    message = f"Your code (by {sender}) check for {repo} has result: \'{result}\'!\n\nOutput: {output}\n\ntimestamp: {time}"

    return message

def parse_push(json):
    try:
        repo = json['repository']['name']
        sender = json['sender']['login']
        commit_message = json['head_commit']['message']
        commit_url = json['head_commit']['html_url']
        commit_time = json['head_commit']['timestamp']
    except Exception as e:
        return str(e)

    message = f"Your code (by {sender}) has been pushed to {repo}!\n\nCommit: {commit_message}\n\n More information: {commit_url} \n\n Time: {commit_time}"

    return message