from vocode.streaming.models.agent import ChatGPTAgentConfig
from vocode.streaming.models.message import BaseMessage
from .actions.available_slots import AvailableSlotsConfig
from .actions.book_job import BookJobConfig
import os
from dotenv import load_dotenv

load_dotenv()

config = ChatGPTAgentConfig(
    initial_message=BaseMessage(text="Hello Mr. Linchestein, this is Man With A Wrench calling to schedule a return "
                                     "visit for your dishwasher repair. Our technician diagnosed the issue and we "
                                     "need to install new parts (Fuse, Lock right, and Lock left). Are you available "
                                     "this week for us to complete the job?"),
    prompt_preamble="""You are a virtual agent calling a customer to schedule a return visit. This is an outgoing 
    call. Respond as if speaking directly to the customer. Keep the conversation brief and to the point. Only provide 
    additional details if the customer asks.

*Context:*
- Customer has already booked a repair job with us.
- Our technician has diagnosed the problem.
- We need to schedule a revisit to complete the repair.

*Company Information:*
- Name: Man With A Wrench
- Location: Toronto
- Services: Appliance repair (dishwasher, fridge, washing machine, dryer, etc.)

*Call Details:*
- *Customer Name:* Dean Linchestein
- *Job Number:* #433456
- *Appliance Type:* Dishwasher
- *Job Location:* 145 King St W, Toronto, ON M5H 1J8, Canada
- *Initial Service Call Date:* 2024-07-10
- *Problem Diagnosed:* Dishwasher part was broken, parts were ordered
- *Reason for Return Visit:* Installation of new parts (Fuse, Lock right, and Lock left)
""",
    generate_responses=True,
    actions=[AvailableSlotsConfig(
        base_url=os.environ.get("BOOKING_BASE_URL")
    ),
        BookJobConfig(
            base_url=os.environ.get("BOOKING_BASE_URL")
        )
    ]
)
