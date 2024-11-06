from api.libs.cf.main import ControlFlow, cf_default_tools
from api.libs.cf.workflows.off_ramp import handle_off_ramping
cf = (ControlFlow(model="anthropic/claude-3-5-sonnet-20240620")).init()

# Create agents
classifier = cf.Agent(
    name="Request Classifier",
    instructions="You are a financial expert at quickly understanding and classifying messages. Always "
                 "respond with exactly one word: either 'off-ramp' or 'simple-task'."
)

web3_expert = cf.Agent(
    name="web3 expert",
    tools=cf_default_tools,
    instructions="You are a financial expert equipped with tools good at handling simple web3 tasks. "
                 "Your replies should be concise but friendly."
)


# Create the flow
@cf.flow
def process_request(content: str):

    # Classify the message
    category = cf.run(
        f"Classify this message",
        result_type=["off-ramp", "simple-task"],
        agents=[classifier],
        context=dict(message=content),
    )

    print(f"category: {category}")

    # If the email is important, write a response
    if category == "off-ramp":
        # response = cf.run(
        #     f"Write a response to this important message",
        #     result_type=str,
        #     agents=[responder],
        #     context=dict(email=content),
        # )
        response = handle_off_ramping(content)
        return response

    # Otherwise, give casual response
    else:
        response = cf.run(
            "You are a financial expert, good at handling simple web3 tasks. "
            "Your replies should be concise but friendly.",
            result_type=str,
            # agents=[web3_expert],
            context=dict(message=content),
        )
        return response
