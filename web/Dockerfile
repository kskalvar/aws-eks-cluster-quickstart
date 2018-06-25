FROM python:2.7
WORKDIR /code
ADD files/requirements.txt /code
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ADD files/app.py /code
CMD python app.py
