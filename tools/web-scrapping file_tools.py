from langchain.tools import tool

class FileTools:

    @tool("Write File with content")
    def write_file(self, data):
        """
        Write a file to a given path with the provided content.
        
        The input to this tool should be a pipe (|) separated text of length two, 
        representing the full path of the file, including the /workdir/template, 
        and the React Component code content you want to write to it.
        
        For example, `./Keynote/src/components/Hero.jsx|REACT_COMPONENT_CODE_PLACEHOLDER`.
        Replace REACT_COMPONENT_CODE_PLACEHOLDER with the actual code you want to write to the file.
        """
        try:
            path, content = data.split("|", 1)  # Split into exactly two parts
            path = path.strip().replace("\n", "").replace(" ", "").replace("`", "")
            
            if not path.startswith("./workdir"):
                path = f"./workdir/{path}"
                
            with open(path, "w") as f:
                f.write(content)
                
            return f"File written to {path}."
        
        except ValueError:
            return "Error: Input should be a pipe-separated string with exactly two parts."
        
        except Exception as e:
            return f"An error occurred: {e}"

