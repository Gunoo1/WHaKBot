import os
from decouple import config
from datetime import date

def set_environment_variables(project_name: str = "") -> None:
    if not project_name:
        project_name = f"Test_{date.today()}"

    os.environ["ANTHROPIC_API_KEY"] = str(config("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",
                                                 default="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"))
    os.environ["OPENAI_API_KEY"] = str(config("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",
                                              default="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"))
    os.environ["LANGCHAIN_API_KEY"] = str(config("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",
                                                 default="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"))
    os.environ["LANGCHAIN_PROJECT"] = project_name
    os.environ['TAVILY_API_KEY'] = str(
        config("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", default="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"))


    print("API KEYS LOAED AND TRACING SET WITH PROJECT NAME", project_name)