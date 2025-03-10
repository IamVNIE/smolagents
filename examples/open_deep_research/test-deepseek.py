from smolagents import CodeAgent, LiteLLMModel
import litellm

# Enable verbose mode for debugging
litellm.set_verbose = True

# Initialize the model
# model = LiteLLMModel("deepseek/deepseek-chat")
model = LiteLLMModel("deepseek/deepseek-reasoner")

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
