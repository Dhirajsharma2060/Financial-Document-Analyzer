## Importing libraries and files
from crewai import Task

from agents import financial_analyst, verifier , investment_advisor , risk_assessor
from tools import search_tool, FinancialDocumentTool

## Creating a task to help solve user's query
analyze_financial_document = Task(
    description="Analyze the financial document at path: {file_path} to answer the user's query: {query}.\n\
Use the Financial Document Reader tool to read the actual document content from the provided file path.\n\
Provide accurate financial analysis based on real data from the document.\n\
Focus on factual information such as revenue, profit margins, cash flow, debt levels, and growth trends.\n\
Identify genuine risks and opportunities based on the actual financial metrics in the document.",

    expected_output="""Provide a comprehensive financial analysis including:
- Key financial metrics (revenue, profit, cash flow, debt ratios)
- Actual trends observed in the data
- Genuine investment insights based on document content
- Real risk factors identified from the financial statements
- Specific recommendations backed by the document's data
- All analysis must be grounded in factual information from the PDF""",

    agent=financial_analyst,
    tools=[FinancialDocumentTool()],
    async_execution=True,
)

## Creating an investment analysis task
investment_analysis = Task(
    description="Read the financial document at {file_path} and provide investment analysis for query: {query}.\n\
Use the Financial Document Reader tool to extract actual financial data.\n\
Base all investment recommendations on real metrics from the document.\n\
Consider factors like P/E ratios, debt-to-equity, revenue growth, and market position.\n\
Provide conservative and aggressive investment scenarios based on the data.",

    expected_output="""Investment analysis report containing:
- Current financial position summary from the document
- Investment strengths and weaknesses based on actual data
- Risk-adjusted return expectations
- Portfolio allocation suggestions
- Timeline for investment decisions
- All recommendations must cite specific data from the financial document""",

    agent=investment_advisor,
    tools=[FinancialDocumentTool()],
    async_execution=True,
)

## Creating a risk assessment task
risk_assessment = Task(
    description="Analyze the financial document at {file_path} to identify real financial risks for query: {query}.\n\
Use the Financial Document Reader tool to examine actual financial statements.\n\
Focus on liquidity risks, debt levels, market exposure, and operational risks.\n\
Provide quantitative risk assessment based on document data.\n\
Consider regulatory compliance and industry-specific risks.",

    expected_output="""Risk assessment report including:
- Quantified financial risks from the document data
- Liquidity and solvency analysis
- Market and operational risk factors
- Regulatory and compliance considerations
- Risk mitigation strategies
- All risk assessments must be based on actual document content""",

    agent=risk_assessor,
    tools=[FinancialDocumentTool()],
    async_execution=True,
)

verification = Task(
    description="Verify that the file at {file_path} is a valid financial document using the Financial Document Reader tool.\n\
Read the document content and confirm it contains financial statements, reports, or relevant financial data.\n\
Validate the document structure and identify the type of financial report.\n\
Ensure the document has sufficient data for analysis.",

    expected_output="""Document verification report:
- Confirmation of document type (10-K, 10-Q, annual report, etc.)
- Summary of available financial sections
- Data quality assessment
- Recommendation on analysis feasibility
- Any limitations or missing information noted""",

    agent=verifier,
    tools=[FinancialDocumentTool()],
    async_execution=True,
)