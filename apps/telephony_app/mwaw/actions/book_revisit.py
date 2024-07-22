from typing import Optional, Type
from pydantic.v1 import BaseModel, Field
import requests

from vocode.streaming.action.base_action import BaseAction
from vocode.streaming.models.actions import (
    ActionConfig,
    ActionInput,
    ActionOutput,
)


class BookRevisitConfig(ActionConfig, type="action_book_revisit"):
    base_url: str


class BookRevisitParameters(BaseModel):
    date: str = Field(..., description="date on which the revisit is to be booked in YYYY-MM-DD format")
    timeslot: str = Field(..., description="Timeslot of the revisit to be booked. Its either 8am to 2pm or 12pm to 6pm")


class BookJobResponse(BaseModel):
    success: str


class BookRevisit(
    BaseAction[
        BookRevisitConfig, BookRevisitParameters, BookJobResponse
    ]
):
    description: str = "Book appliance repair job"
    parameters_type: Type[BookRevisitParameters] = BookRevisitParameters
    response_type: Type[BookJobResponse] = BookJobResponse

    async def run(
            self, action_input: ActionInput[BookRevisitParameters]
    ) -> ActionOutput[BookJobResponse]:
        #
        # response = requests.post(self.action_config.base_url + '/api/bookings/virtualAgentBook',
        #                          data=action_input.params.dict(),
        #                          headers={'Accept': 'application/json'}).json()

        # print('booked job response', response)
        # if response['message'] == 'success':
        return_val = 'The revisit has been booked successfully'
        # else:
        #     return_val = 'Failed to book the job.'

        return ActionOutput(
            action_type=self.action_config.type,
            response=BookJobResponse(success=return_val),
        )
