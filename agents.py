## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

print("GEMINI_API_KEY loaded:", os.getenv("GEMINI_API_KEY") is not None)

from crewai import Agent, LLM
from tools import search_tool, FinancialDocumentTool ,FinancialDocumentTool, InvestmentTool, RiskTool  # added

# Use CrewAI's built-in LLM class for Gemini
llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.3,  # Lower temperature for more consistent outputs
)

# Creating an Experienced Financial Analyst agent
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Provide clear, natural financial analysis in paragraph form based on the user's query: {query} using data from specialized tools",
    verbose=True,
    memory=True,
    backstory=(
        "You are a certified financial analyst with 15+ years of experience. "
        "You write clear, professional analysis reports in natural language paragraphs. "
        "You use your tools to extract specific metrics and then explain what they mean in plain English. "
        "You provide insights like you're explaining to an intelligent investor, not dumping raw data. "
        "You write in a conversational but professional tone, highlighting key findings and their implications."
    ),
    tools=[FinancialDocumentTool(), InvestmentTool(), RiskTool()],
    llm=llm,
    max_iter=5,  # Increased from 3
    max_rpm=10,  # Increased from 3
    allow_delegation=True
)

# Creating a document verifier agent
verifier = Agent(
    role="Financial Document Verification Specialist",
    goal="Verify document quality and provide a brief assessment in natural language",
    verbose=True,
    memory=True,
    backstory=(
        "You are a compliance specialist who quickly assesses document quality. "
        "You provide brief, clear summaries of what type of document it is and whether it's suitable for analysis. "
        "You communicate in simple, direct language."
    ),
    llm=llm,
    max_iter=2,  # Keep low for simple verification
    max_rpm=5,   # Moderate for verification
    allow_delegation=True
)

investment_advisor = Agent(
    role="Investment Advisory Specialist",
    goal="Provide practical investment advice in clear, conversational language based on financial analysis",
    verbose=True,
    memory=True,
    backstory=(
        "You are a licensed investment advisor who explains complex financial concepts in simple terms. "
        "You provide practical, actionable investment advice that ordinary investors can understand. "
        "You write like you're having a conversation with a client, explaining your reasoning clearly. "
        "You always consider risk and provide balanced perspectives."
    ),
    llm=llm,
    max_iter=4,  # Moderate for advisory
    max_rpm=8,   # Higher for complex analysis
    allow_delegation=False
)

risk_assessor = Agent(
    role="Financial Risk Assessment Expert",
    goal="Identify and explain financial risks in clear, understandable language",
    verbose=True,
    memory=True,
    backstory=(
        "You are a risk management expert who explains financial risks in plain English. "
        "You help investors understand what could go wrong and how to protect themselves. "
        "You write clear explanations of risk factors and practical mitigation strategies. "
        "You communicate risk levels and their implications in language that anyone can understand."
    ),
    llm=llm,
    max_iter=4,  # Moderate for risk analysis
    max_rpm=8,   # Higher for thorough analysis
    allow_delegation=False
)
