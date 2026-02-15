ARG BASE_POSTGRES_IMAGE=postgres:16.12-alpine3.23
FROM golang:1.25.7-alpine AS gosu-builder

ARG GOSU_VERSION=1.17

RUN apk add --no-cache git ca-certificates

WORKDIR /src
RUN git clone --depth 1 --branch "${GOSU_VERSION}" https://github.com/tianon/gosu.git .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -trimpath -ldflags="-s -w" -o /out/gosu .

FROM ${BASE_POSTGRES_IMAGE}

# Replace upstream gosu with a rebuild from Go 1.25.7.
COPY --from=gosu-builder /out/gosu /usr/local/bin/gosu
RUN chmod +x /usr/local/bin/gosu
