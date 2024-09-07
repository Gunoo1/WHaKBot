import os
from decouple import config
from datetime import date

def set_environment_variables(project_name: str = "") -> None:
    if not project_name:
        project_name = f"Test_{date.today()}"

    os.environ["ANTHROPIC_API_KEY"] = str(config("API-KEY",
                                                 default="API-KEY"))
    os.environ["OPENAI_API_KEY"] = str(config("API-KEY",
                                              default="API-KEY"))
    os.environ["LANGCHAIN_API_KEY"] = str(config("API-KEY",
                                                 default="API-KEY"))
    os.environ["LANGCHAIN_PROJECT"] = project_name
    os.environ['TAVILY_API_KEY'] = str(
        config("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", default="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"))


    print("API KEYS LOAED AND TRACING SET WITH PROJECT NAME", project_name)
