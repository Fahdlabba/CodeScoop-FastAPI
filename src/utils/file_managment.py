from typing import List
import os

def get_files()-> List[str]:
        modules = {}
        code_tree=[]

        for root,_,files in os.walk("github") : 
            for file in files : 
                if file.endswith(".py") or file.endswith(".txt"):
                    file_path:str=os.path.join(root,file)
                    module_name = os.path.dirname(file_path) or 'root'  
                    if module_name not in modules:
                        modules[module_name] = []
                    modules[module_name].append(os.path.basename(file_path))
        
        for module, files in modules.items():
            code_tree.append({
                "module": module,
                "files": files
            })
        
        return code_tree

def delete_repo()->None:
        try:
            os.system(f"rm -rf github")
            print("Repository deleted successfully.")
                
        except Exception as e:
            print(f"Error deleting repository: {e}")