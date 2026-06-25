from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, text

from agents.reconstruction_agent import ReconstructionAgent
from agents.comparison_agent import ComparisonAgent
from agents.explanation_agent import ExplanationAgent
from agents.query_agent import QueryAgent
from agents.stats_agent import StatsAgent

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL="mysql+pymysql://root:arda123@localhost/timetravel"

engine=create_engine(DATABASE_URL)

history_agent=ReconstructionAgent()
comparison_agent=ComparisonAgent()
explanation_agent=ExplanationAgent()
query_agent=QueryAgent()
stats_agent=StatsAgent()


class User(BaseModel):
    name:str
    email:str


# ================= HISTORY =================

@app.get("/history")
def history():

    rows=history_agent.get_history()

    formatted=[]

    for row in rows:

        formatted.append({

            "User ID":row[1],
            "Operation":row[2],
            "Old Name":row[3],
            "New Name":row[4],
            "Old Email":row[5],
            "New Email":row[6],
            "Time":str(row[7])

        })

    return {"history":formatted}


# ================= COMPARE =================

@app.get("/compare")
def compare():

    data=comparison_agent.compare_history()

    return {
        "comparison":str(data)
    }


# ================= EXPLAIN =================

@app.get("/explain")
def explain():

    return {
        "explanation":
        explanation_agent.explain_changes()
    }


# ================= SEARCH =================

@app.get("/query/{question}")
def query(question:str):

    result=query_agent.process_query(question)

    return {
        "result":str(result)
    }


# ================= SNAPSHOT =================

@app.get("/snapshot/{time}")
def snapshot(time:str):

    return {
        "snapshot":
        str(history_agent.get_snapshot(time))
    }


# ================= STATS =================

@app.get("/stats")
def stats():

    rows=history_agent.get_history()

    insert_count=0
    update_count=0

    for row in rows:

        if row[2]=="INSERT":
            insert_count+=1

        elif row[2]=="UPDATE":
            update_count+=1

    return {

        "Total Records":len(rows),
        "Insert Operations":insert_count,
        "Update Operations":update_count

    }


# ================= ADD USER =================

@app.post("/add_user")
def add_user(user:User):

    with engine.connect() as conn:

        conn.execute(
            text("""
            INSERT INTO users
            (name,email)

            VALUES
            (:name,:email)
            """),

            {
                "name":user.name,
                "email":user.email
            }

        )

        conn.commit()

    return {

        "message":"User added successfully"

    }
