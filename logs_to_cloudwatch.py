import boto3
import time

cloudwatch_logs = boto3.client('logs')
# create a log group if it doesnt exist
log_group_name = 'logs_from_repo_beta'
list_log_groups_response = cloudwatch_logs.list_log_groups(
    logGroupNamePattern=log_group_name
)

foundLogGroups = list_log_groups_response["logGroups"]

if foundLogGroups == 0:
    create_log_group_response = cloudwatch_logs.create_log_group(
        logGroupName=log_group_name
    )

    print(create_log_group_response)
else:
    print("Log group already exists", log_group_name)

# create a log stream if it doesnt exist

log_stream_name = str(time.time())
print("Log stream name", log_stream_name)

create_log_stream_response = cloudwatch_logs.create_log_stream(
    logGroupName=log_group_name,
    logStreamName=log_stream_name
)

# read in log
log_events = [] 
with open('log.txt', 'r') as file:
    # parse the log
    for line in file:
        if len(line.strip()) > 0:
            log_events.append({
                'timestamp': round(time.time() * 1000),
                'message': line.strip()
                })

# create log event for each line in log

if len(log_events) > 0:
    put_log_events_response = cloudwatch_logs.put_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        logEvents=log_events
    )

    print(put_log_events_response)