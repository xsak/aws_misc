# aws_misc
Miscellaneous scripts to query your AWS account

## aws-check-rds-tags
Python script to check if all the needed tags are present on RDS instances. This scans all regions.

## EC2_startstop_event_handler
A lambda to tag EC2 and RDS resources on creation with `owner: {username}` tag. Check its [README.md](./EC2_startstop_event_handler/README.md) file for details!
