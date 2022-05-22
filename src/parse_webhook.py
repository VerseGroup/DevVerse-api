def parse_check_run(json):

    try:
        repo = json['repository']['name']
        sender = json['sender']['login']
        result = json['check_run']['conclusion']
        status = json['check_run']['status']
        output = json['check_run']['output']['title']
        time = json['check_run']['completed_at']
        url = json['check_run']['url']
    except Exception as e:
        return f"Error {str(e)}"

    if status != 'completed':
        return None

    message = f"Your code (by {sender}) check for {repo} has result: \'{result}\'!\n\nOutput: {output}\n\nURL: {url}\n\ntimestamp: {time}"

    return message

def parse_push(json):
    try:
        repo = json['repository']['name']
        sender = json['sender']['login']
        commit_message = json['head_commit']['message']
        commit_url = json['head_commit']['url']
        commit_time = json['head_commit']['timestamp']
    except Exception as e:
        return None

    message = f"Your code (by {sender}) has been pushed to {repo}!\n\nCommit: {commit_message}\n\n More information: {commit_url}\n\nTime: {commit_time}"

    return message

def parse_issue(json):
    try:
        repo = json['repository']['name']
        sender = json['sender']['login']
        issue_title = json['issue']['title']
        issue_url = json['issue']['url']
        issue_time = json['issue']['created_at']

        assignees = []
        for assignee in json['issue']['assignees']:
            assignees.append(assignee['login'])
    except Exception as e:
        return None

    message = f"An issue has been posted (by {sender}) has been assigned to {assignees} in {repo}!\n\nIssue: {issue_title}\n\n More information: {issue_url}\n\nTime: {issue_time}"

        

