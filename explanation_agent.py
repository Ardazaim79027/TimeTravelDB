from sqlalchemy import create_engine, text

DATABASE_URL="mysql+pymysql://root:arda123@localhost/timetravel"

engine=create_engine(DATABASE_URL)

class ExplanationAgent:

    def explain_changes(self):

        with engine.connect() as conn:

            result=conn.execute(
                text("""
                SELECT operation_type
                FROM users_history
                """)
            )

            rows=result.fetchall()

            explanation=""

            for row in rows:

                if row[0]=="INSERT":
                    explanation += "A user was added. "

                elif row[0]=="UPDATE":
                    explanation += "A user record was modified. "

                elif row[0]=="DELETE":
                    explanation += "A user was deleted. "

            return explanation
