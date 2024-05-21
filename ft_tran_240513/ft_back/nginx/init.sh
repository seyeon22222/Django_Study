#!/bin/sh

#req: OpenSSL 명령어 중 하나로, X.509 인증서 요청 및 생성에 사용됩니다.
#-newkey rsa:4096: 새로운 RSA 개인 키를 4096 비트로 생성합니다.
#-days 30: 생성된 인증서의 유효 기간을 30일로 지정합니다.
#-nodes: 생성된 개인 키를 암호화하지 않습니다.
#-x509: X.509 인증서를 생성합니다.

openssl req -newkey rsa:4096 -days 30 -nodes -x509 \
    -subj "/C=KR/ST=Seoul/L=Seoul/O=42Seoul/OU=gam/CN=test.42.fr" \
    -keyout "/etc/ssl/test.42.fr.key" \
    -out "/etc/ssl/test.42.fr.pem" 2>/dev/null

echo "\
--------------------

@nginx ready
@port:443

--------------------"

exec nginx -g 'daemon off;'
