import boto3
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--instance",
        dest="instance",
        help="EC2 instance id"
    )
    parser.add_argument(
        "-r", "--region",
        dest="region",
        help="Region of the instance"
    )
    parser.add_argument(
        "-v", "--verbose",
        dest="verbose",
        help="Verbose mode",
        default=False,
        action='store_true'
    )
    options = parser.parse_args()
    return options


def get_instance_tags(instance_id, region):
    ec2_resource = boto3.resource('ec2', region_name=region)
    try:
        instance = ec2_resource.Instance(instance_id)
    except Exception as e:
        print(f" *** Error getting tags for {instance_id}!")
        raise e
    else:
        return instance.tags


def tag_an_ec2(instance_id, region, is_verbose):
    conn = boto3.client('ec2', region_name=region)
    print(f" * Please give the following informations for instance {instance_id} in region {region}!")
    value_name  = input("Name of the instance: ")
    value_owner = input("Name of the owner: ")
    value_unit  = input("Value of unit: ")
    value_email = input("Email address: ")
    print(f"\nCurrent tags for instance {instance_id}:")
    print(str(get_instance_tags(instance_id, region)))
    while True:
        if input("Do You Want To Continue? [yes/no] ") == "yes":
            break
    print('\n * Tagging instance...')
    try:
        response = conn.create_tags(
            Resources=[instance_id],
            Tags=[
                {'Key': 'Name',  'Value': value_name},
                {'Key': 'owner', 'Value': value_owner},
                {'Key': 'unit',  'Value': value_unit},
                {'Key': 'email', 'Value': value_email}
            ]
        )
    except Exception as e:
        print(" *** Error during tagging!")
        print(e)
    else:
        print(" *** Tagging seems to be ok.")
        if is_verbose:
            print(f"Response:\n{response}")
            print(f"Current Tags:\n {get_instance_tags(instance_id,region)}")


if __name__ == "__main__":
    options = get_arguments()
    if options.instance == None:
        options.instance = input("Instance ID: ")
    if options.region == None:
        options.region = input("Region of the instance: ")
    print(f"verbose: {options.verbose}")
    tag_an_ec2(options.instance, options.region, options.verbose)
