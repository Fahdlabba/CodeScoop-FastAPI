from fastapi.routing import APIRouter
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.services.llm.gemini import GeminiLLM
from src.utils.file_managment import get_files
import os


router = APIRouter()

@router.post("/suggestions")
async def code_suggestions(graph: str):
    """
    Generate code suggestions for the given code graph.
    """
    try:

        if not os.path.exists("github"):
            return HTTPException(status_code=404, detail="Repository not found. Please upload the repository first.")
        
        files = get_files()

        file_content = {}


        for module in files:
            for file in module["files"]:
                file_path = os.path.join(module["module"], file)
                if not os.path.exists(file_path):
                    raise HTTPException(status_code=404, detail=f"File {file_path} not found.")
                
                with open(file_path, "r") as f:
                    content = f.read()
                    file_content[file] = content

        
                
                
        llm = GeminiLLM(code_tree=file_content, graph=graph)

        response = llm.generate_response(task_type="code_review")
        return JSONResponse(content={"suggestions": response})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})