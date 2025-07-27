from fastapi.routing import APIRouter
from fastapi import  HTTPException
from fastapi.responses import JSONResponse
from src.services.github_service import GitHubService
from src.utils.file_managment import delete_repo
import os



router = APIRouter()

@router.post("/upload_repo")
async def upload_repo(repo_url: str):
    """
    Upload a GitHub repository to the server.
    """
    try:
        github_service = GitHubService(repo_url)
        github_service.clone_repo()
        return JSONResponse(content={"message": "Repository uploaded successfully."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@router.delete("/delete_repo")
async def delete_repository():
    """
    Delete the cloned GitHub repository from the server.
    """
    try:
        if not os.path.exists("github"):
            return HTTPException(status_code=404, detail="Repository not found.")
        delete_repo()
        return JSONResponse(content={"message": "Repository deleted successfully."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})