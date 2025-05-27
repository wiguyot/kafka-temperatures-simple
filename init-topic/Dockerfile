FROM bitnami/kafka:latest

COPY create-topic.sh /create-topic.sh

USER root
RUN chmod +x /create-topic.sh
USER 1001

CMD ["/create-topic.sh"]
