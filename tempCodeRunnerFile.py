from sqlalchemy import create_engine,text

DATABASE_URL="mysql+pymysql://root:arda123@localhost/timetravel"

engine=create_engine(DATABASE_URL)

class ReconstructionAgent:

    def get_history(self):

        with engine.connect() as conn:

            result=conn.execute(
                text("SELECT * FROM users_history")
            )

            return result.fetchall()
