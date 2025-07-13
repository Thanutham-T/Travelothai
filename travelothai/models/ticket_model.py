from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .province_model import ProvinceCategory
    from .booking_model import Booking

# TicketType schema
class TicketTypeBase(SQLModel):
    name: str = Field(index=True, unique=True)

class TicketType(TicketTypeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    tickets: List["Ticket"] = Relationship(back_populates="ticket_type")
    campaigns: List["TicketCampaignTicketType"] = Relationship(back_populates="ticket_type")
    usage_rules: List["TicketUsageRule"] = Relationship(back_populates="ticket_type")


# TicketUsageRule schema
class TicketUsageRuleBase(SQLModel):
    ticket_type_id: int = Field(foreign_key="tickettype.id")
    category_id: int = Field(foreign_key="provincecategory.id")
    allowance: bool = Field(default=False)
    tax_reduction: float = Field(default=0.0)

class TicketUsageRule(TicketUsageRuleBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    ticket_type: Optional["TicketType"] = Relationship(back_populates="usage_rules")
    province_category: Optional["ProvinceCategory"] = Relationship(back_populates="usage_rules")


# Ticket schema
class TicketBase(SQLModel):
    # user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user_id: int = Field(default=None)
    ticket_type_id: int = Field(foreign_key="tickettype.id")
    campaign_id: Optional[int] = Field(default=None, foreign_key="ticketcampaign.id")
    amount: int = Field(gt=0)
    used: int = Field(default=0)
    expires_at: datetime = Field(default=None)

class Ticket(TicketBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    ticket_type: Optional["TicketType"] = Relationship(back_populates="tickets")
    campaign: Optional["TicketCampaign"] = Relationship(back_populates="tickets")
    bookings: List["Booking"] = Relationship(back_populates="ticket")


# TicketCampaign schema
class TicketCampaignBase(SQLModel):
    name: str = Field(index=True, unique=True)
    limit: int = Field(gt=0)
    registered: int = Field(default=0)
    is_active: bool = Field(default=True)
    start_date: datetime = Field(default_factory=datetime.now)
    end_date: datetime = Field(default_factory=datetime.now)

class TicketCampaign(TicketCampaignBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    tickets: List["Ticket"] = Relationship(back_populates="campaign")
    ticket_types: List["TicketCampaignTicketType"] = Relationship(back_populates="campaign")


# TicketCampaignTicketType schema
class TicketCampaignTicketTypeBase(SQLModel):
    campaign_id: int = Field(foreign_key="ticketcampaign.id")
    ticket_type_id: int = Field(foreign_key="tickettype.id")
    amount: int = Field(gt=0)
    expiration_date: datetime = Field(default_factory=datetime.now)

class TicketCampaignTicketType(TicketCampaignTicketTypeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    campaign: Optional["TicketCampaign"] = Relationship(back_populates="ticket_types")
    ticket_type: Optional["TicketType"] = Relationship(back_populates="campaigns")
