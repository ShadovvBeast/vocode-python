import os
from dotenv import load_dotenv
from vocode.streaming.telephony.conversation.outbound_call import OutboundCall
from vocode.streaming.telephony.config_manager.redis_config_manager import (
    RedisConfigManager,
)
from vocode.streaming.models.synthesizer import ElevenLabsSynthesizerConfig

from vocode.streaming.models.agent import ChatGPTAgentConfig
from vocode.streaming.models.message import BaseMessage

load_dotenv()

BASE_URL = os.environ["BASE_URL"]


async def main():
    config_manager = RedisConfigManager()

    outbound_call = OutboundCall(
        base_url=BASE_URL,
        to_phone="+14168717173",
        from_phone="+12898074196",
        mobile_only=False,
        config_manager=config_manager,
        agent_config=ChatGPTAgentConfig(
                initial_message=BaseMessage(text="Hello, I am a virtual Infinity Engager sales representative"),
                prompt_preamble="Act as a professional and courteous sales representative agent for Infinity Engager, a product that helps you engage with your audience on social media by replying to comments. Each comment only costs 1 cent, use that as a selling point. Your goal is to make a deal and help the user register. They can look up Infinity Engager on Google to get to the website and get 1000 free tokens to test out the product",
                generate_responses=True,
            ),
        synthesizer_config=ElevenLabsSynthesizerConfig.from_telephone_output_device(
                        api_key=os.getenv("ELEVEN_LABS_API_KEY"))
    )

    input("Press enter to start call...")
    await outbound_call.start()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
