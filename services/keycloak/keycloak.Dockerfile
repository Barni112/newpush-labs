FROM quay.io/keycloak/keycloak:latest AS builder

ENV KC_DB=postgres
ENV KC_HEALTH_ENABLED=true

WORKDIR /opt/keycloak

RUN /opt/keycloak/bin/kc.sh build

COPY --chown=1000:0 keycloak.conf /opt/keycloak/conf/
COPY --chown=1000:0 newpush_labs_realm.json /opt/keycloak/data/import/


FROM quay.io/keycloak/keycloak:latest

COPY --from=builder /opt/keycloak/ /opt/keycloak/

CMD ["start", "--optimized", "--import-realm"]
