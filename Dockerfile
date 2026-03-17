# Use the `python:3.7` source image from Amazon ECR Public Gallery
# We are not using Docker Hub slim images to avoid pull rate limits.
FROM public.ecr.aws/sam/build-python3.7:latest

# Set up an app directory for your code
COPY . /app
WORKDIR /app

# Install pip and needed Python packages from requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Define an entrypoint which will run the main app using the Gunicorn WSGI server.
ENTRYPOINT ["gunicorn", "-b", ":8080", "main:APP"]
