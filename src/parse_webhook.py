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

def parse_push(json):
    try:
        repo = json['repository']['name']
        sender = json['sender']['login']
        commit_message = json['head_commit']['message']
        commit_url = json['head_commit']['url']
    except:
        return None

    message = f"Your code (by {sender}) has been pushed to {repo}!\n\n Commit: {commit_message}\n\n {commit_url}"
