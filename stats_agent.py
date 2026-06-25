from sqlalchemy import create_engine, text

DATABASE_URL = "mysql+pymysql://root:arda123@localhost/timetravel"

engine = create_engine(DATABASE_URL)

class StatsAgent:

    def get_stats(self):

        with engine.connect() as conn:

            total = conn.execute(
                text("SELECT COUNT(*) FROM users_history")
            ).scalar()

            inserts = conn.execute(
                text("""
                SELECT COUNT(*)
                FROM users_history
                WHERE operation_type='INSERT'
                """)
            ).scalar()

            updates = conn.execute(
                text("""
                SELECT COUNT(*)
                FROM users_history
                WHERE operation_type='UPDATE'
                """)
            ).scalar()

            return {
                "total_records": total,
                "insert_count": inserts,
                "update_count": updates
            }
