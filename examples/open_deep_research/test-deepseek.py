from smolagents import CodeAgent, LiteLLMModel
import litellm, os
from dotenv import load_dotenv
load_dotenv(override=True)


# Enable verbose mode for debugging
litellm.set_verbose = True
# os.environ['LITELLM_LOG'] = 'DEBUG'


MODEL_LIST = [
    "deepseek/deepseek-chat",
    "deepseek/deepseek-reasoner",
]


for model_name in MODEL_LIST:

    print(f"\n\n{50*'~'} \nRunning {model_name} \n {50*'~'}\n")
    model = LiteLLMModel(model_name)

    # Create a basic agent
    agent = CodeAgent(
        tools=[],
        model=model,
        add_base_tools=True,
        verbosity_level=2
    )

    # Run the agent with a simple task
    result = agent.run("Get the weather in Dublin")
    print(result) 
