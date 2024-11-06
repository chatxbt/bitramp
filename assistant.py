from api.libs.cf.main import ControlFlow
from api.libs.cf.workflows.main_flow import process_request
cf = (ControlFlow(model="anthropic/claude-3-5-sonnet-20240620")).init()

# Create a ControlFlow task to generate an reply
# reply = cf.run(
#     "get me the rate of BTC in naira",
#     # context=dict(email=emails[0]),
# )

reply = process_request("i want to exchange my btc to naira")

# 2174344023
# 033
# 0.0005 btc, email: kingsleyonyeneke@gmail.com, bank account number: 2174344023, bank code 033

print(f" final output: {reply}")
