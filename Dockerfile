FROM nikolaik/python-nodejs

RUN apt-get update && apt-get install -y
RUN echo $extra_metadata

# copy over all files to the container
COPY . .

# run chmod to entrypoint.sh
RUN chmod +x entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]