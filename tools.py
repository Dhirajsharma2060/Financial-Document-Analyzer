## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai_tools import SerperDevTool
from langchain_community.document_loaders import PyPDFLoader
import asyncio
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import re

## Creating search tool
search_tool = SerperDevTool()

## Creating custom pdf reader tool
class FinancialDocumentInput(BaseModel):
    """Input schema for FinancialDocumentTool."""
    path: str = Field(description="Path to the PDF file to analyze", default="data/sample.pdf")

class FinancialDocumentTool(BaseTool):
    name: str = "Financial Document Reader"
    description: str = "Tool to read and extract content from PDF financial documents. Always use the file_path from the task context."
    args_schema: Type[BaseModel] = FinancialDocumentInput
    
    def _run(self, path: str = 'data/sample.pdf') -> str:
        """Tool to read data from a pdf file from a path

        Args:
            path (str, optional): Path of the pdf file. Defaults to 'data/sample.pdf'.

        Returns:
            str: Full Financial Document file content
        """
        
        try:
            # Check if file exists
            if not os.path.exists(path):
                return f"Error: File not found at path: {path}"
                
            loader = PyPDFLoader(path)
            docs = loader.load()
            
            if not docs:
                return f"Error: No content found in PDF at path: {path}"
            
            full_report = ""
            for data in docs:
                content = data.page_content
                # Remove extra whitespaces and format properly
                while "\n\n" in content:
                    content = content.replace("\n\n", "\n")
                full_report += content + "\n"
                
            return f"Financial document content from {path}:\n\n{full_report}"
        except Exception as e:
            return f"Error reading PDF from {path}: {str(e)}"

## Creating Investment Analysis Tool - NOW TAKES FILE PATH
class InvestmentTool(BaseTool):
    name: str = "Investment Analysis Tool"
    description: str = "Extract key investment metrics from a PDF file path. Reads the PDF first, then analyzes for investment insights."
    args_schema: Type[BaseModel] = FinancialDocumentInput  # Same schema as PDF tool
    
    def _run(self, path: str = 'data/sample.pdf') -> str:
        """Analyze PDF file for investment insights
        
        Args:
            path (str): Path to PDF file to analyze
            
        Returns:
            str: Investment analysis results
        """
        try:
            # First, read the PDF
            if not os.path.exists(path):
                return f"Error: File not found at path: {path}"
                
            loader = PyPDFLoader(path)
            docs = loader.load()
            
            if not docs:
                return f"Error: No content found in PDF at path: {path}"
            
            # Extract text content
            text = ""
            for data in docs:
                text += data.page_content + "\n"
            
            # Now analyze the text for investment metrics
            insights = []
            
            # Extract revenue information
            revenue_patterns = [
                r'(?:total\s+)?revenues?\s*:?\s*\$?([\d,\.]+)\s*(?:billion|million|B|M)',
                r'revenue\s+(?:of\s+)?\$?([\d,\.]+)\s*(?:billion|million|B|M)',
                r'net\s+revenue\s*:?\s*\$?([\d,\.]+)'
            ]
            
            for pattern in revenue_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    insights.append(f"Revenue: ${matches[0]}")
                    break
            
            # Extract profit/income information
            profit_patterns = [
                r'(?:net\s+)?income\s*:?\s*\$?([\d,\.]+)\s*(?:billion|million|B|M)',
                r'operating\s+income\s*:?\s*\$?([\d,\.]+)',
                r'profit\s*:?\s*\$?([\d,\.]+)'
            ]
            
            for pattern in profit_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    insights.append(f"Net Income: ${matches[0]}")
                    break
            
            # Extract margin information
            margin_matches = re.findall(r'(?:operating\s+|gross\s+)?margin\s*:?\s*([\d\.]+)%', text, re.IGNORECASE)
            if margin_matches:
                insights.append(f"Margin: {margin_matches[0]}%")
            
            # Extract growth information
            growth_matches = re.findall(r'(?:revenue\s+)?growth\s*:?\s*([+-]?[\d\.]+)%', text, re.IGNORECASE)
            if growth_matches:
                insights.append(f"Growth Rate: {growth_matches[0]}%")
            
            # Extract cash flow information
            cash_flow_matches = re.findall(r'(?:free\s+)?cash\s+flow\s*:?\s*\$?([\d,\.]+)', text, re.IGNORECASE)
            if cash_flow_matches:
                insights.append(f"Cash Flow: ${cash_flow_matches[0]}")
            
            # Extract EPS information
            eps_matches = re.findall(r'earnings\s+per\s+share\s*:?\s*\$?([\d\.]+)', text, re.IGNORECASE)
            if eps_matches:
                insights.append(f"EPS: ${eps_matches[0]}")
            
            if insights:
                result = f"Investment Analysis from {path}:\n\n"
                result += "Investment Metrics Found:\n" + "\n".join([f"• {insight}" for insight in insights])
                
                # Add investment recommendation based on metrics
                if any("growth" in insight.lower() for insight in insights):
                    result += "\n\nInvestment Outlook: Growth metrics indicate potential for capital appreciation."
                if any("margin" in insight.lower() for insight in insights):
                    result += "\nProfitability: Company shows operational efficiency through margin analysis."
                    
                return result
            else:
                return f"Investment Analysis from {path}: No clear investment metrics found in the document."
                
        except Exception as e:
            return f"Error analyzing investment metrics from {path}: {str(e)}"

## Creating Risk Assessment Tool - NOW TAKES FILE PATH
class RiskTool(BaseTool):
    name: str = "Risk Assessment Tool"
    description: str = "Identify and analyze financial risks from a PDF file path. Reads the PDF first, then analyzes for risk factors."
    args_schema: Type[BaseModel] = FinancialDocumentInput  # Same schema as PDF tool
    
    def _run(self, path: str = 'data/sample.pdf') -> str:
        """Assess financial risks from PDF file
        
        Args:
            path (str): Path to PDF file to analyze
            
        Returns:
            str: Risk assessment results
        """
        try:
            # First, read the PDF
            if not os.path.exists(path):
                return f"Error: File not found at path: {path}"
                
            loader = PyPDFLoader(path)
            docs = loader.load()
            
            if not docs:
                return f"Error: No content found in PDF at path: {path}"
            
            # Extract text content
            text = ""
            for data in docs:
                text += data.page_content + "\n"
            
            # Now analyze the text for risks
            risks = []
            risk_level = "Low"
            
            # Debt and leverage risks
            debt_patterns = [
                r'total\s+debt\s*:?\s*\$?([\d,\.]+)',
                r'debt.to.equity\s*:?\s*([\d\.]+)',
                r'leverage\s*:?\s*([\d\.]+)'
            ]
            
            for pattern in debt_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    risks.append(f"Debt Exposure: {matches[0]}")
                    risk_level = "Medium"
                    break
            
            # Liquidity risks
            liquidity_keywords = ['liquidity', 'cash shortage', 'working capital deficit', 'cash crunch']
            for keyword in liquidity_keywords:
                if keyword in text.lower():
                    risks.append(f"Liquidity Risk: {keyword.title()} mentioned in document")
                    risk_level = "High"
                    break
            
            # Market and operational risks
            risk_keywords = [
                'market volatility', 'economic uncertainty', 'regulatory changes',
                'competitive pressure', 'supply chain disruption', 'cybersecurity',
                'inflation', 'interest rate', 'currency fluctuation'
            ]
            
            found_risks = [keyword for keyword in risk_keywords if keyword in text.lower()]
            if found_risks:
                risks.append(f"Market/Operational Risks: {', '.join(found_risks)}")
                if len(found_risks) > 2:
                    risk_level = "High"
                elif risk_level == "Low":
                    risk_level = "Medium"
            
            # Declining metrics
            decline_patterns = [
                r'(?:revenue\s+)?decreas(?:ed?|ing)\s+(?:by\s+)?([\d\.]+)%',
                r'(?:profit\s+)?drop(?:ped?|ping)\s+(?:by\s+)?([\d\.]+)%',
                r'down\s+([\d\.]+)%'
            ]
            
            for pattern in decline_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    risks.append(f"Performance Decline: {matches[0]}% decrease noted")
                    if float(matches[0]) > 10:
                        risk_level = "High"
                    elif risk_level == "Low":
                        risk_level = "Medium"
                    break
            
            # Credit rating mentions
            if any(word in text.lower() for word in ['downgrade', 'credit rating', 'default risk']):
                risks.append("Credit Risk: Rating or default concerns mentioned")
                risk_level = "High"
            
            if risks:
                result = f"Risk Assessment from {path} - Overall Risk Level: {risk_level}\n\n"
                result += "Identified Risks:\n" + "\n".join([f"• {risk}" for risk in risks])
                
                # Risk mitigation suggestions
                result += "\n\nRisk Mitigation Recommendations:"
                if risk_level == "High":
                    result += "\n• Consider reducing position size or hedging strategies"
                    result += "\n• Monitor financial metrics closely"
                    result += "\n• Diversify portfolio to reduce concentration risk"
                elif risk_level == "Medium":
                    result += "\n• Maintain moderate position sizing"
                    result += "\n• Regular monitoring of key risk factors"
                else:
                    result += "\n• Standard portfolio management practices apply"
                    
                return result
            else:
                return f"Risk Assessment from {path}: Low risk profile - No significant risk factors identified."
                
        except Exception as e:
            return f"Error assessing risks from {path}: {str(e)}"