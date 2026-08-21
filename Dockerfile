# set up the container.
FROM python:3.14.6

# set the working dir.
WORKDIR /app

# copy the app dir.
COPY . /app
COPY pyproject.toml uv.lock ./

# install libraries.
RUN pip install --no-cache-dir uv
RUN uv sync --frozen --no-dev

# expose the port.
EXPOSE 8000

# command to run the app using uvicorn.
CMD ["uv", "run", "uvicorn","app.main:app","--host","0.0.0.0","--port","8000"] 