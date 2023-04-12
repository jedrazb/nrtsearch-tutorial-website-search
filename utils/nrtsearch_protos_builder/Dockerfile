FROM amazoncorretto:17

RUN yum -y install git

RUN git clone --depth 1 https://github.com/Yelp/nrtsearch.git /user/nrtsearch

WORKDIR /user/nrtsearch

# This generates all .proto files
RUN ./gradlew clean installDist

# Copy all .proto files to a persistent volume
CMD cp -r /user/nrtsearch/clientlib/src/main/proto/* /user/protos && cp -r /user/nrtsearch/clientlib/build/extracted-include-protos/main/* /user/protos