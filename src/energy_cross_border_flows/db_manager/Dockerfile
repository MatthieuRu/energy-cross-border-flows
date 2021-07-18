FROM python:3.6


WORKDIR src/energy_cross_border_flows/api/db_manager

# copy pip requirements file from build context to directory
COPY requirements.txt requirements.txt

# install python dependencies
RUN pip install -r requirements.txt 

COPY ./ ./

EXPOSE 8000

# run uvicorn server to run API
CMD ["python", "./main.py", "postgres"]
