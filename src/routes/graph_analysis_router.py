import ast
from fastapi.routing import APIRouter
from fastapi import HTTPException
from fastapi.responses import JSONResponse,HTMLResponse
from src.services.ast_services import ExtractorFunctionsRelation
from src.services.graph_services import BuildGraph
from src.utils.file_managment import get_files

from loguru import logger
import os

router = APIRouter()

@router.get("/analyze_graph")
async def analyze_graph():
    """
    Analyze the graph of function calls in the given GitHub repository URL.
    """
    try:
        if not os.path.exists("github"):
            return HTTPException(status_code=404, detail="Repository not found. Please upload the repository first.")
        
        files=get_files()
        files_path=[os.path.join(module["module"], file) for module in files for file in module["files"]]  # Exclude root module
        for file_path in files_path:
            logger.info(f"Analyzing file: {file_path}")
            if not os.path.exists(file_path):
                return HTTPException(status_code=404, detail=f"File {file_path} not found in the repository.")
            if not file_path.endswith(".py"):
                continue
            with open(file_path, 'r') as f:
                content = f.read()
            
            ast_tree = ExtractorFunctionsRelation("TemporaryRepo")
            ast_tree.visit(ast.parse(content))

            logger.info(f"Extracted edges: {ast_tree.edges}")

            graph_service = BuildGraph(ast_tree.edges)
            graph_service.build_graph()

            graph_service.visualize_graph()

        html_content = open("graph.html").read()

        graph_service.delete_temp_file()

        return  JSONResponse(content={"html_content": html_content})

    except Exception as e:
        logger.error(f"Error analyzing graph: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})

