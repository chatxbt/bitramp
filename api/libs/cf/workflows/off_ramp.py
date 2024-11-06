from api.libs.cf.main import ControlFlow
cf = (ControlFlow(model="anthropic/claude-3-5-sonnet-20240620")).init()


@cf.flow
def handle_off_ramping(text: str):
    # Create a parent task to represent the entire analysis
    with cf.Task(
            """
            handle this off ramping request, here is how off ramping works:
            Receive crypto and make instant local currency transfers to your customers.
            Our Offramp API allows your users to go from crypto to local currency instantly.
            We currenctly support Offramp with Bank transfer (NGN) and MoMo (GHS)
            Offramp with Bank transfer (NGN)
            """,
            # instructions="Include each subtask result in your result"
            #              "ask user for clarity and request for more info required to complete request",
            instructions="give transaction quote before actually performing transaction"
                         "ask user for clarity and request for more info required to complete request",
            result_type=dict,
            context={"text": text},
            interactive=True
    ) as parent_task:
        # Child task 1: resolve bank account
        resolve_bank_account = cf.Task(
            """
            Resolve destination bank account: 
            Use our resolve-bank-account reference to verify recepient bank account and return the account details
            """,
            result_type=list[str]
        )

        # Child task 2: get-current-rates (resolve_bank_account)
        get_current_rates = cf.Task(
            "Get rates: Use our get-current-rates reference to fetch offramp rates",
            result_type=str,
            # depends_on=[resolve_bank_account]
        )

        # Child task 3: create-payment (get_current_rates)
        create_payment = cf.Task(
            "Create your payment: Use our create-payment reference to create your payment.",
            result_type=str,
            depends_on=[get_current_rates, resolve_bank_account]
        )

    # Run the parent task, which will automatically run all child tasks
    result = parent_task.run()
    return result

