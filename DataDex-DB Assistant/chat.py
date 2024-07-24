from dotenv import load_dotenv
import streamlit as st
from langchain_community.utilities import SQLDatabase
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def init_database(user: str, password: str, host: str, port: str, service_name: str):
    db_url = f"oracle+cx_oracle://{user}:{password}@{host}:{port}/{service_name}"
    return SQLDatabase.from_uri(db_url)

def get_sql_chain(db):
  template = """
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    Based on the table schema below, write a SQL query that would answer the user's question. Take the conversation history into account.
    
    <SCHEMA>{schema}</SCHEMA>
    
    Conversation History: {chat_history}
    
    Write only the SQL query without semicolon and nothing else. Do not wrap the SQL query in any other text, not even backticks.
    
    For example:
    Question: which 3 artists have the most tracks?
    SQL Query: SELECT ArtistId, COUNT(*) as track_count FROM Track GROUP BY ArtistId ORDER BY track_count DESC LIMIT 3
    Question: Name 10 artists
    SQL Query: SELECT Name FROM Artist LIMIT 10
    
    Your turn:
    
    Question: {question}
    SQL Query:
    """
  
  prompt = ChatPromptTemplate.from_template(template)

  llm = ChatOpenAI(model="gpt-4o-mini")

  def get_schema(_):
      return db.get_table_info()
  
  return(
      RunnablePassthrough.assign(schema=get_schema)
      | prompt
      | llm
      | StrOutputParser()
  )
  
def get_response(user_query: str, db: SQLDatabase, chat_history: list):
  sql_chain = get_sql_chain(db)
  
  template = """
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    Based on the table schema below, question, sql query, and sql response, write a natural language response.
    <SCHEMA>{schema}</SCHEMA>

    Conversation History: {chat_history}
    SQL Query: <SQL>{query}</SQL>
    User question: {question}
    SQL Response: {response}"""
  
  prompt = ChatPromptTemplate.from_template(template)

  llm = ChatOpenAI(model="gpt-4o-mini")
  
  chain = (
    RunnablePassthrough.assign(query=sql_chain).assign(
      schema=lambda _: db.get_table_info(),
      response=lambda vars: db.run(vars["query"]),
    )
    | prompt
    | llm
    | StrOutputParser()
  )
  
  return chain.invoke({
    "question": user_query,
    "chat_history": chat_history,
  })

    
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage("Hello! I'm a DataDex, Ask me anything about the database."),
    ]

load_dotenv()

st.set_page_config(page_title= "Chat with Oracle Database", page_icon=":speech_ballon:")

st.title("DataDex Database Assistant")

with st.sidebar:
    host = st.text_input("Host", value="", key="Host")
    port = st.text_input("Port", value="", key="Port") 
    user = st.text_input("User", value="", key="User")
    password = st.text_input("Password", type="password", value="", key="Password")
    service_name = st.text_input("Service Name", value="", key="Service_Name")

    if st.button("Connect"):
        with st.spinner("Connecting to database..."):
            db = init_database(
                    st.session_state["User"],
                    st.session_state["Password"],
                    st.session_state["Host"],
                    st.session_state["Port"],
                    st.session_state["Service_Name"]
            )

            st.session_state["Database"] = db
            st.success("Connected to database!")

for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.markdown(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)

user_query = st.chat_input('Type a message...')
if user_query is not None and user_query.strip() != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        response = get_response(user_query, st.session_state["Database"], st.session_state.chat_history)
        # sql_chain = get_sql_chain(st.session_state["Database"])
        # response = sql_chain.invoke({
        #     "chat_history": st.session_state.chat_history,
        #     "question": user_query
        # })
        st.markdown(response)

    st.session_state.chat_history.append(HumanMessage(content=response))