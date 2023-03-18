# lambda-digit-recognition

Serverless digit recognition with lambda and a tensorflow model.

# commands used for creating and deploying a lambda function from a docker image

docker build -t hello-world-v5 .

## testing the container locally

docker run -p 9000:8080 -e AWS_ACCESS_KEY_ID="accesskey" -e AWS_SECRET_ACCESS_KEY="secret_access_key" -e AWS_REGION="eu-central-1" container_image_name

curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d "{}"
- dont forget double quotes at the end if you are on windows

## deploying the lambda function

For this we first need to put our docker container to aws ecr. To do this we first create repository in ecr.
Now we want to push our local container to ecr. In the repository in ecr we create there is a button "Push-Befehle". To use them we need to have installed aws cli. Then we can open cmd:

aws configure
* logging into aws with an access key

aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin [your_account_number].dkr.ecr.eu-central-1.amazonaws.com

After this we can tag our container and push it to ecr.

docker tag digit-recognition-with-lambda [your_account_number].dkr.ecr.eu-central-1.amazonaws.com/aws-lambda-tensorflow:digit-recognition-with-lambda

docker push [your_account_number].dkr.ecr.eu-central-1.amazonaws.com/aws-lambda-tensorflow:digit-recognition-with-lambda

If we done this successfully, we can open aws lambda and create a new lambda function.
We choose create from container image and then use our new container.

## using the lambda function in application

lambda_client = boto3.client('lambda')
response = lambda_client.invoke(FunctionName='digit-ocr-v1', Payload = json.dumps(payload))

response = s3.get_object(Bucket="sudoku-solver-bucket", Key="images/Digit_Img_1.png")