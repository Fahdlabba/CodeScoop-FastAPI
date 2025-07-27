from git import Repo 

class GitHubService:
    def __init__(self, repo_path: str):
        self.repo_path:str = repo_path
        self.repo:Repo=None
    
 
    def clone_repo(self)->None:
        try:
            self.repo = Repo.clone_from(url=self.repo_path, to_path="github")
            

        except Exception as e:
            print(f"Error cloning repository: {e}")
            

