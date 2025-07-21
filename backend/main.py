import os
import uvicorn
from dotenv import load_dotenv
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent import agent_executor

load_dotenv()

app = FastAPI(title="Air Quality Analysis Agent")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
    table_data: Optional[List[Dict[str, Any]]] = None
    chart_data: Optional[Dict[str, Any]] = None
    chart_type: Optional[str] = None

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    try:
        response = agent_executor.invoke({"input": request.query})

        print("Response: ", response)
        
        answer_text = response.get('output', '')
        
        table_data = None
        chart_data = None
        chart_type = None
        
        # Look for JSON data in the response that could be table data
        if '|' in answer_text:  # Markdown table detected
            # Extract table for frontend rendering
            lines = answer_text.split('\n')
            table_lines = [line for line in lines if line.strip().startswith('|') and line.strip().endswith('|')]
            
            if len(table_lines) >= 2:  # Header + at least one data row
                headers = [cell.strip() for cell in table_lines[0].split('|')[1:-1]]
                table_data = []
                for line in table_lines[2:]:  # Skip header separator
                    if '---' not in line:
                        cells = [cell.strip() for cell in line.split('|')[1:-1]]
                        if len(cells) == len(headers):
                            row_dict = dict(zip(headers, cells))
                            table_data.append(row_dict)
        
        # Suggest chart type based on query content
        query_lower = request.query.lower()
        if 'hour' in query_lower or 'time' in query_lower:
            chart_type = 'line'
        elif 'room' in query_lower and 'compare' in query_lower:
            chart_type = 'bar'
        elif 'variation' in query_lower or 'range' in query_lower:
            chart_type = 'box'
        
        return QueryResponse(
            answer=answer_text,
            table_data=table_data,
            chart_data=chart_data,
            chart_type=chart_type
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)

    uvicorn.run(app, host="0.0.0.0", port=8000)