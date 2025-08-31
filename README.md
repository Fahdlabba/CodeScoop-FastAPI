# GitHub Repository Analysis and README Generator

## Overview
This project provides a comprehensive suite of tools for analyzing GitHub repositories, generating README files, and performing code reviews. It leverages various services including static code analysis, call graph generation, and large language models (LLMs) for intelligent insights. The application is built with FastAPI, offering a robust API for interacting with its functionalities.

## Features
- **Repository Management**: Clone and delete GitHub repositories.
- **README Generation**: Automatically generate `README.md` files for cloned repositories using LLMs.
- **Code Review**: Get intelligent code suggestions and reviews based on static analysis and call graphs.
- **Graph Analysis**: Visualize the call graph of functions and methods within a Python codebase.
- **Static Code Metrics**: Calculate cyclomatic complexity, lines of code (LOC), logical lines of code (LLOC), and comment count for Python files.
- **LLM Integration**: Supports multiple LLM providers (Gemini, Azure OpenAI, Groq) for various text generation tasks.
- **File Content Fetching**: A tool for LLMs to fetch content of specific files within the repository.

## Project Structure

- `github/main.py`: The main FastAPI application entry point, setting up routes and middleware.
- `github/requirements.txt`: Lists all Python dependencies required for the project.
- `github/src/prompt/`: Contains prompt templates used by the LLMs.
    - `code_review.txt`: Prompt template for code review tasks.
    - `system_prompt_template.txt`: General system prompt template.
- `github/src/config/settings.py`: Manages application settings and environment variables using Pydantic.
- `github/src/routes/`: Defines API endpoints for different functionalities.
    - `readme_generator.py`: Endpoint for generating README files.
    - `code_review.py`: Endpoint for generating code review suggestions.
    - `github_service.py`: Endpoints for uploading and deleting GitHub repositories.
    - `graph_analysis_router.py`: Endpoint for analyzing and visualizing code call graphs.
    - `code_analysis.py`: Endpoint for calculating static code metrics.
- `github/src/services/`: Contains core logic and services.
    - `static_metrics_services.py`: Implements static code metrics calculation (cyclomatic complexity, maintainability index, raw metrics).
    - `graph_services.py`: Handles building and visualizing call graphs using NetworkX and Pyvis.
    - `github_service.py`: Provides functionalities for cloning GitHub repositories.
    - `ast_services.py`: Extracts function and class relationships from Python abstract syntax trees (AST).
- `github/src/services/tools/fetch_file_content.py`: A tool function to fetch file content, primarily used by LLMs.
- `github/src/services/llm/`: Integrates with different Large Language Models.
    - `azure_openai.py`: Service for interacting with Azure OpenAI models.
    - `llm.py`: Abstract base class for LLM services.
    - `gemini.py`: Service for interacting with Google Gemini models.
    - `groq.py`: Service for interacting with Groq models.
- `github/src/utils/file_managment.py`: Utility functions for file and directory operations, such as getting file lists and deleting repositories.

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd github
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory and add necessary API keys and settings. For example:
   ```
   GROQ_API_KEY="your_groq_api_key"
   GEMINI_API_KEY="your_gemini_api_key"
   AZURE_ENDPOINT="your_azure_openai_endpoint"
   AZURE_KEY="your_azure_openai_key"
   api_version="your_azure_api_version"
   CORPS_ALLOWED="http://localhost:3000" # Or your frontend URL
   ENVIRONMENT="local" # dev or prod
   ```

## Usage

1. **Run the FastAPI application**:
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at `http://127.0.0.1:8000`. You can access the API documentation at `http://127.00.1:8000/docs`.

2. **Upload a GitHub repository**:
   Use the `/github/upload_repo` endpoint with a `POST` request, providing the `repo_url` as a query parameter.
   Example using `curl`:
   ```bash
   curl -X POST "http://127.0.0.1:8000/github/upload_repo?repo_url=https://github.com/your-org/your-repo.git"
   ```

3. **Generate a README**:
   After uploading a repository, call the `/readme/generate_readme` endpoint with a `GET` request.
   ```bash
   curl -X GET "http://127.0.0.1:8000/readme/generate_readme"
   ```

4. **Analyze the graph**:
    Call the `/graph_analysis/analyze_graph` endpoint with a `GET` request. This will generate `graph.html` and return the HTML content.
    ```bash
    curl -X GET "http://127.0.0.1:8000/graph_analysis/analyze_graph"
    ```

5. **Calculate static metrics**:
    Call the `/code_analysis/calculate_metrics` endpoint with a `GET` request.
    ```bash
    curl -X GET "http://127.0.0.1:8000/code_analysis/calculate_metrics"
    ```

6. **Get code review suggestions**:
    Call the `/code_review/suggestions` endpoint with a `POST` request, providing the code graph in the request body.
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"graph": "your_code_graph_json_or_text"}' "http://127.0.0.1:8000/code_review/suggestions"
    ```

7. **Delete the cloned repository**:
   Use the `/github/delete_repo` endpoint with a `DELETE` request.
   ```bash
   curl -X DELETE "http://127.0.0.1:8000/github/delete_repo"
   ```

## Contributing
Contributions are welcome! Please feel free to open issues or submit pull requests.
