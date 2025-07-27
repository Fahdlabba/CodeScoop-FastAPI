from fastapi.routing import APIRouter
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.services.llm.gemini import GeminiLLM
from src.utils.file_managment import get_files
import os


router = APIRouter()

@router.get("/generate_readme")
async def generate_readme():
    """
    Generate a README file for the given GitHub repository URL.
    """
    try:

        if not os.path.exists("github"):
            return HTTPException(status_code=404, detail="Repository not found. Please upload the repository first.")
        
        files = get_files()

        llm = GeminiLLM(code_tree=files)

        response = llm.generate_response()
        
        return JSONResponse(content={"readme_content": response})
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})