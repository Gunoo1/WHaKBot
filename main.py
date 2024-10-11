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