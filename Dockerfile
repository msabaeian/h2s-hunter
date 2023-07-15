# TODO update dockerfile to use poetry
# TODO fix two COPY
FROM python:latest
RUN pip3 install beautifulsoup4 requests kavenegar python-dotenv --upgrade
COPY main.py .
COPY .env .
ENTRYPOINT [ "python3" ]
CMD ["main.py"]
