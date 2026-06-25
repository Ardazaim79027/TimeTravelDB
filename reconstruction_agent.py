from sqlalchemy import create_engine, text

DATABASE_URL = "mysql+pymysql://root:arda123@localhost/timetravel"

engine = create_engine(DATABASE_URL)

class ReconstructionAgent:

    def get_history(self):

        with engine.connect() as conn:

            result = conn.execute(
                text(
                    "SELECT * FROM users_history"
                )
            )

            return result.fetchall()

    def get_snapshot(self, time):

        with engine.connect() as conn:

            result = conn.execute(
                text("""
                SELECT *
                FROM users_history
                WHERE change_time <= :time
                """),
                {"time": time}
            )

            rows = result.fetchall()

            formatted = []

            for row in rows:

                formatted.append({

                    "user_id": row[1],
                    "operation": row[2],
                    "old_name": row[3],
                    "new_name": row[4],
                    "old_email": row[5],
                    "new_email": row[6],
                    "time": str(row[7])

                })

            return formatted
