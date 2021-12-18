Downloaded from - https://nsdcindia.org/learning-resources

How it works:
1. The Government of India publishes National Occupational Standards for each Qualification package(Occupation) - download from source
2. Each Qualification Package has details about the minimum requirements - use web scraping and pdf downloader to analyse text(not in this project)
3. We store these requirements in JSON documents in Elasticsearch using Python Client - bulk-ingest.py
4. The user inputs are queried with a full-text query with text analyser in Elasticsearch database - utils.py
5. The queried results are rendered using HTML and served to the user on the Streamlit App - templates.py
6. Streamlit App - srcs/streamlit_app.py
7. Docker and other files to publish and deploy
