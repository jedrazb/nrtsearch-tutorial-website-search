FROM amazoncorretto:17

RUN yum -y install git
RUN yum -y install hostname

RUN git clone --depth 1 https://github.com/Yelp/nrtsearch.git /user/nrtsearch

WORKDIR /user/nrtsearch

COPY . /user/nrtsearch/

RUN ./gradlew clean installDist