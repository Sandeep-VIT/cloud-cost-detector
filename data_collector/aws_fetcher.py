import boto3
import datetime
import pandas as pd

def get_ec2_cpu_utilization(instance_id, days=7):
    """Get CPU usage for an EC2 instance over the past N days."""
    cw = boto3.client('cloudwatch', region_name='us-east-1')
    end = datetime.datetime.utcnow()
    start = end - datetime.timedelta(days=days)

    response = cw.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
        StartTime=start, EndTime=end,
        Period=3600,  # hourly data
        Statistics=['Average']
    )
    points = response['Datapoints']
    df = pd.DataFrame(points)[['Timestamp', 'Average']]
    df = df.sort_values('Timestamp').reset_index(drop=True)
    return df
