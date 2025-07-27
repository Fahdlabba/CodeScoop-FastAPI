from fastapi.routing import APIRouter
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.services.static_metrics_services import StaticMetrics
from src.utils.file_managment import get_files
import os

router = APIRouter()
@router.get("/calculate_metrics")
async def calculate_metrics():
    """
    Calculate static metrics for the given GitHub repository URL.
    """
    try:
        if not os.path.exists("github"):
            return HTTPException(status_code=404, detail="Repository not found. Please upload the repository first.")
        
        files = get_files()
        metrics_service = StaticMetrics()

        all_metrics = []
        for module in files:
            for file in module["files"]:
                file_path = os.path.join(module["module"], file)
                with open(file_path, 'r') as f:
                    content = f.read()
                metrics = metrics_service.calculate_metrics(content)
                all_metrics.append({"file": file_path, "metrics": metrics})

        return JSONResponse(content={"metrics": all_metrics})
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})