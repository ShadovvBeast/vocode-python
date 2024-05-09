from vocode.streaming.agent.factory import AgentFactory
import logging
from typing import Optional
from vocode.streaming.agent.base_agent import BaseAgent
from vocode.streaming.agent.chat_gpt_agent import ChatGPTAgent
from vocode.streaming.models.agent import (
    AgentConfig,
    ChatGPTAgentConfig,
)

from actions.factory import MwawActionFactory


class MwawAgentFactory(AgentFactory):
    def create_agent(
            self, agent_config: AgentConfig, logger: Optional[logging.Logger] = None
    ) -> BaseAgent:
        if isinstance(agent_config, ChatGPTAgentConfig):
            return ChatGPTAgent(agent_config=agent_config, logger=logger, action_factory=MwawActionFactory())
        raise Exception("Invalid agent config", agent_config.type)
