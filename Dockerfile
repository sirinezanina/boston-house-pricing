FROM python:3.11

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r /code/requirements.txt

COPY ./boston-house-pricing /code/boston-house-pricing

EXPOSE 8000

CMD ["uvicorn", "boston-house-pricing.app:app", "--host", "0.0.0.0", "--port", "8000"]