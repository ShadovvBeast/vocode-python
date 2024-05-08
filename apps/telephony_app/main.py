# Standard library imports
import logging
import os
import sys

# Third-party imports
from fastapi import FastAPI
from vocode.streaming.models.telephony import TwilioConfig
from pyngrok import ngrok
from vocode.streaming.telephony.config_manager.redis_config_manager import (
    RedisConfigManager,
)
from vocode.streaming.models.agent import ChatGPTAgentConfig
from vocode.streaming.models.message import BaseMessage
from vocode.streaming.telephony.server.base import (
    TwilioInboundCallConfig,
    TelephonyServer,
)
from dotenv import load_dotenv
from vocode.streaming.models.synthesizer import ElevenLabsSynthesizerConfig
from action.available_slots import AvailableSlotsActionConfig
# Local application/library specific imports
from speller_agent import (
    SpellerAgentFactory,
)

# if running from python, this will load the local .env
# docker-compose will load the .env file by itself
load_dotenv()

app = FastAPI(docs_url=None)

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

config_manager = RedisConfigManager(
    logger=logger,
)

BASE_URL = os.getenv("BASE_URL")

if not BASE_URL:
    ngrok_auth = os.environ.get("NGROK_AUTH_TOKEN")
    if ngrok_auth is not None:
        ngrok.set_auth_token(ngrok_auth)
    port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else 3000

    # Open a ngrok tunnel to the dev server
    BASE_URL = ngrok.connect(port).public_url.replace("https://", "")
    logger.info('ngrok tunnel "{}" -> "http://127.0.0.1:{}"'.format(BASE_URL, port))

if not BASE_URL:
    raise ValueError("BASE_URL must be set in environment if not using pyngrok")

telephony_server = TelephonyServer(
    base_url=BASE_URL,
    config_manager=config_manager,
    inbound_call_configs=[
        TwilioInboundCallConfig(
            url="/inbound_call",
            agent_config=ChatGPTAgentConfig(
                initial_message=BaseMessage(text="Hello, I am a Man with a wrench virtual agent"),
                prompt_preamble="""Act as a professional and courteous customer service agent for an appliance repair
                 company. Your primary tasks include booking and rescheduling appointments for customers, 
                 providing status updates on current service jobs, and offering any relevant information or advice. 
                 You will handle each inquiry with empathy and precision, ensuring the customer feels supported 
                 throughout their interaction. If a customer asks a question or requests assistance that requires 
                 specialized knowledge, provide clear instructions on the next steps they can take or guide them 
                 to the appropriate resources.
                 For booking a repair appointment, here are the steps:
                 
                 1. First ask what type of appliance needs repair. 
                 2. If appliance is dryer or stove ask whether its electric or gas, otherwise no need to ask.
                 3. Ask the postal code of the repair job location. 
                 4. Call action_available_slots function to get the available slots for booking an appliance repair job. 
                 5. Tell customer we provide two timeslots 8am to 2pm and 12pm to 6pm. Suggest first 3 dates of
                 the available slots.For example if 8am to 2pm slots are available in 1st,2nd,3rd, 
                 then say 8am to 2pm slots are available for 1st,2nd and 3rd of 2024. Same for 12pm to 6pm.
                 If customer chosen date are not available, suggest another date close to 
                 the date customer selected. Do not tell the whole available slots. 
                 6. Ask additional details for booking such as customer first and last name, address, email, alternative 
                 phone numbers if any, short description of the problem, appliance model and sticker 
                 information if any. Ask them these questions one by one. After getting all the relevant details, tell 
                 them that they will get a confirmation email after all the details are verified.
                 7. After all the information are available, call the book tool to book the customer repair job.
                 """,
                generate_responses=True,
                actions=[AvailableSlotsActionConfig(
                    base_url=os.environ.get("BOOKING_BASE_URL")
                )]
            ),
            # uncomment this to use the speller agent instead
            # agent_config=SpellerAgentConfig(
            #     initial_message=BaseMessage(text="im a speller agent, say something to me and ill spell it out for you"),
            #     generate_responses=False,
            # ),
            synthesizer_config=ElevenLabsSynthesizerConfig.from_telephone_output_device(
                api_key=os.getenv("ELEVEN_LABS_API_KEY"),
                voice_id="XrExE9yKIg1WjnnlVkGX"
            ),
            twilio_config=TwilioConfig(
                account_sid=os.environ["TWILIO_ACCOUNT_SID"],
                auth_token=os.environ["TWILIO_AUTH_TOKEN"],
            ),
        )
    ],
    agent_factory=SpellerAgentFactory(),
    logger=logger,
)

app.include_router(telephony_server.get_router())
