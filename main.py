
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from src.routes.graph_analysis_router import router as graph_analysis_router
from src.routes.github_service import router as github_service_router
from src.routes.readme_generator import router as readme_generator_router
from src.routes.code_analysis import router as code_analysis_router
from src.routes.code_review import router as code_review_router
from dotenv import load_dotenv
import os
load_dotenv()

app = FastAPI()


ascii_art = """

#####################################################################################
#__        __   _                            _____                                  #
#\ \      / /__| | ___ ___  _ __ ___   ___  |_   _|__                               #
# \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \   | |/ _ \                              #
#  \ V  V /  __/ | (_| (_) | | | | | |  __/   | | (_) |                             #
#  _\_/\_/ \___|_|\___\___/|_| |_| |_|\___|   |_|\___/    _   _                     #
# / ___|___   __| | ___/ ___|  ___ ___   ___  _ __       | \ | | _____  ___   _ ___ #
#| |   / _ \ / _` |/ _ \___ \ / __/ _ \ / _ \| '_ \ _____|  \| |/ _ \ \/ / | | / __|#
#| |__| (_) | (_| |  __/___) | (_| (_) | (_) | |_) |_____| |\  |  __/>  <| |_| \__ \#
# \____\___/ \__,_|\___|____/ \___\___/ \___/| .__/      |_| \_|\___/_/\_\\__,_|___/#
#                                            |_|                                    #
#####################################################################################


"""

app.add_middleware(CORSMiddleware,
    allowed_origins=[os.getenv("CORPS_ALLOWED")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(graph_analysis_router, prefix="/graph_analysis", tags=["Graph Analysis"])
app.include_router(github_service_router, prefix="/github", tags=["GitHub Service"])
app.include_router(readme_generator_router, prefix="/readme", tags=["README Generator"])
app.include_router(code_analysis_router, prefix="/code_analysis", tags=["Code Analysis"])
app.include_router(code_review_router, prefix="/code_review", tags=["Code Review"])


@app.get("/",response_class=PlainTextResponse)
async def root():
    return ascii_art

