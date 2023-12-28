FROM python

RUN mkdir -p /home/forex

COPY . /home/forex

WORKDIR /home/forex

RUN pip install telethon

RUN python3 -m pip --version

# RUN npm install canvas

CMD [ "python3", "listen.py" ]