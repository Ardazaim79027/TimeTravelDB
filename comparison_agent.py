from sqlalchemy import create_engine,text

DATABASE_URL="mysql+pymysql://root:arda123@localhost/timetravel"

engine=create_engine(DATABASE_URL)

class ComparisonAgent:

    def compare_history(self):

        with engine.connect() as conn:

            result=conn.execute(
                text("""
                SELECT
                operation_type,
                COUNT(*) as total
                FROM users_history
                GROUP BY operation_type
                """)
            )

            return result.fetchall()
