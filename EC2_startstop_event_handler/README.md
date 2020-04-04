# EC2_startstop_event_handler

To have automatic owner label on EC2 and RDS resources we utilize Cloudwatch Events, that looks for *RunInstances* (EC2) and *CreateDBInstance* or *CreateDBCluster* (RDS) events and calls *EC2_startstop_event_handler* lambda function.

The lambda function  tries to create an `owner` tag for the resource and the owner's name is read from the event which reflects to the user initiated the event.

## Deployment

First we have to deploy the lambda function in place. Then we can create the event rules that calls the lambda function.

### IAM role for Lambda

On AWS IAM console first we create a policy:
 - Click **Policies** then create a new with **Create Policy** button
 - Click on **JSON** tab to add the policy document from this repo's `AWS_lambda_ExecutionRole.json` file (copy-paste). (Be aware that on the 12th live the log group name should match with the lambda function name!)
 - Click **Review policy**
 - in **Name** field give it a name you will remmeber
 - Optionally a **Description** can be useful
 - If it seems ok, click on **Create policy** button to create it

Then we should create an IAM Role for the lambda, still on the AWS IAM console:
 - Click **Roles** on the left
 - Click **Create role** button
 - Select **AWS service** at the top for *Select type of trusted entity*
 - Select **Lambda** as your use case then click **Next: Permissions**
 - in the list of **Attach permissions policies** choose the policy you created previously (you can find it easier if you filter for "*Customer managed*" policies only) then click button: **Next: Tags**
 - Add any well tought out tags you like and click **Next: Review**
 - Give a descriptive name in the **Role name** field
 - With the button **Create Role** the role will be created.

### Lambda function deployment

On AWS console open the lambda console:
 - **Create function** button
 - Option: **Author from scratch**
 - Function name like `EC2_startstop_event_handler` (this function name will be used later when creating loggroup)
 - Runtime: **Python 3.7**
 - Permissions: **Use an existing role**
 - in the **Existing role** dropdown list choose the role created earlier and click **Create function** button
 - Add the code to the code editor!
 - Add some descriptive tags!
 - in **Basic settings** click **Edit** to change timeout to 10s.
 - And save it with the **Save** button on the top right.

### LogGroup for lambda function

On AWS CLoudwatch console:
 - Open **Logs** -> **Log groups**
 - Click on **Create log group** button
 - in the **Log group name** field put a string like: `/aws/lambda/EC2_RDS_startstop_event_handler`, where
    - it starts with `/aws/lambda/`
    - ends with the name of the lambda function!

### Cloudwatch event rule for EC2

On AWS console open the Cloudwatch console:
 - Choose **Events** -> **Rules** -> **Create rule**
 - in the **Event Source** column choose **Event Pattern**
 - in **Service Name** chooose **EC2**
 - in **Event Type** choose **AWS API Call via CloudTrail**
 - Below this change **Any operation** to **Specific operation(s)**
 - Put `RunInstances` to the field below.
 - In the "Event Pattern Preview" box you should see a json like in this repo's `EC2_startstop_Cloudwatch_EC2event_pattern.json` file
 - Now on the right side choose **Add target** button.
 - You can choose **Lambda function** in the dropdown list.
 - Choose your Lambda function's name created previously
 - You can add other targets too, like a **Cloudwatch log group** to have it logged as well
 - Now click on **Configure details** button on the bottom right
 - Give a good name to the event rule in the **Name** field
 - Finally click **Create rule** button.
  
### Cloudwatch event rule for RDS

On AWS console open the Cloudwatch console:
 - Choose **Events** -> **Rules** -> **Create rule**
 - in the **Event Source** column choose **Event Pattern**
 - in **Service Name** chooose **CloudTrail**
 - in **Event Type** choose **AWS API Call via CloudTrail**
 - Below this change **Any operation** to **Specific operation(s)**
 - Put `CreateDBInstance` to the field below.
 - Click on the **`+`** sign below to have another field
 - Put `CreateDBCluster` to the field
- In the "Event Pattern Preview" box you should see a json like in this repo's `EC2_startstop_Cloudwatch_RDSevent_pattern.json` file. If there is incorrect data, then you can edit the json directly.
 - Now on the right side choose **Add target** button.
 - You can choose **Lambda function** in the dropdown list.
 - Choose your Lambda function's name created previously
 - You can add other targets too, like a **Cloudwatch log group** to have it logged as well
 - Now click on **Configure details** button on the bottom right
 - Give a good name to the event rule in the **Name** field
 - Finally click **Create rule** button.
