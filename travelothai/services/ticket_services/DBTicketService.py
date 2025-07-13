from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException

from .TicketServiceInterface import TicketServiceInterface
from travelothai.schemas import ticket_schema
from travelothai.models import ticket_model

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class DBTicketService(TicketServiceInterface):
    def __init__(self, session: AsyncSession):
        self.session = session


    # TicketType Methods
    async def list_ticket_types(self) -> List[ticket_schema.TicketType]:
        result = await self.session.exec(select(ticket_model.TicketType))
        if not result:
            raise HTTPException(status_code=404, detail="No ticket types found")
        ticket_types = result.scalars().all()
        return ticket_types

    async def get_ticket_type(self, type_id: int) -> Optional[ticket_schema.TicketType]:
        result = await self.session.exec(select(ticket_model.TicketType).where(ticket_model.TicketType.id == type_id))
        if not result:
            raise HTTPException(status_code=404, detail="Ticket type not found")
        return result.scalar_one_or_none()

    async def create_ticket_type(self, type: ticket_schema.TicketTypeCreate) -> ticket_schema.TicketType:
        # Validate the name not empty and unique
        if not type.name:
            raise HTTPException(status_code=400, detail="Ticket type name is required")
        result = await self.session.exec(select(ticket_model.TicketType).where(ticket_model.TicketType.name == type.name))
        if result.first():
            raise HTTPException(status_code=400, detail="Ticket type name must be unique")

        # Create the TicketType
        ticket_type = ticket_model.TicketType.model_validate(type)
        self.session.add(ticket_type)
        await self.session.commit()
        await self.session.refresh(ticket_type)
        return ticket_type


    async def update_ticket_type(self, type_id: int, type: ticket_schema.TicketTypeUpdate) -> Optional[ticket_schema.TicketType]:
        # Validate the name not empty and unique
        if not type.name:
            raise HTTPException(status_code=400, detail="Ticket type name is required")
        result = await self.session.exec(select(ticket_model.TicketType).where(ticket_model.TicketType.name == type.name))
        if result.first():
            raise HTTPException(status_code=400, detail="Ticket type name must be unique")
        ticket_type = await self.get_ticket_type(type_id)
        if not ticket_type:
            raise HTTPException(status_code=404, detail="Ticket type not found")

        # Update the TicketType
        for key, value in type.model_dump(exclude_unset=True).items():
            setattr(ticket_type, key, value)
        self.session.add(ticket_type)
        await self.session.commit()
        await self.session.refresh(ticket_type)
        return ticket_type
    
    
    async def delete_ticket_type(self, type_id: int) -> None:
        ticket_type = await self.get_ticket_type(type_id)
        if not ticket_type:
            raise HTTPException(status_code=404, detail="Ticket type not found")
        await self.session.delete(ticket_type)
        await self.session.commit()
        return ticket_type


    # TicketUsageRules Methods
    async def list_ticket_usage_rules(self) -> List[ticket_schema.TicketUsageRule]:
        result = await self.session.exec(select(ticket_model.TicketUsageRule))
        if not result:
            raise HTTPException(status_code=404, detail="No ticket usage rules found")
        ticket_usage_rules = result.scalars().all()
        return ticket_usage_rules

    async def get_ticket_usage_rule(self, rule_id: int) -> Optional[ticket_schema.TicketUsageRule]:
        result = await self.session.exec(select(ticket_model.TicketUsageRule).where(ticket_model.TicketUsageRule.id == rule_id))
        if not result:
            raise HTTPException(status_code=404, detail="Ticket usage rule not found")
        return result.scalar_one_or_none()

    async def create_ticket_usage_rule(self, rule: ticket_schema.TicketUsageRuleCreate) -> ticket_schema.TicketUsageRule:
        # Validate the ticket_type_id and category_id exist
        result = await self.session.exec(select(ticket_model.TicketType).where(ticket_model.TicketType.id == rule.ticket_type_id))
        if not result.first():
            raise HTTPException(status_code=404, detail="Ticket type not found")
        result = await self.session.exec(select(ticket_model.TicketType).where(ticket_model.TicketType.id == rule.category_id))
        if not result.first():
            raise HTTPException(status_code=404, detail="Category not found")

        # Create the TicketUsageRule
        ticket_usage_rule = ticket_model.TicketUsageRule.model_validate(rule)
        self.session.add(ticket_usage_rule)
        await self.session.commit()
        await self.session.refresh(ticket_usage_rule)
        return ticket_usage_rule
    

    async def update_ticket_usage_rule(self, rule_id: int, rule: ticket_schema.TicketUsageRuleUpdate) -> Optional[ticket_schema.TicketUsageRule]:
        # Validate the ticket_id and ticket_type_id not empty and exist
        ticket_usage_rule = await self.get_ticket_usage_rule(rule_id)
        if not ticket_usage_rule:
            raise HTTPException(status_code=404, detail="Ticket usage rule not found")
        if not rule.ticket_id:
            raise HTTPException(status_code=400, detail="Ticket ID must not be empty")
        result = await self.session.exec(select(ticket_model.TicketType).where(ticket_model.TicketType.id == rule.ticket_type_id))
        if not result.first():
            raise HTTPException(status_code=404, detail="Ticket type not found")

        # Update the TicketUsageRule
        for key, value in rule.model_dump(exclude_unset=True).items():
            setattr(ticket_usage_rule, key, value)
        self.session.add(ticket_usage_rule)
        await self.session.commit()
        await self.session.refresh(ticket_usage_rule)
        return ticket_usage_rule


    async def delete_ticket_usage_rule(self, rule_id: int) -> None:
        ticket_usage_rule = await self.get_ticket_usage_rule(rule_id)
        if not ticket_usage_rule:
            raise HTTPException(status_code=404, detail="Ticket usage rule not found")
        await self.session.delete(ticket_usage_rule)
        await self.session.commit()
        return ticket_usage_rule


    # Ticket Methods
    async def list_tickets(self) -> List[ticket_schema.Ticket]:
        result = await self.session.exec(select(ticket_model.Ticket))
        if not result:
            raise HTTPException(status_code=404, detail="No tickets found")
        tickets = result.scalars().all()
        return tickets

    async def get_ticket(self, ticket_id: int) -> Optional[ticket_schema.Ticket]:
        result = await self.session.exec(select(ticket_model.Ticket).where(ticket_model.Ticket.id == ticket_id))
        if not result:
            raise HTTPException(status_code=404, detail="Ticket not found")
        return result.scalar_one_or_none()

    async def create_ticket(self, ticket: ticket_schema.TicketCreate) -> ticket_schema.Ticket:
        # Validate the ticket_type_id exists
        result = await self.session.exec(select(ticket_model.TicketType).where(ticket_model.TicketType.id == ticket.ticket_type_id))
        if not result.first():
            raise HTTPException(status_code=404, detail="Ticket type not found")

        # Create the Ticket
        ticket = ticket_model.Ticket.model_validate(ticket)
        self.session.add(ticket)
        await self.session.commit()
        await self.session.refresh(ticket)
        return ticket
    
    
    async def update_ticket(self, ticket_id: int, ticket: ticket_schema.TicketUpdate) -> Optional[ticket_schema.Ticket]:
        # Validate ticket_id and the ticket_type_id not empty and exists
        if not ticket.ticket_type_id:
            raise HTTPException(status_code=400, detail="Ticket type ID must not be empty")
        result = await self.session.exec(select(ticket_model.TicketType).where(ticket_model.TicketType.id == ticket.ticket_type_id))
        if not result.first():
            raise HTTPException(status_code=404, detail="Ticket type not found")
        ticket = await self.get_ticket(ticket_id)
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")

        # Update the Ticket
        for key, value in ticket.model_dump(exclude_unset=True).items():
            setattr(ticket, key, value)
        self.session.add(ticket)
        await self.session.commit()
        await self.session.refresh(ticket)
        return ticket


    async def collect_ticket(self, ticket_id: int) -> Optional[ticket_schema.Ticket]:
        # Validate ticket_id
        ticket = await self.get_ticket(ticket_id)
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")

        # Update the Ticket's traveler information
        ticket.user_id = None
        self.session.add(ticket)
        await self.session.commit()
        await self.session.refresh(ticket)
        return ticket


    async def delete_ticket(self, ticket_id: int) -> None:
        ticket = await self.get_ticket(ticket_id)
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        await self.session.delete(ticket)
        await self.session.commit()
        return ticket


    # TicketCampaignTicketTypes Methods
    async def list_ticket_campaign_ticket_types(self) -> List[ticket_schema.TicketCampaignTicketType]:
        result = await self.session.exec(select(ticket_model.TicketCampaignTicketType))
        if not result:
            raise HTTPException(status_code=404, detail="No ticket campaign ticket types found")
        ticket_campaign_ticket_types = result.scalars().all()
        return ticket_campaign_ticket_types

    async def get_ticket_campaign_ticket_type(self, tctt_id: int) -> Optional[ticket_schema.TicketCampaignTicketType]:
        result = await self.session.exec(select(ticket_model.TicketCampaignTicketType).where(ticket_model.TicketCampaignTicketType.id == tctt_id))
        if not result:
            raise HTTPException(status_code=404, detail="Ticket campaign ticket type not found")
        return result.scalar_one_or_none()

    async def create_ticket_campaign_ticket_type(self, tctt: ticket_schema.TicketCampaignTicketTypeCreate) -> ticket_schema.TicketCampaignTicketType:
        # Validate the campaign_id and ticket_type_id not empty and exist
        if not tctt.campaign_id:
            raise HTTPException(status_code=400, detail="Campaign ID must not be empty")
        result = await self.session.exec(select(ticket_model.TicketCampaign).where(ticket_model.TicketCampaign.id == tctt.campaign_id))
        if not result.first():
            raise HTTPException(status_code=404, detail="Campaign not found")
        if not tctt.ticket_type_id:
            raise HTTPException(status_code=400, detail="Ticket type ID must not be empty")
        result = await self.session.exec(select(ticket_model.TicketType).where(ticket_model.TicketType.id == tctt.ticket_type_id))
        if not result.first():
            raise HTTPException(status_code=404, detail="Ticket type not found")

        ticket_campaign_ticket_type = ticket_model.TicketCampaignTicketType.model_validate(tctt)
        self.session.add(ticket_campaign_ticket_type)
        await self.session.commit()
        await self.session.refresh(ticket_campaign_ticket_type)
        return ticket_campaign_ticket_type

    async def update_ticket_campaign_ticket_type(self, tctt_id: int, tctt: ticket_schema.TicketCampaignTicketTypeUpdate) -> Optional[ticket_schema.TicketCampaignTicketType]:
        # Validate the campaign_id and ticket_type_id not empty and exist
        if not tctt.campaign_id:
            raise HTTPException(status_code=400, detail="Campaign ID must not be empty")
        result = await self.session.exec(select(ticket_model.TicketCampaign).where(ticket_model.TicketCampaign.id == tctt.campaign_id))
        if not result.first():
            raise HTTPException(status_code=404, detail="Campaign not found")
        if not tctt.ticket_type_id:
            raise HTTPException(status_code=400, detail="Ticket type ID must not be empty")
        result = await self.session.exec(select(ticket_model.TicketType).where(ticket_model.TicketType.id == tctt.ticket_type_id))
        if not result.first():
            raise HTTPException(status_code=404, detail="Ticket type not found")
        ticket_campaign_ticket_type = await self.get_ticket_campaign_ticket_type(tctt_id)
        if not ticket_campaign_ticket_type:
            raise HTTPException(status_code=404, detail="Ticket campaign ticket type not found")

        # Update the fields
        for key, value in tctt.model_dump(exclude_unset=True).items():
            setattr(ticket_campaign_ticket_type, key, value)
        self.session.add(ticket_campaign_ticket_type)
        await self.session.commit()
        await self.session.refresh(ticket_campaign_ticket_type)
        return ticket_campaign_ticket_type

    async def delete_ticket_campaign_ticket_type(self, tctt_id: int) -> None:
        ticket_campaign_ticket_type = await self.get_ticket_campaign_ticket_type(tctt_id)
        if not ticket_campaign_ticket_type:
            return None
        await self.session.delete(ticket_campaign_ticket_type)
        await self.session.commit()
        return ticket_campaign_ticket_type
    

    # TicketCampaign Methods
    async def list_ticket_campaigns(self) -> List[ticket_schema.TicketCampaign]:
        result = await self.session.exec(select(ticket_model.TicketCampaign))
        if not result:
            raise HTTPException(status_code=404, detail="No ticket campaigns found")
        ticket_campaigns = result.scalars().all()
        return ticket_campaigns

    async def get_ticket_campaign(self, campaign_id: int) -> Optional[ticket_schema.TicketCampaign]:
        result = await self.session.exec(select(ticket_model.TicketCampaign).where(ticket_model.TicketCampaign.id == campaign_id))
        if not result:
            raise HTTPException(status_code=404, detail="Campaign not found")
        return result.scalar_one_or_none()

    async def create_ticket_campaign(self, campaign: ticket_schema.TicketCampaignCreate) -> ticket_schema.TicketCampaign:
        # Validate the campaign name not empty and unique
        if not campaign.name:
            raise HTTPException(status_code=400, detail="Campaign name must not be empty")
        result = await self.session.exec(select(ticket_model.TicketCampaign).where(ticket_model.TicketCampaign.name == campaign.name))
        if result.first():
            raise HTTPException(status_code=400, detail="Campaign name must be unique")

        # Create the ticket campaign
        ticket_campaign = ticket_model.TicketCampaign.model_validate(campaign)
        self.session.add(ticket_campaign)
        await self.session.commit()
        await self.session.refresh(ticket_campaign)
        return ticket_campaign


    async def update_ticket_campaign(self, campaign_id: int, campaign: ticket_schema.TicketCampaignUpdate) -> Optional[ticket_schema.TicketCampaign]:
        # Validate the campaign name not empty and unique
        if not campaign.name:
            raise HTTPException(status_code=400, detail="Campaign name must not be empty")
        result = await self.session.exec(select(ticket_model.TicketCampaign).where(ticket_model.TicketCampaign.name == campaign.name))
        if result.first():
            raise HTTPException(status_code=400, detail="Campaign name must be unique")
        ticket_campaign = await self.get_ticket_campaign(campaign_id)
        if not ticket_campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")

        # Update the ticket campaign
        for key, value in campaign.model_dump(exclude_unset=True).items():
            setattr(ticket_campaign, key, value)
        self.session.add(ticket_campaign)
        await self.session.commit()
        await self.session.refresh(ticket_campaign)
        return ticket_campaign


    async def register_ticket_campaign(self, campaign_id: int) -> bool:
        # Validate campaign_id is an integer
        if not isinstance(campaign_id, int):
            raise HTTPException(status_code=400, detail="Campaign ID must be an integer")
        ticket_campaign = await self.get_ticket_campaign(campaign_id)
        if not ticket_campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        if ticket_campaign.limit is not None and ticket_campaign.registered >= ticket_campaign.limit:
            raise HTTPException(status_code=400, detail="Campaign registration limit exceeded")

        # Update the ticket campaign's registered count
        if ticket_campaign.registered is None:
            ticket_campaign.registered = 0
        ticket_campaign.registered = ticket_campaign.registered + 1
        self.session.add(ticket_campaign)
        await self.session.commit()
        await self.session.refresh(ticket_campaign)

        # Get TicketCampaignTicketTypes queryset
        ticket_campaign_ticket_types = await self.session.exec(
            select(ticket_model.TicketCampaignTicketType).where(ticket_model.TicketCampaignTicketType.campaign_id == campaign_id)
        )
        ticket_types: List[ticket_schema.TicketCampaignTicketType] = ticket_campaign_ticket_types.scalars().all()

        # Create Ticket
        for ticket_detail in ticket_types:
            ticket = ticket_schema.TicketCreate(
                campaign_id=ticket_campaign.id,
                ticket_type_id=ticket_detail.ticket_type_id,
                user_id=1,
                amount=ticket_detail.amount,
                used=0,
                expires_at=ticket_detail.expiration_date,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            await self.create_ticket(ticket)
        return True

    async def update_ticket_campaign_is_active(self, campaign_id: int) -> Optional[ticket_schema.TicketCampaign]:
        # Validate campaign_id
        ticket_campaign = await self.get_ticket_campaign(campaign_id)
        if not ticket_campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")

        # Update the ticket campaign's active status
        ticket_campaign.is_active = not ticket_campaign.is_active
        self.session.add(ticket_campaign)
        await self.session.commit()
        await self.session.refresh(ticket_campaign)
        return ticket_campaign


    async def delete_ticket_campaign(self, campaign_id: int) -> None:
        ticket_campaign = await self.get_ticket_campaign(campaign_id)
        if not ticket_campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        await self.session.delete(ticket_campaign)
        await self.session.commit()
        return ticket_campaign
