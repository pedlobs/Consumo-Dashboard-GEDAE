from __future__ import annotations

import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

# "UC" stands for the Brazilian utility term "Unidade Consumidora"
# (Consumer Unit), the standard identifier used by ANEEL/utilities for
# a single metered point of consumption.
_ANONYMIZED_ID_PATTERN = re.compile(r"^UC-\d{2,}$")


class ConsumptionReading(BaseModel):
    """A single electricity consumption reading, in "long" format.

    This is the system's validation boundary. 

    Parameters

    timestamp : datetime
        Date and time of the reading.
    consumer_unit : str
        Identifier of the metering point
    consumption_kwh : float
        Energy consumed over the period, in kWh. 
    """

    model_config = ConfigDict(str_strip_whitespace=True)

    timestamp: datetime
    consumer_unit: str = Field(min_length=1)
    consumption_kwh: float = Field(
        ge=0, description="Consumption in kWh"
    )

    @field_validator("consumer_unit")
    @classmethod
    def _require_anonymized_identifier(cls, value: str) -> str:
        """Reject any value that does not follow the expected anonymized format.
        
        Raises ValueError if ``value`` does not match ``^UC-\\d{2,}$``.
        """
        if not _ANONYMIZED_ID_PATTERN.match(value):
            raise ValueError(
                f"'{value}' is not a valid anonymized identifier "
                "(expected the 'UC-NN' format). This usually means a "
                "real identifier is trying to enter the system without "
                "going through ConsumerUnitAnonymizer."
            )
        return value
