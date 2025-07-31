# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container
COPY . .

# Add PostgreSQL official repository and install PostgreSQL Client 16.4 and other dependencies
RUN apt-get update && apt-get install -y wget gnupg2 lsb-release && \
    echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list && \
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - && \
    apt-get update && apt-get install -y \
    libpq-dev gcc python3-dev iputils-ping postgresql-client-16

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Prisma client generate
RUN python -m prisma generate

ENV PYTHONPATH=src

#EXPOSE 5001 eski hali
EXPOSE 3005

CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "3005"]
