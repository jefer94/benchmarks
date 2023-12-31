# Benchmark
Short `len(rand_obj) == 3`, Medium `len(rand_obj) == 10` and Big `len(rand_obj) == 30`

Running short benchmark (500 iterations)
```txt
    Database        Algoritm Technologie Implementation  Result(s)  Delta(s)       %  Requests/s
0       None            None     Nothing         Native   0.000205  0.000000     100     2444419
10     Cache     HMAC SHA512         JWT         Native   0.000511  0.000306     250      978846
9      Cache     HMAC SHA256         JWT         Native   0.000522  0.000317     255      958084
2       None     HMAC SHA256         JWT          PyJWT   0.013017  0.012812    6364       38413
3       None     HMAC SHA512         JWT          PyJWT   0.013739  0.013534    6717       36393
11      None     HMAC SHA256   Signature         Native   0.021325  0.021121   10426       23446
12      None     HMAC SHA512   Signature         Native   0.022224  0.022019   10865       22499
4      Redis     HMAC SHA256         JWT          PyJWT   0.026073  0.025868   12746       19177
1       None  ED25519 SHA512         JWT          PyJWT   0.110295  0.110090   53921        4533
8   Postgres     HMAC SHA512         JWT          PyJWT   0.395306  0.395101  193259        1265
7   Postgres     HMAC SHA256         JWT          PyJWT   0.399611  0.399407  195363        1251
5    MongoDB     HMAC SHA256         JWT          PyJWT   1.283839  1.283634  627648         389
6    MongoDB     HMAC SHA512         JWT          PyJWT   1.321760  1.321555  646187         378
```

Running medium benchmark (500 iterations)
```txt
    Database        Algoritm Technologie Implementation  Result(s)  Delta(s)       %  Requests/s
0       None            None     Nothing         Native   0.000344  0.000000     100     1453106
9      Cache     HMAC SHA256         JWT         Native   0.000637  0.000293     185      784945
10     Cache     HMAC SHA512         JWT         Native   0.000717  0.000373     208      697559
2       None     HMAC SHA256         JWT          PyJWT   0.013256  0.012912    3852       37719
3       None     HMAC SHA512         JWT          PyJWT   0.014135  0.013791    4108       35374
4      Redis     HMAC SHA256         JWT          PyJWT   0.035951  0.035607   10448       13908
12      None     HMAC SHA512   Signature         Native   0.053244  0.052900   15474        9391
11      None     HMAC SHA256   Signature         Native   0.057570  0.057226   16731        8685
1       None  ED25519 SHA512         JWT          PyJWT   0.110278  0.109934   32049        4534
8   Postgres     HMAC SHA512         JWT          PyJWT   0.397573  0.397229  115543        1258
7   Postgres     HMAC SHA256         JWT          PyJWT   0.401849  0.401505  116786        1244
5    MongoDB     HMAC SHA256         JWT          PyJWT   1.278553  1.278208  371574         391
6    MongoDB     HMAC SHA512         JWT          PyJWT   1.315114  1.314770  382200         380
```

Running big benchmark (500 iterations)
```txt
    Database        Algoritm Technologie Implementation  Result(s)  Delta(s)       %  Requests/s
0       None            None     Nothing         Native   0.000683  0.000000     100      732259
9      Cache     HMAC SHA256         JWT         Native   0.000971  0.000289     142      514676
10     Cache     HMAC SHA512         JWT         Native   0.001019  0.000336     149      490792
2       None     HMAC SHA256         JWT          PyJWT   0.013897  0.013214    2035       35978
3       None     HMAC SHA512         JWT          PyJWT   0.014562  0.013879    2133       34336
4      Redis     HMAC SHA256         JWT          PyJWT   0.027942  0.027260    4092       17894
1       None  ED25519 SHA512         JWT          PyJWT   0.109966  0.109283   16105        4547
11      None     HMAC SHA256   Signature         Native   0.138190  0.137507   20238        3618
12      None     HMAC SHA512   Signature         Native   0.153261  0.152578   22445        3262
7   Postgres     HMAC SHA256         JWT          PyJWT   0.388380  0.387697   56879        1287
8   Postgres     HMAC SHA512         JWT          PyJWT   0.391496  0.390814   57335        1277
6    MongoDB     HMAC SHA512         JWT          PyJWT   1.306637  1.305954  191359         383
5    MongoDB     HMAC SHA256         JWT          PyJWT   1.341285  1.340602  196434         373
```


## No encryption

Responses

- Median was 3ms
- Average was 5ms
- Min was 0ms
- Max was 66ms
- About 3768 requests per second

CPU (based in amount of cycles waited)

- Median was 0Hz
- Average was 0Hz
- Min was 0Hz
- Max was 34Hz

RAM

- Median was 5775MB
- Average was 5697MB
- Min was 4660MB
- Max was 6446MB
- Delta was 1785MB
- About 0.474MB per request

SWAP

- Median was 0MB
- Average was 0MB
- Min was 0MB
- Max was 0MB

## Encryption, internal HMAC-SHA256, external nothing

Responses

- Median was 5ms
- Average was 5ms
- Min was 0ms
- Max was 79ms
- About 3319 requests per second

CPU (based in amount of cycles waited)

- Median was 0Hz
- Average was 1Hz
- Min was 0Hz
- Max was 54Hz

RAM

- Median was 6390MB
- Average was 6369MB
- Min was 4682MB
- Max was 7749MB
- Delta was 3067MB
- About 0.924MB per request

SWAP

- Median was 0MB
- Average was 0MB
- Min was 0MB
- Max was 0MB

## Encryption, internal HMAC-SHA512, external nothing

Responses

- Median was 5ms
- Average was 5ms
- Min was 0ms
- Max was 66ms
- About 3319 requests per second

CPU (based in amount of cycles waited)

- Median was 0Hz
- Average was 1Hz
- Min was 0Hz
- Max was 61Hz

RAM

- Median was 6403MB
- Average was 6375MB
- Min was 4701MB
- Max was 7775MB
- Delta was 3073MB
- About 0.926MB per request

SWAP

- Median was 0MB
- Average was 0MB
- Min was 0MB
- Max was 0MB

## Encryption, internal ED25519, external nothing

Responses

- Median was 5ms
- Average was 5ms
- Min was 0ms
- Max was 80ms
- About 3324 requests per second

CPU (based in amount of cycles waited)

- Median was 0Hz
- Average was 1Hz
- Min was 0Hz
- Max was 56Hz

RAM

- Median was 6432MB
- Average was 6416MB
- Min was 4697MB
- Max was 7768MB
- Delta was 3071MB
- About 0.924MB per request

SWAP

- Median was 0MB
- Average was 0MB
- Min was 0MB
- Max was 0MB

## Encryption, internal JWT ED25519, external nothing

Responses

- Median was 5ms
- Average was 5ms
- Min was 0ms
- Max was 81ms
- About 3316 requests per second

CPU (based in amount of cycles waited)

- Median was 0Hz
- Average was 1Hz
- Min was 0Hz
- Max was 48Hz

RAM

- Median was 6420MB
- Average was 6405MB
- Min was 4711MB
- Max was 7685MB
- Delta was 2974MB
- About 0.897MB per request

SWAP

- Median was 0MB
- Average was 0MB
- Min was 0MB
- Max was 0MB

## Encryption, JWT ED25519 saved in Postgres Database

Responses

- Median was 3ms
- Average was 6ms
- Min was 0ms
- Max was 104ms
- About 2856 requests per second

CPU (based in amount of cycles waited)

- Median was 3Hz
- Average was 4Hz
- Min was 0Hz
- Max was 65Hz

RAM

- Median was 5397MB
- Average was 5578MB
- Min was 4724MB
- Max was 7069MB
- Delta was 2345MB
- About 0.821MB per request

SWAP

- Median was 0MB
- Average was 0MB
- Min was 0MB
- Max was 0MB

## Encryption, JWT ED25519 saved in Postgres Database (external)

Responses

- Median was 3ms
- Average was 7ms
- Min was 0ms
- Max was 132ms
- About 2639 requests per second

CPU (based in amount of cycles waited)

- Median was 3Hz
- Average was 4Hz
- Min was 0Hz
- Max was 66Hz

RAM

- Median was 5289MB
- Average was 5478MB
- Min was 4734MB
- Max was 6872MB
- Delta was 2137MB
- About 0.810MB per request

SWAP

- Median was 0MB
- Average was 0MB
- Min was 0MB
- Max was 0MB

## Encryption, JWT ED25519 saved in Redis Database

Responses

- Median was 5ms
- Average was 5ms
- Min was 0ms
- Max was 90ms
- About 3304 requests per second

CPU (based in amount of cycles waited)

- Median was 0Hz
- Average was 1Hz
- Min was 0Hz
- Max was 39Hz

RAM

- Median was 6276MB
- Average was 6295MB
- Min was 4663MB
- Max was 7687MB
- Delta was 3024MB
- About 0.915MB per request

SWAP

- Median was 0MB
- Average was 0MB
- Min was 0MB
- Max was 0MB

## Encryption, JWT ED25519 saved in Mongo Database

Responses

- Median was 5ms
- Average was 5ms
- Min was 0ms
- Max was 101ms
- About 3521 requests per second

CPU (based in amount of cycles waited)

- Median was 1Hz
- Average was 1Hz
- Min was 0Hz
- Max was 32Hz

RAM

- Median was 6299MB
- Average was 6361MB
- Min was 4700MB
- Max was 8243MB
- Delta was 3542MB
- About 1.006MB per request

SWAP

- Median was 0MB
- Average was 0MB
- Min was 0MB
- Max was 0MB

