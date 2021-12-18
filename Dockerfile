FROM python:3

# copy all the files to the container
COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./srcs /srcs

ENTRYPOINT ["streamlit", "run"]

CMD ["/srcs/streamlit_app/app.py"]

EXPOSE 8501