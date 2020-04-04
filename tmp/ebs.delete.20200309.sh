for i in `cat ebs.delete.20200309.txt`
do
  echo $i
  echo aws ec2 create-snapshot --volume-id $i --tag-specifications 'ResourceType="snapshot",Tags=[{Key="snapshot-date", Value="2020.March.09."}]'
done
for i in `cat ebs.delete.20200309.txt`
do
  echo $i
  echo aws ec2 delete-volume --volume-id $i
done
