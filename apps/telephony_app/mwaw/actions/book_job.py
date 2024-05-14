from typing import Optional, Type
from pydantic.v1 import BaseModel, Field
import requests

from vocode.streaming.action.base_action import BaseAction
from vocode.streaming.models.actions import (
    ActionConfig,
    ActionInput,
    ActionOutput,
)


class BookJobConfig(ActionConfig, type="action_book_job"):
    base_url: str


class BookJobParameters(BaseModel):
    name: str = Field(..., description="Full customer name")
    email: str = Field(..., description="Provided emails in json array format"),
    phone: str = Field(..., description="Provided phone numbers in json array format"),
    appliance: str = Field(..., description="Name of the appliance"),
    appliance_type: str = Field(...,
                                description="Either gas or electric, if not mentioned, default should be electric"),
    location: str = Field(..., description="Address of the job location with postal code"),
    description: str = Field(...,
                             description="Description of the problem that needs repair along with appliance model, "
                                         "sticker information and all other relevant info"),
    date: str = Field(..., description="date on which the repair job is to be booked in YYYY-MM-DD format"),
    timeslot: str = Field(..., description="Timeslot of the repair job to be booked. Its either 8am to 2pm or 12pm to "
                                           "6pm"),


class BookJobResponse(BaseModel):
    success: str


class BookJob(
    BaseAction[
        BookJobConfig, BookJobParameters, BookJobResponse
    ]
):
    description: str = "Book appliance repair job"
    parameters_type: Type[BookJobParameters] = BookJobParameters
    response_type: Type[BookJobResponse] = BookJobResponse

    async def run(
            self, action_input: ActionInput[BookJobParameters]
    ) -> ActionOutput[BookJobResponse]:

        response = requests.get(self.action_config.base_url + '/api/bookings/availableDates',
                                params=action_input.params,
                                headers={'Accept': 'application/json'}).json()

        if response['message'] == 'success':
            return_val = 'The job has been booked successfully'
        else:
            return_val = 'Failed to book the job.'

        return ActionOutput(
            action_type=self.action_config.type,
            response=BookJobResponse(success=return_val),
        )
