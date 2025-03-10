from run import create_agent

from smolagents.gradio_ui import GradioUI


agent = create_agent(
    # model_id="deepseek/deepseek-chat",
    model_id="deepseek/deepseek-reasoner",
    # model_id="together_ai/deepseek-ai/DeepSeek-V3",
    # model_id="bedrock/us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    )

demo = GradioUI(agent)

if __name__ == "__main__":
    demo.launch()
