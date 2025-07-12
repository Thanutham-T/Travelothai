from datetime import datetime
from typing import Optional
from pydantic import BaseModel, config

# TicketType schema
class TicketTypeBase(BaseModel):
    name: str

class TicketTypeCreate(TicketTypeBase):
    pass

class TicketTypeUpdate(TicketTypeBase):
    pass

class TicketType(TicketTypeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = config.ConfigDict(from_attributes=True)

# TicketUsageRule schema
class TicketUsageRuleBase(BaseModel):
    ticket_type_id: int
    category_id: int
    allowance: bool
    tax_reduction: float

class TicketUsageRuleCreate(TicketUsageRuleBase):
    pass

class TicketUsageRuleUpdate(TicketUsageRuleBase):
    ticket_type_id: Optional[int] = None
    category_id: Optional[int] = None
    allowance: Optional[bool] = None
    tax_reduction: Optional[float] = None

class TicketUsageRule(TicketUsageRuleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = config.ConfigDict(from_attributes=True)

# Ticket schema
class TicketBase(BaseModel):
    user_id: Optional[int] = None
    ticket_type_id: int
    campaign_id: Optional[int] = None
    amount: int
    used: int = 0
    expires_at: datetime

class TicketCreate(TicketBase):
    pass

class TicketUpdate(TicketBase):
    user_id: Optional[int] = None
    ticket_type_id: Optional[int] = None
    campaign_id: Optional[int] = None
    amount: Optional[int] = None
    used: Optional[int] = None
    expiration_date: Optional[datetime] = None

class Ticket(TicketBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = config.ConfigDict(from_attributes=True)

# TicketCampaign schema
class TicketCampaignBase(BaseModel):
    name: str
    limit: int
    registered: int = 0
    is_active: bool
    start_date: datetime
    end_date: datetime

class TicketCampaignCreate(TicketCampaignBase):
    pass

class TicketCampaignUpdate(TicketCampaignBase):
    name: Optional[str] = None
    limit: Optional[int] = None
    registered: Optional[int] = None
    is_active: Optional[bool] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class TicketCampaign(TicketCampaignBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = config.ConfigDict(from_attributes=True)

# TicketCampaignTicketType schema
class TicketCampaignTicketTypeBase(BaseModel):
    campaign_id: int
    ticket_type_id: int
    amount: int
    expiration_date: datetime

class TicketCampaignTicketTypeCreate(TicketCampaignTicketTypeBase):
    pass

class TicketCampaignTicketTypeUpdate(TicketCampaignTicketTypeBase):
    campaign_id: Optional[int] = None
    ticket_type_id: Optional[int] = None
    amount: Optional[int] = None
    expiration_date: Optional[datetime] = None

class TicketCampaignTicketType(TicketCampaignTicketTypeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = config.ConfigDict(from_attributes=True)
