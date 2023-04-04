FROM python:latest
COPY main.py .
RUN pip3 install beautifulsoup4 requests kavenegar --upgrade
ENTRYPOINT [ "python3" ]
CMD ["main.py"] 