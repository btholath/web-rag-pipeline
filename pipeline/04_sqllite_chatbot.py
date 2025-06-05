import os
from typing import List
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_sql_agent
from langchain_core.messages import SystemMessage

# Configuration
DB_PATH = "./data/ford_trucks_data.db"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    OPENAI_API_KEY = input("Please enter your OpenAI API key: ")
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

def format_sql_results(results: List[tuple], columns: List[str]) -> str:
    """Format SQL query results into a readable string"""
    if not results:
        return "No results found"
    
    output = []
    for row in results:
        row_dict = dict(zip(columns, row))
        formatted_row = "\n".join([f"{col}: {val}" for col, val in row_dict.items()])
        output.append(formatted_row)
    
    return "\n\n".join(output)

def create_ford_agent():
    """Create a SQL agent for Ford trucks database"""

    # Initialize the database connection
    db = SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")

    # Initialize the language model
    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0,
        max_tokens=1000
    )

    # Create the SQL toolkit
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    # Custom system message for Ford-specific queries
    system_message = SystemMessage(content="""You are an AI assistant specialized in querying the Ford Trucks database. 
    The database contains information about Ford trucks including models, variants, prices, engine specs, battery, charging, and sales data.

    When analyzing the data:
    1. Always format prices as currency with commas
    2. Express battery capacity in kWh, charging time in hours, and engine size in liters
    3. For analysis, mention the sample size you're using
    4. Be specific about which models and variants you're discussing

    Guidelines for your responses:
    1. If asked about trends, include specific numbers and percentages
    2. For price analysis, mention both average and range
    3. When comparing models, cite specific differences in specifications
    4. If data is insufficient, clearly state what's missing

    Before executing any query:
    1. Verify table and column names (table is 'ford_trucks')
    2. Check query syntax
    3. Ensure proper joins if needed (for future multiple tables)
    4. Add appropriate limiting clauses

    DO NOT make any modifications to the database (no INSERT, UPDATE, DELETE, etc.).
    """)

    # Create the agent
    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        agent_type="openai-tools",
        verbose=True,
        system_message=system_message,
    )
    
    return agent

def main():
    print("Welcome to the Ford Trucks Database Agent")
    print("Loading agent...")

    try:
        agent = create_ford_agent()
        
        print("\nAgent initialized successfully!")
        print("\nYou can ask questions about Ford trucks, such as:")
        print("- What's the average price of the Ford F-150?")
        print("- How many F-250 trucks were sold in Texas?")
        print("- Which truck has the highest towing capacity?")
        print("- Compare the specifications of F-150 and F-250")
        print("\nType 'quit' to exit")

        while True:
            question = input("\nWhat would you like to know about Ford trucks? ").strip()
            if question.lower() == 'quit':
                print("Thank you for using the Ford Trucks Database Agent. Goodbye!")
                break

            try:
                # Get response from agent
                response = agent.invoke({"input": question})
                # Print the response
                print("\nAnswer:", response["output"])
            except Exception as e:
                print(f"Error processing query: {str(e)}")
                print("Please try rephrasing your question.")
    except Exception as e:
        print(f"Error initializing agent: {str(e)}")
        print("Please check your database connection and API key.")

if __name__ == "__main__":
    main()
