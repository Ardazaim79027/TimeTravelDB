from sqlalchemy import create_engine, text

DATABASE_URL="mysql+pymysql://root:arda123@localhost/timetravel"

engine=create_engine(DATABASE_URL)


class QueryAgent:

    def process_query(self,question):

        with engine.connect() as conn:

            result=conn.execute(
                text("""
                SELECT *
                FROM users_history
                WHERE
                new_name LIKE :search
                OR old_name LIKE :search
                OR operation_type LIKE :search
                """),
                {
                    "search":f"%{question}%"
                }
            )

            return result.fetchall()
