import os
from dotenv import load_dotenv
from vocode.streaming.telephony.conversation.outbound_call import OutboundCall
from vocode.streaming.telephony.config_manager.redis_config_manager import (
    RedisConfigManager,
)
from vocode.streaming.models.synthesizer import ElevenLabsSynthesizerConfig
from vocode.streaming.models.synthesizer import AzureSynthesizerConfig
from vocode.streaming.synthesizer.azure_synthesizer import AzureSynthesizer
from vocode.streaming.models.transcriber import AzureTranscriberConfig, PunctuationEndpointingConfig
from vocode.streaming.models.agent import ChatGPTAgentConfig
from vocode.streaming.models.message import BaseMessage

load_dotenv()

BASE_URL = os.environ["BASE_URL"]


async def main():
    config_manager = RedisConfigManager()

    outbound_call = OutboundCall(
        base_url=BASE_URL,
        #to_phone="+972542347471",
        to_phone="+972505817223",
        #to_phone="+14168717173",
        #to_phone="+27764169128",
        #to_phone="+14103775563",
        from_phone="+12898074196",
        mobile_only=False,
        transcriber_config=AzureTranscriberConfig.from_telephone_input_device(endpointing_config=PunctuationEndpointingConfig(), candidate_languages=['he-IL']),
        config_manager=config_manager,
        agent_config=ChatGPTAgentConfig(
                initial_message=BaseMessage(text="שלום, אני סוכנת חכמה, אשמח לעזור לך בניהול השוטף של העסק, בניתוב שיחות, ובשלל משימות נוספות"),
                prompt_preamble="את סוכנת חכמה מבוססת קול, תשתדלי למכור את עצמך לעסק, המטרה שלך היא לסגור עסקה עם הלקוח (כנראה עסק) שמדבר איתך, תעני תשובות קצרות, אין להשתמש בסימנים מיוחדים, רק אותיות וסימני פיסוק",
                generate_responses=True,
                model_name="gpt-4o",
                actions=[]
            ),
        synthesizer_config=AzureSynthesizerConfig.from_telephone_output_device(language_code='he-IL', voice_name='he-IL-HilaNeural')
    )

    input("Press enter to start call...")
    await outbound_call.start()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
