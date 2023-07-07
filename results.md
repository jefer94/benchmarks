## No encryption

Responses

- Median was 2ms
- Average was 2ms
- Min was 0ms
- Max was 82ms
- About 2823 requests per second

CPU (based in amount of cycles waited)

- Median was 0Hz
- Average was 1Hz
- Min was 0Hz
- Max was 34Hz

RAM

- Median was 11769MB
- Average was 11780MB
- Min was 11002MB
- Max was 12537MB
- Delta was 1534MB
- About 0.544MB per request

SWAP

- Median was 1252MB
- Average was 1252MB
- Min was 1252MB
- Max was 1252MB

## Encryption, internal HMAC-SHA256, external nothing

Responses

- Median was 5ms
- Average was 4ms
- Min was 0ms
- Max was 90ms
- About 2823 requests per second

CPU (based in amount of cycles waited)

- Median was 1Hz
- Average was 1Hz
- Min was 0Hz
- Max was 52Hz

RAM

- Median was 12436MB
- Average was 12397MB
- Min was 10985MB
- Max was 13648MB
- Delta was 2663MB
- About 0.943MB per request

SWAP

- Median was 1252MB
- Average was 1276MB
- Min was 1252MB
- Max was 1426MB

## Encryption, internal HMAC-SHA512, external nothing

Responses

- Median was 5ms
- Average was 4ms
- Min was 0ms
- Max was 90ms
- About 2823 requests per second

CPU (based in amount of cycles waited)

- Median was 1Hz
- Average was 1Hz
- Min was 0Hz
- Max was 33Hz

RAM

- Median was 12190MB
- Average was 12193MB
- Min was 10737MB
- Max was 13712MB
- Delta was 2974MB
- About 1.054MB per request

SWAP

- Median was 1476MB
- Average was 1476MB
- Min was 1476MB
- Max was 1476MB

## Encryption, internal ED25519, external nothing

Responses

- Median was 5ms
- Average was 4ms
- Min was 0ms
- Max was 86ms
- About 2823 requests per second

CPU (based in amount of cycles waited)

- Median was 1Hz
- Average was 2Hz
- Min was 0Hz
- Max was 39Hz

RAM

- Median was 12195MB
- Average was 12213MB
- Min was 10731MB
- Max was 13762MB
- Delta was 3030MB
- About 1.073MB per request

SWAP

- Median was 1498MB
- Average was 1500MB
- Min was 1498MB
- Max was 1565MB

## Encryption, internal JWT ED25519, external nothing

Responses

- Median was 7ms
- Average was 6ms
- Min was 0ms
- Max was 81ms
- About 2823 requests per second

CPU (based in amount of cycles waited)

- Median was 5Hz
- Average was 4Hz
- Min was 0Hz
- Max was 65Hz

RAM

- Median was 12135MB
- Average was 12097MB
- Min was 10576MB
- Max was 13555MB
- Delta was 2979MB
- About 1.055MB per request

SWAP

- Median was 1564MB
- Average was 1563MB
- Min was 1563MB
- Max was 1565MB

## Encryption, JWT ED25519 saved in Postgres Database (external)

Responses

- Median was 10ms
- Average was 11ms
- Min was 1ms
- Max was 108ms
- About 1746 requests per second

CPU (based in amount of cycles waited)

- Median was 8Hz
- Average was 9Hz
- Min was 0Hz
- Max was 77Hz

RAM

- Median was 11835MB
- Average was 11810MB
- Min was 10771MB
- Max was 12779MB
- Delta was 2008MB
- About 1.150MB per request

SWAP

- Median was 1563MB
- Average was 1563MB
- Min was 1563MB
- Max was 1563MB

## Encryption, JWT ED25519 saved in Postgres Database (external)

Responses

- Median was 12ms
- Average was 12ms
- Min was 0ms
- Max was 128ms
- About 1559 requests per second

CPU (based in amount of cycles waited)

- Median was 8Hz
- Average was 9Hz
- Min was 0Hz
- Max was 83Hz

RAM

- Median was 11649MB
- Average was 11674MB
- Min was 10734MB
- Max was 12612MB
- Delta was 1878MB
- About 1.205MB per request

SWAP

- Median was 1563MB
- Average was 1563MB
- Min was 1563MB
- Max was 1563MB

## Encryption, JWT ED25519 saved in Redis Database (external)

Responses

- Median was 5ms
- Average was 4ms
- Min was 0ms
- Max was 87ms
- About 2823 requests per second

CPU (based in amount of cycles waited)

- Median was 1Hz
- Average was 1Hz
- Min was 0Hz
- Max was 40Hz

RAM

- Median was 12145MB
- Average was 12140MB
- Min was 10699MB
- Max was 13657MB
- Delta was 2958MB
- About 1.048MB per request

SWAP

- Median was 1563MB
- Average was 1563MB
- Min was 1563MB
- Max was 1563MB

## Encryption, JWT ED25519 saved in Mongo Database (external)

Responses

- Median was 6ms
- Average was 5ms
- Min was 0ms
- Max was 100ms
- About 2823 requests per second

CPU (based in amount of cycles waited)

- Median was 2Hz
- Average was 2Hz
- Min was 0Hz
- Max was 33Hz

RAM

- Median was 12220MB
- Average was 12273MB
- Min was 10622MB
- Max was 13872MB
- Delta was 3249MB
- About 1.151MB per request

SWAP

- Median was 1563MB
- Average was 1569MB
- Min was 1563MB
- Max was 1705MB

