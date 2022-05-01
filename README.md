# aws_iam_global

- This is the global **iam stack** for an aws account
- it contains all the iam roles, policies, user definitions etc. that are being used for any project on the account
- therefore there is no particular stack in each project setting the iam rules for a project


## 1. Check the version of the template

* to update the stack
* make sure the templates being part of the stack are updated on the s3 URLs

* sync the bucket `!Sub ${Project}-TemplatesBucket-Name` **to the local current directory**

```shell
$ aws s3 sync . s3://443723655583-weatherdata-templates/
```



## 2. Parameter Stack

```shell
aws cloudformation create-stack \
--profile encprodadmin \
--stack-name parameter-stack \
--template-body file://global_parameter.yaml
```

- here the stack-update command (CLI)

```shell
aws cloudformation update-stack \
--profile encprodadmin \
--stack-name parameter-stack \
--template-body file://global_parameter.yaml
```



## 3. S3 Stack

```shell
aws cloudformation create-stack \
--profile encprodadmin \
--stack-name s3-stack \
--template-body file://global_s3.yaml \
--capabilities CAPABILITY_IAM
```

- here the stack-update command (CLI)

```shell
aws cloudformation update-stack \
--profile encprodadmin \
--stack-name s3-stack \
--template-body file://global_s3.yaml \
--capabilities CAPABILITY_IAM
```

- if the stack cannot be deleted due to an NON-empy bucket  you can empty a bucket completely like this:

```shell
$ aws s3 rm s3://bucket-name --recursive
# like
$ aws s3 rm s3://300746241447-asa-templatescfn --recursive
```

- Then delete the Bucket

```
$ aws cloudformation delete-stack --stack-name mys3stack
```

## 4. SNS Stack (cause there are a lot of SNS topic used everywhere)

```shell
aws cloudformation create-stack \
--profile default \
--stack-name sns-stack \
--template-body file://global_sns.yaml
```

```shell
aws cloudformation update-stack \
--profile default \
--stack-name sns-stack \
--template-body file://global_sns.yaml
```



## 5. IAM Masterstack

- contains the following stacks:
  - Master Stack
  - Policy Stack
  - Role Stack
  - User Groups Stack
  - Instance Profiles Stack

- make sure the templates being part of the stack are uploaded on the s3 URLs
- sync the bucket `${AWS::AccountId}-${Project}-templates`to the local current directory

```shell
cd aws (directory which holds the iam directory)
```

```shell
aws s3 cp \
--profile default \
--recursive iam s3://300746241447-asa-templatescfn
```

- then

```shell
$ cd iam (directory which holds the masterstack and the nested stacks)
```

- now create/ update the stack

```shell
aws cloudformation create-stack \
--profile default \
--stack-name iam-stack \
--template-body file://iam_masterstack.yaml \
--capabilities CAPABILITY_NAMED_IAM
```

- here the stack-update command (CLI)

```shell
aws cloudformation update-stack \
--profile default \
--stack-name iam-stack \
--template-body file://iam_masterstack.yaml \
--capabilities CAPABILITY_NAMED_IAM
```


## 5.1 Admin User Stack

-  This template will create IAM admin users, along with groups and policies

```shell
aws cloudformation create-stack \
--profile default \
--stack-name adminuser-stack \
--template-body file://admin_users_stack.yaml \
--capabilities CAPABILITY_NAMED_IAM
```

- here the stack-update command (CLI)

```shell
aws cloudformation update-stack \
--profile default \
--stack-name adminuser-stack \
--template-body file://admin_users_stack.yaml
--capabilities CAPABILITY_NAMED_IAM
```

## 6. KMS Stack

```shell
aws cloudformation create-stack \
--profile encprodadmin \
--stack-name kms-stack \
--template-body file://global_kms.yaml
```

- here the stack-update command (CLI)

```shell
aws cloudformation update-stack \
--profile encprodadmin \
--stack-name kms-stack \
--template-body file://global_kms.yaml
```



## 7. Secret Stack

```shell
aws cloudformation create-stack \
--profile encprodadmin \
--stack-name secrets-stack \
--template-body file://global_secrets.yaml
```

```shell
aws cloudformation update-stack \
--profile encprodadmin \
--stack-name secrets-stack \
--template-body file://global_secrets.yaml
```

## 8. Lambda Layer Stack

- creates the Layers used by all Lambdas

- **create deployment packages**

```shell
zip -r dp-layer.zip .
```

- upload  **deployment.zip** file to s3 bucket

```shell
aws s3 cp dp-layer.zip  \
--profile encprodadmin \
s3://443723655583-asa-lambdalayers/layers/dp-layer.zip
```

- then create the lambda stack

```shell
aws cloudformation create-stack \
--profile encprodadmin \
--stack-name LambdaLayer-stack \
--template-body file://global_lambda_layer.yaml
```

```shell
aws cloudformation update-stack \
--profile encprodadmin \
--stack-name LambdaLayer-stack \
--template-body file://global_lambda_layer.yaml
```