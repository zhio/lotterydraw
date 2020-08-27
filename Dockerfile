FROM python:3.7
RUN pip install fastapi uvicorn
EXPOSE 80
COPY ./app /app
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /app/requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

