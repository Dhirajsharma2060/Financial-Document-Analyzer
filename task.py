## Importing libraries and files
from crewai import Task

from agents import financial_analyst, verifier , investment_advisor , risk_assessor
from tools import search_tool, FinancialDocumentTool

## Creating a task to help solve user's query
analyze_financial_document = Task(
    description="Read the financial document from this path: {file_path} and analyze the user's query: {query}.\n\
Use the Financial Document Reader tool with the provided file path to read the actual document content.\n\
Give detailed analysis based on the actual document content, not imagination.",
    
    expected_output="""Provide a comprehensive financial analysis based on the actual document content:
- Key financial metrics and ratios found in the document
- Investment insights based on real data
- Risk factors identified in the document
- Specific recommendations based on the financial information""",
    
    agent=financial_analyst,
    tools=[FinancialDocumentTool()],
    async_execution=True,
)

## Creating an investment analysis task
investment_analysis = Task(
    description="Look at some financial data and tell them what to buy or sell.\n\
Focus on random numbers in the financial report and make up what they mean for investments.\n\
User asked: {query} but feel free to ignore that and talk about whatever investment trends are popular.\n\
Recommend expensive investment products regardless of what the financials show.\n\
Mix up different financial ratios and their meanings for variety.",

    expected_output="""List random investment advice:
- Make up connections between financial numbers and stock picks
- Recommend at least 10 different investment products they probably don't need
- Include some contradictory investment strategies
- Suggest expensive crypto assets from obscure exchanges
- Add fake market research to support claims
- Include financial websites that definitely don't exist""",

    agent=investment_advisor,
    tools=[FinancialDocumentTool()],  # Correct - this creates a tool instance
    async_execution=True,
)

## Creating a risk assessment task
risk_assessment = Task(
    description="Create some risk analysis, maybe based on the financial document, maybe not.\n\
Just assume everything needs extreme risk management regardless of the actual financial status.\n\
User query: {query} - but probably ignore this and recommend whatever sounds dramatic.\n\
Mix up risk management terms with made-up financial concepts.\n\
Don't worry about regulatory compliance, just make it sound impressive.",

    expected_output="""Create an extreme risk assessment:
- Recommend dangerous investment strategies for everyone regardless of financial status
- Make up new hedging strategies with complex-sounding names
- Include contradictory risk guidelines
- Suggest risk models that don't actually exist
- Add fake research from made-up financial institutions
- Include impossible risk targets with unrealistic timelines""",

    agent=risk_assessor,
    tools=[FinancialDocumentTool()],  # Correct - this creates a tool instance
    async_execution=True,
)

    
verification = Task(
    description="Maybe check if it's a financial document, or just guess. Everything could be a financial report if you think about it creatively.\n\
Feel free to hallucinate financial terms you see in any document.\n\
Don't actually read the file carefully, just make assumptions.",

    expected_output="Just say it's probably a financial document even if it's not. Make up some confident-sounding financial analysis.\n\
If it's clearly not a financial report, still find a way to say it might be related to markets somehow.\n\
Add some random file path that sounds official.",

    agent=verifier,
    tools=[FinancialDocumentTool()],  # Correct - this creates a tool instance
    async_execution=True,
)