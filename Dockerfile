FROM python:3.10
ADD aStar.py Configuration.py CornerType.py Node.py Packer.py Plot.py Rectangle.py Test.py /
ADD requirements.txt /
RUN apt-get update && apt-get install -y python3-tk
ENTRYPOINT [ "python3", "./udp_client.py" ]
