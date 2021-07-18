FROM python:3.6

WORKDIR src/energy_cross_border_flows/app

# copy pip requirements file from build context to directory
COPY requirements.txt /app/requirements.txt

# install python dependencies
RUN pip install -r /app/requirements.txt 

COPY app.py app/app.py
COPY config.yml ./config.yml

EXPOSE 8050

CMD ["python", "./app/app.py", "db_manager"]

