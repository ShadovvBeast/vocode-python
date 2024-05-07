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

# Local application/library specific imports
from speller_agent import (
    SpellerAgentFactory,
    SpellerAgentConfig,
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
                prompt_preamble="Act as a professional and courteous customer service agent for an appliance repair company. Your primary tasks include booking and rescheduling appointments for customers, providing status updates on current service jobs, and offering any relevant information or advice. You will handle each inquiry with empathy and precision, ensuring the customer feels supported throughout their interaction. If a customer asks a question or requests assistance that requires specialized knowledge, provide clear instructions on the next steps they can take or guide them to the appropriate resources",
                generate_responses=True,
            ),
            # uncomment this to use the speller agent instead
            # agent_config=SpellerAgentConfig(
            #     initial_message=BaseMessage(text="im a speller agent, say something to me and ill spell it out for you"),
            #     generate_responses=False,
            # ),
            synthesizer_config=ElevenLabsSynthesizerConfig.from_telephone_output_device(
                        api_key=os.getenv("ELEVEN_LABS_API_KEY"),
                        voice_id="3gsg3cxXyFLcGIfNbM6C"
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
