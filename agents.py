from crewai import Agent
from tools import tool
from dotenv import load_dotenv
load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
import os

## call the gemini models

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro",
                             verbose=True,
                             temperature=0.5,
                             google_api_key=os.getenv("GOOGLE_API_KEY"))



# Agent 1: BigBasket Industry Researcher

industry_researcher = Agent(
    role="Industry Researcher",
    goal= "Gather strategic insights about the company’s industry, key products, and market positioning, with a focus on AI/ML opportunities.",
    verbose=False,
    memory=True,
    backstory=("You specialize in identifying AI/ML applications in industries. For the company {topic}, gather only the most critical information such as: product offerings, key competitors, and strategic focus in AI and automation. The information should help generate actionable AI use cases that align with the company’s goals."
               ),
    tools=[tool],
    llm=llm,
    allow_delegation=False
)

# Agent 2: BigBasket Use Case Generator

use_case_generator = Agent(
    role="AI Solutions Architect",
    goal="Analyze industry AI/ML trends to generate 3-5 actionable use cases relevant to {topic} that improve operations, customer experiences, and strategic growth.",
    verbose=False,
    memory=True,
    backstory=("You specialize in generating AI-powered solutions. Based on current industry trends, propose 3-5 use cases for leveraging AI, ML, and automation to improve {topic}'s operations, customer service, and efficiency. The use cases should be directly actionable and include clear benefits for different departments."),
    tools=[tool],
    llm=llm,
    allow_delegation=True
)


# Agent 3: BigBasket Delivery Dataset Curator

resource_collector = Agent(
    role="Resource Asset Finder",
    goal="Gather high-quality, relevant datasets for the generated use cases, ensuring they are directly applicable for AI/ML model development.",
    verbose=False,
    memory=True,
    backstory=("""
       You are an expert at sourcing technical resources and datasets from various platforms. You focus on finding datasets and model assets to support the proposed use cases, ensuring {topic} has access to the necessary resources for implementation.
    """),
    tools=[tool],
    llm=llm,
    allow_delegation=True
)

