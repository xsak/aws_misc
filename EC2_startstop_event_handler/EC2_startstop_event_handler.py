import json
import boto3


def has_owner_tag(instance_tags):
    """
    Returns True if instance_tags contains 'owner' tag, otherwise returns False.
    Parameter: instance_tags = list of tags with Key, Value pairs.
    """
    if instance_tags is not None:
        for u in instance_tags:
            if u.get('Key', '') == 'owner' or u.get('key', '') == 'owner':
                return True
        return False


def tag_ec2_instance(instande_id, username, region):
    """
    Tags EC2 instance with 'owner' = {username} tag.
    Parameters:
        - instance_id: EC2 instance id to tag,
        - username: Username to put in 'owner' tag,
        - region: region of the EC2 instance.
    """
    try:
        conn = boto3.client('ec2', region_name=region)
        tag_call_response = conn.create_tags(
            Resources=[instande_id],
            Tags=[
            {
                'Key': 'owner',
                'Value': username
            }
            ]
        )
    except Exception as e:
        print("DEBUG: Error during tagging!\n")
        print(e)
        raise e
    else:
        print("DEBUG: Tagging owner seems to be ok.\n")
        print(tag_call_response)


def tag_rds_resource(resource_arn, username, region):
    """
    Tags RDS cluster with 'owner' = {username} tag.
    Parameters:
        - resource_arn: RDS resource arns to tag,
        - username: Username to put in 'owner' tag,
        - region: region of the RDS cluster.
    """
    try:
        conn = boto3.client('rds', region_name=region)
        tag_call_response = conn.add_tags_to_resource(
            ResourceName=resource_arn,
            Tags=[
                {
                    'Key': 'owner',
                    'Value': username
                }
            ]
        )
    except Exception as e:
        print("DEBUG: Error during tagging!\n")
        print(e)
        raise e
    else:
        print("DEBUG: Tagging owner seems to be ok.\n")
        print(tag_call_response)


def resource_tagging_on_runinstances(event):
    #Narrowing focus of event data:
    ec2_instance_item = event['detail']['responseElements']['instancesSet']['items'][0]
    # Instance id from the event:
    ec2_instance_id = ec2_instance_item['instanceId']
    # Username who starts the EC2 instance:
    user_starting_ec2 = event['detail']['userIdentity']['userName']
    # Check if instance has tags at all:
    if 'tagSet' in ec2_instance_item:
        # if it has tags, get them:
        ec2_instance_tags = ec2_instance_item['tagSet']['items']
    else:
        # if no tags, have an empty list:
        ec2_instance_tags = []
    ec2_instance_region = event['region']
    print(f"DEBUG: instanceid: {ec2_instance_id} started by {user_starting_ec2}")
    print(f'DEBUG: tagz: {ec2_instance_tags}')
    # 
    if not has_owner_tag(ec2_instance_tags):
        print(f"DEBUG: No owner tag. Trying to tag it...")
        try:
            tag_ec2_instance(ec2_instance_id, user_starting_ec2, ec2_instance_region)
            return_status_code = 200
            return_message = f'Instance {ec2_instance_id} (region:{ec2_instance_region}) gets tagged with owner={user_starting_ec2}.'
        except Exception as err:
            print(f"Problem during tagging!\n")
            print(err)
            return_status_code = 400
            return_message = 'Tagging failed for the EC2 instance'
    else:
        print("DEBUG: There is an owner tag.")
        return_status_code = 200
        return_message = 'There was already an owner tag for the instance.'
    # Returning values:
    return {
        'statusCode': return_status_code,
        'body': json.dumps(return_message)
    }


def resource_tagging_on_createrdsinstances(event):
    rds_resource_arn = []
    respElements = event['detail']['responseElements']
    for arn_type in ['dBClusterArn', 'dBInstanceArn']:
        if arn_type in respElements:
            rds_resource_arn.append(respElements[arn_type])
    user_creating_rds = event['detail']['userIdentity']['userName']
    rds_cluster_region = event['region']
    print(f"DEBUG: RDS resource identifier: {rds_resource_arn} (region: {rds_cluster_region}) created by: {user_creating_rds}")
    if 'tags' in event['detail']['requestParameters']:
        rds_cluster_tags = event['detail']['requestParameters']['tags']
    else:
        rds_cluster_tags = []
    if not has_owner_tag(rds_cluster_tags):
        print(f"DEBUG: No owner tag. Trying to tag it...")
        try:
            for resource1 in rds_resource_arn:
                print(f"DEBUG: Tagging resource: {resource1}...")
                tag_rds_resource(resource1, user_creating_rds, rds_cluster_region)
            return_status_code = 200
            return_message = f"RDS Resources: {str(rds_resource_arn)} (region: {rds_cluster_region}) gets tagged with owner={user_creating_rds}."
        except Exception as err:
            print("Problem during tagging!\n")
            print(err)
            return_status_code = 400
            return_message = 'Tagging failed for the RDS cluster'
    else:
        print("DEBUG: There is an owner tag.")
        return_status_code = 200
        return_message = "There was already an owner tag of the RDS cluster."
    # Returning values:
    return {
        'statusCode': return_status_code,
        'body': json.dumps(return_message)
    }


def lambda_handler(event, context):
    # Default response:
    response = {
        'statusCode': 200,
        'body': json.dumps("No matching event to handle.")
    }

    # EC2 creation event:
    if event['detail']['eventName'] == 'RunInstances':
        response = resource_tagging_on_runinstances(event)
    
    # RDS creation event:
    if event['detail']['eventName'] in ['CreateDBInstance', 'CreateDBCluster']:
        response = resource_tagging_on_createrdsinstances(event)
    
    # Returning response:
    print(f"DEBUG: response: {json.dumps(response)}")
    return response
