import boto3
import csv

field_names = ['Instance_ID', 'Instance Type', 'Region', 'Instance State', 'Instance Name', 'Instance Owner Tag']


def get_name_tag(tag_list):
    if tag_list is None:
        return ""
    else:
        for u in tag_list:
            if u.get('Key', '').lower() == 'name':
                return u.get('Value', '')
        return ""


def get_owner_tag(tag_list):
    if tag_list is None:
        return ""
    else:
        for u in tag_list:
            if u.get('Key', '').lower() == 'owner':
                return u.get('Value', '')
        return ""


def get_all_ec2_instances_csv():
    client = boto3.client('ec2', region_name='eu-central-1')
    ec2_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    with open('output.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([item for item in field_names])
        for region in ec2_regions:
            print(f"DEBUG: processing region: {region}")
            conn = boto3.resource('ec2', region_name=region)
            instances = conn.instances.filter()
            for instance in instances:
                print(f"DEBUG: instance_id: {instance.id}")
                name_tag = get_name_tag(instance.tags)
                owner_tag = get_owner_tag(instance.tags)
                csv_writer.writerow(
                    [
                        instance.id,
                        instance.instance_type,
                        region,
                        instance.state['Name'],
                        name_tag,
                        owner_tag
                    ])
                # print('___________________________')


if __name__ == "__main__":
    get_all_ec2_instances_csv()
