import logging
# Set up logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


from smolagents import CodeAgent, LiteLLMModel

import litellm, os
from dotenv import load_dotenv
load_dotenv(override=True)

from scripts.visual_qa import visualizer
from scripts.text_inspector_tool import TextInspectorTool
from scripts.text_web_browser import (
    ArchiveSearchTool, FinderTool, FindNextTool, PageDownTool, PageUpTool, SimpleTextBrowser, VisitTool
)
from smolagents import CodeAgent, LiteLLMModel, ToolCallingAgent, DuckDuckGoSearchTool
# Enable verbose mode for debugging
# litellm.set_verbose = True
# os.environ['LITELLM_LOG'] = 'DEBUG'


AUTHORIZED_IMPORTS = [
    "requests",
    "zipfile",
    "os",
    "pandas",
    "numpy",
    "sympy",
    "json",
    "bs4",
    "pubchempy",
    "xml",
    "yahoo_finance",
    "Bio",
    "sklearn",
    "scipy",
    "pydub",
    "io",
    "PIL",
    "chess",
    "PyPDF2",
    "pptx",
    "torch",
    "datetime",
    "fractions",
    "csv",
]
load_dotenv(override=True)

custom_role_conversions = {"tool-call": "assistant", "tool-response": "user"}

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"


BROWSER_CONFIG = {
    "viewport_size": 1024 * 5,
    "downloads_folder": "downloads_folder",
    "request_kwargs": {
        "headers": {"User-Agent": user_agent},
        "timeout": 300,
    },
    "serpapi_key": os.getenv("SERPAPI_API_KEY"),
}

browser = SimpleTextBrowser(**BROWSER_CONFIG)

os.makedirs(f"./{BROWSER_CONFIG['downloads_folder']}", exist_ok=True)




MODEL_LIST = [
    "deepseek/deepseek-chat",
    "deepseek/deepseek-reasoner",
]


for model_name in MODEL_LIST:

    print(f"\n\n{50*'~'} \nRunning {model_name} \n {50*'~'}\n")
    model = LiteLLMModel(
        model_name,
        # custom_role_conversions=custom_role_conversions,
        max_completion_tokens=8192,
        reasoning_effort="high",
        drop_params = True,
        fix_user_message=True
    )
    text_limit = 20000
    WEB_TOOLS = [
        # GoogleSearchTool(),
        DuckDuckGoSearchTool(),
        VisitTool(browser),
        PageUpTool(browser),
        PageDownTool(browser),
        FinderTool(browser),
        FindNextTool(browser),
        ArchiveSearchTool(browser),
        TextInspectorTool(model, text_limit),
    ]
    # Create a basic agent
    agent = CodeAgent(
        model=model,
        tools=[visualizer, TextInspectorTool(model, text_limit)],
        add_base_tools=True,
        max_steps=12,
        verbosity_level=10,
        additional_authorized_imports=AUTHORIZED_IMPORTS,
        planning_interval=4,
    )

    # Run the agent with a simple task
    result = agent.run("Get the weather in Bangalore")
    print(result) 
