# To push another image:
# > docker build -t maxholloway/dydx-alerts:?.?.? .
# > docker push maxholloway/dydx-alerts:?.?.?

FROM python:3.10.2

# Install python dependencies
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run the program
COPY dydx_alerts/ dydx_alerts/
COPY run run
COPY run-forever run-forever
RUN touch /messenger_blobs.json /api_credentials.json # a hack to ensure that these are provided as files, not directories when passing a volume to the docker image
ENTRYPOINT ["python3", "dydx_alerts/run_forever.py"]