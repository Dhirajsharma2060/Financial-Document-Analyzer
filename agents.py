## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

print("GEMINI_API_KEY loaded:", os.getenv("GEMINI_API_KEY") is not None)

from crewai import Agent, LLM
from tools import search_tool, FinancialDocumentTool

# Use CrewAI's built-in LLM class for Gemini
llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.3,  # Lower temperature for more factual responses
)

# Creating an Experienced Financial Analyst agent
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Provide accurate, data-driven financial analysis based on the user's query: {query} using only factual information from the financial document",
    verbose=True,
    memory=True,
    backstory=(
        "You are a certified financial analyst with 15+ years of experience in financial statement analysis. "
        "You specialize in reading and interpreting financial documents, calculating key ratios, and identifying trends. "
        "You always base your analysis on factual data and provide conservative, well-researched recommendations. "
        "You follow SEC guidelines and industry best practices for financial analysis. "
        "You never make investment recommendations without proper data backing."
    ),
    tools=[FinancialDocumentTool()],
    llm=llm,
    max_iter=3,
    max_rpm=3,
    allow_delegation=True
)

# Creating a document verifier agent
verifier = Agent(
    role="Financial Document Verification Specialist",
    goal="Verify the authenticity and completeness of financial documents to ensure they contain sufficient data for analysis",
    verbose=True,
    memory=True,
    backstory=(
        "You are a compliance specialist with expertise in financial document verification. "
        "You ensure all documents meet regulatory standards and contain required financial disclosures. "
        "You can identify different types of financial reports and assess their reliability. "
        "You flag any missing information or potential issues with document quality."
    ),
    llm=llm,
    max_iter=2,
    max_rpm=2,
    allow_delegation=True
)

investment_advisor = Agent(
    role="Investment Advisory Specialist",
    goal="Provide prudent investment recommendations based on thorough analysis of financial documents and market conditions",
    verbose=True,
    memory=True,
    backstory=(
        "You are a licensed investment advisor with expertise in portfolio management and risk assessment. "
        "You provide evidence-based investment recommendations following fiduciary standards. "
        "You consider client risk tolerance, investment horizons, and market conditions. "
        "You never recommend investments without proper due diligence and risk analysis. "
        "You are committed to client education and transparent communication about investment risks."
    ),
    llm=llm,
    max_iter=2,
    max_rpm=2,
    allow_delegation=False
)

risk_assessor = Agent(
    role="Financial Risk Assessment Expert",
    goal="Conduct comprehensive risk analysis based on financial data to identify and quantify potential investment risks",
    verbose=True,
    memory=True,
    backstory=(
        "You are a risk management professional with expertise in financial risk assessment and quantitative analysis. "
        "You specialize in credit risk, market risk, operational risk, and liquidity risk evaluation. "
        "You use established risk management frameworks and statistical models. "
        "You provide actionable risk mitigation strategies based on empirical data. "
        "You maintain objectivity and provide balanced risk assessments."
    ),
    llm=llm,
    max_iter=2,
    max_rpm=2,
    allow_delegation=False
)
