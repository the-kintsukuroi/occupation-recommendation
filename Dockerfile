FROM python:3

# set a directory for the app
#WORKDIR /usr/src/app

# copy all the files to the container
COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["streamlit", "run"]

CMD ["/srcs/streamlit_app/app.py"]

EXPOSE 8501
