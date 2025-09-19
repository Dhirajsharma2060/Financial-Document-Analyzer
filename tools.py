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
                
            from langchain_community.document_loaders import PyPDFLoader
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
        
## Creating Investment Analysis Tool
class InvestmentTool:
    @staticmethod
    async def analyze_investment_tool(financial_document_data: str) -> str:
        """Analyze financial document data for investment insights"""
        
        def _process_data_sync(data: str) -> str:
            # Clean up the data format efficiently
            processed_data = " ".join(data.split())  # Remove all extra whitespace
            
            # TODO: Implement investment analysis logic here
            return "Investment analysis functionality to be implemented"
        
        # Run in thread to avoid blocking
        return await asyncio.to_thread(_process_data_sync, financial_document_data)

## Creating Risk Assessment Tool
class RiskTool:
    @staticmethod
    async def create_risk_assessment_tool(financial_document_data: str) -> str:
        """Create risk assessment from financial document data"""
        
        def _assess_risk_sync(data: str) -> str:
            # TODO: Implement risk assessment logic here
            return "Risk assessment functionality to be implemented"
        
        # Run in thread to avoid blocking
        return await asyncio.to_thread(_assess_risk_sync, financial_document_data)