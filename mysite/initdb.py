import psycopg

# 데이터베이스 연결 정보
dbname = "mydatabase"
user = "mydatabaseuser"
password = "mypassword"
host = "127.0.0.1"
port = "5432"

# 데이터베이스에 연결
with psycopg.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host,
    port=port
) as conn:

    # 커서 생성
    with conn.cursor() as cur:

        # SQL 쿼리 실행
        cur.execute("SELECT * FROM my_table")

        # 결과 가져오기
        rows = cur.fetchall()
        for row in rows:
            print(row)
