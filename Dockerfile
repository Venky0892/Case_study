FROM python:3.7 AS build

# virtualenv
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# add and install requirements
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

#################
# RUNTIME IMAGE #
#################
FROM python:3.7 AS runtime

# setup user and group ids
ARG USER_ID=1000
ENV USER_ID $USER_ID
ARG GROUP_ID=1000
ENV GROUP_ID $GROUP_ID

# add non-root user and give permissions to workdir
RUN groupadd --gid $GROUP_ID user && \
          adduser user --ingroup user --gecos '' --disabled-password --uid $USER_ID && \
          mkdir -p /app && \
          chown -R user:user /app

# copy from build image
COPY --chown=user:user --from=build /opt/venv /opt/venv

# set working directory
WORKDIR /Case_study

# switch to non-root user
USER user

# disables lag in stdout/stderr output
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
# Path
ENV PATH="/opt/venv/bin:$PATH"

COPY . /Case_study

# Run streamlit

CMD streamlit run stream.py