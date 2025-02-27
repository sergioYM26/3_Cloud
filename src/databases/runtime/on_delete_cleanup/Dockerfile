FROM public.ecr.aws/lambda/python:3.13

# Copy the application code
COPY handler.py ${LAMBDA_TASK_ROOT}
COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip install -r requirements.txt

# Command to run the Lambda function
CMD ["handler.handler"]