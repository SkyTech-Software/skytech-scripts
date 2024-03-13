## SoftwareSkyTech Scripts

### Description

REST API service for hosting small scripts, connected directly with [SoftwareSkytech](https://skytechsoftware.pl/) page.


### Available scripts

- IMEI Checker - Checks whether the provided IMEI number of the device is not blocked by the following 4 network operators in Poland.

- Mailer - A small service allowing to send emails from our OVH mailbox.

- Crawler - Script for obtaining font types from .apk files using Google Store.

### How to set up service

1. Clone repo `git clone <url>`.
2. Create .env file.

```
API_KEY=
SMTP_SERVER=
SMTP_PORT=
MAILER_USERNAME=
MAILER_PASSWORD=
```
3. Build docker image and run container `docker compose -f docker-compose-dev.yml up --build` (--build flag only at the first run).
4. Run swagger `http://localhost:8020/scripts/api/docs`
5. Happy coding!

### Plans:

- unit tests,
- add unit tests + pre-commit into ci/cd.
