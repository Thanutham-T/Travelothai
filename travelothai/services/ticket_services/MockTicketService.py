import datetime
from typing import List, Optional

from .TicketServiceInterface import TicketServiceInterface
from travelothai.schemas import ticket_schema

# Mock data for TicketType, TicketUsageRule, Ticket, TicketCampaign, and TicketCampaignTicketType
mock_ticket_types: List[ticket_schema.TicketType] = [
    ticket_schema.TicketType(id=1, name="Standard Ticket", price=100.0, created_at=datetime.datetime.now(), updated_at=datetime.datetime.now()),
    ticket_schema.TicketType(id=2, name="VIP Ticket", price=200.0, created_at=datetime.datetime.now(), updated_at=datetime.datetime.now()),
]
mock_ticket_usage_rules: List[ticket_schema.TicketUsageRule] = [
    ticket_schema.TicketUsageRule(id=1, ticket_type_id=1, category_id=1, allowance=True, tax_reduction=0.1, created_at=datetime.datetime.now(), updated_at=datetime.datetime.now()),
]
mock_tickets: List[ticket_schema.Ticket] = [
    ticket_schema.Ticket(id=1, user_id=1, ticket_type_id=1, campaign_id=None, amount=10, used=0, expires_at=datetime.datetime.now() + datetime.timedelta(days=30), created_at=datetime.datetime.now(), updated_at=datetime.datetime.now()),
    ticket_schema.Ticket(id=2, user_id=2, ticket_type_id=2, campaign_id=None, amount=5, used=0, expires_at=datetime.datetime.now() + datetime.timedelta(days=30), created_at=datetime.datetime.now(), updated_at=datetime.datetime.now()),
]
mock_ticket_campaigns: List[ticket_schema.TicketCampaign] = [
    ticket_schema.TicketCampaign(id=1, name="Summer Sale", is_active=True, limit=100, registed=0, start_date=datetime.datetime.now(), end_date=datetime.datetime.now() + datetime.timedelta(days=30), created_at=datetime.datetime.now(), updated_at=datetime.datetime.now()),
]
mock_ticket_campaign_ticket_types: List[ticket_schema.TicketCampaignTicketType] = [
    ticket_schema.TicketCampaignTicketType(id=1, campaign_id=1, ticket_type_id=1, amount=3, expiration_date=datetime.datetime.now() + datetime.timedelta(days=15), created_at=datetime.datetime.now(), updated_at=datetime.datetime.now()),
]

mock_ticket_type_id = 3
mock_ticket_usage_rule_id = 2
mock_ticket_id = 3
mock_ticket_campaign_id = 2
mock_ticket_campaign_ticket_type_id = 2


class MockTicketService(TicketServiceInterface):
    # Mock TicketType methods
    async def list_ticket_types(self) -> List[ticket_schema.TicketType]:
        return mock_ticket_types

    async def get_ticket_type(self, type_id: int) -> Optional[ticket_schema.TicketType]:
        for ticket_type in mock_ticket_types:
            if ticket_type.id == type_id:
                return ticket_type
        return None

    async def create_ticket_type(self, ticket_type: ticket_schema.TicketTypeCreate) -> ticket_schema.TicketType:
        global mock_ticket_type_id
        new_ticket_type = ticket_schema.TicketType(
            id=mock_ticket_type_id,
            name=ticket_type.name,
            price=ticket_type.price,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )
        mock_ticket_types.append(new_ticket_type)
        mock_id += 1
        return new_ticket_type

    async def update_ticket_type(self, type_id: int, ticket_type: ticket_schema.TicketTypeUpdate) -> Optional[ticket_schema.TicketType]:
        for idx, existing_ticket_type in enumerate(mock_ticket_types):
            if existing_ticket_type.id == type_id:
                updated_ticket_type = existing_ticket_type.model_copy(update=ticket_type.model_dump(exclude_unset=True))
                updated_ticket_type.updated_at = datetime.datetime.now()
                mock_ticket_types[idx] = updated_ticket_type
                return updated_ticket_type
        return None

    async def delete_ticket_type(self, type_id: int) -> None:
        global mock_ticket_types
        mock_ticket_types = [ticket_type for ticket_type in mock_ticket_types if ticket_type.id != type_id]
        return None


    # Mock TicketUsageRules methods
    async def list_ticket_usage_rules(self) -> List[ticket_schema.TicketUsageRule]:
        return mock_ticket_usage_rules

    async def get_ticket_usage_rule(self, rule_id: int) -> Optional[ticket_schema.TicketUsageRule]:
        for rule in mock_ticket_usage_rules:
            if rule.id == rule_id:
                return rule
        return None

    async def create_ticket_usage_rule(self, rule: ticket_schema.TicketUsageRuleCreate) -> ticket_schema.TicketUsageRule:
        global mock_ticket_usage_rule_id
        new_rule = ticket_schema.TicketUsageRule(
            id=mock_ticket_usage_rule_id,
            ticket_type_id=rule.ticket_type_id,
            category_id=rule.category_id,
            allowance=rule.allowance,
            tax_reduction=rule.tax_reduction,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )
        mock_ticket_usage_rules.append(new_rule)
        mock_ticket_usage_rule_id += 1
        return new_rule

    async def update_ticket_usage_rule(self, rule_id: int, rule: ticket_schema.TicketUsageRuleUpdate) -> Optional[ticket_schema.TicketUsageRule]:
        for idx, existing_rule in enumerate(mock_ticket_usage_rules):
            if existing_rule.id == rule_id:
                updated_rule = existing_rule.model_copy(update=rule.model_dump(exclude_unset=True))
                updated_rule.updated_at = datetime.datetime.now()
                mock_ticket_usage_rules[idx] = updated_rule
                return updated_rule
        return None

    async def delete_ticket_usage_rule(self, rule_id: int) -> None:
        global mock_ticket_usage_rules
        mock_ticket_usage_rules = [rule for rule in mock_ticket_usage_rules if rule.id != rule_id]
        return None
    

    # Mock Ticket methods
    async def list_tickets(self) -> List[ticket_schema.Ticket]:
        return mock_tickets

    async def get_ticket(self, ticket_id: int) -> Optional[ticket_schema.Ticket]:
        for ticket in mock_tickets:
            if ticket.id == ticket_id:
                return ticket
        return None

    async def create_ticket(self, ticket: ticket_schema.TicketCreate) -> ticket_schema.Ticket:
        global mock_ticket_id
        new_ticket = ticket_schema.Ticket(
            id=mock_ticket_id,
            user_id=ticket.user_id,
            ticket_type_id=ticket.ticket_type_id,
            campaign_id=ticket.campaign_id,
            amount=ticket.amount,
            used=ticket.used,
            expires_at=ticket.expires_at
        )
        mock_tickets.append(new_ticket)
        mock_ticket_id += 1
        return new_ticket

    async def update_ticket(self, ticket_id: int, ticket: ticket_schema.TicketUpdate) -> Optional[ticket_schema.Ticket]:
        for idx, existing_ticket in enumerate(mock_tickets):
            if existing_ticket.id == ticket_id:
                updated_ticket = existing_ticket.model_copy(update=ticket.model_dump(exclude_unset=True))
                updated_ticket.updated_at = datetime.datetime.now()
                mock_tickets[idx] = updated_ticket
                return updated_ticket
        return None

    async def collect_ticket(self, ticket_id: int) -> Optional[ticket_schema.Ticket]:
        for idx, existing_ticket in enumerate(mock_tickets):
            if existing_ticket.id == ticket_id:
                existing_ticket.user_id = None
                existing_ticket.updated_at = datetime.datetime.now()
                mock_tickets[idx] = existing_ticket
                return existing_ticket
        return None

    async def delete_ticket(self, ticket_id: int) -> None:
        global mock_tickets
        mock_tickets = [ticket for ticket in mock_tickets if ticket.id != ticket_id]
        return None


    # Mock TicketCampaign methods
    async def list_ticket_campaigns(self) -> List[ticket_schema.TicketCampaign]:
        return mock_ticket_campaigns

    async def get_ticket_campaign(self, campaign_id: int) -> Optional[ticket_schema.TicketCampaign]:
        for campaign in mock_ticket_campaigns:
            if campaign.id == campaign_id:
                return campaign
        return None

    async def create_ticket_campaign(self, campaign: ticket_schema.TicketCampaignCreate) -> ticket_schema.TicketCampaign:
        global mock_ticket_campaign_id
        new_campaign = ticket_schema.TicketCampaign(
            id=mock_ticket_campaign_id,
            name=campaign.name,
            is_active=getattr(campaign, 'is_active', True),
            limit=getattr(campaign, 'limit', 100),
            registed=getattr(campaign, 'registed', 0),
            start_date=campaign.start_date,
            end_date=campaign.end_date,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )
        mock_ticket_campaigns.append(new_campaign)
        mock_ticket_campaign_id += 1
        return new_campaign

    async def update_ticket_campaign(self, campaign_id: int, campaign: ticket_schema.TicketCampaignUpdate) -> Optional[ticket_schema.TicketCampaign]:
        for idx, existing_campaign in enumerate(mock_ticket_campaigns):
            if existing_campaign.id == campaign_id:
                updated_campaign = existing_campaign.model_copy(update=campaign.model_dump(exclude_unset=True))
                updated_campaign.updated_at = datetime.datetime.now()
                mock_ticket_campaigns[idx] = updated_campaign
                return updated_campaign
        return None

    async def register_ticket_campaign(self, campaign_id: int) -> bool:
        for idx, existing_campaign in enumerate(mock_ticket_campaigns):
            if existing_campaign.id == campaign_id:
                if existing_campaign.registered > existing_campaign.limit:
                    return False
                existing_campaign.registered = existing_campaign.registered + 1
                existing_campaign.updated_at = datetime.datetime.now()
                mock_ticket_campaigns[idx] = existing_campaign

                for existing_tctt in mock_ticket_campaign_ticket_types:
                    if existing_tctt.campaign_id == campaign_id:
                        mock_tickets.append(ticket_schema.Ticket(
                            id=mock_ticket_id,
                            user_id=None,
                            campaign_id=existing_tctt.campaign_id,
                            ticket_type_id=existing_tctt.ticket_type_id,
                            amount=existing_tctt.amount,
                            expiration_date=existing_tctt.expiration_date,
                            created_at=datetime.datetime.now(),
                            updated_at=datetime.datetime.now()
                        ))
                        mock_ticket_id += 1
                return True
        return False

    async def update_ticket_campaign_is_active(self, campaign_id: int) -> bool:
        for idx, existing_campaign in enumerate(mock_ticket_campaigns):
            if existing_campaign.id == campaign_id:
                existing_campaign.is_active = not existing_campaign.is_active
                existing_campaign.updated_at = datetime.datetime.now()
                mock_ticket_campaigns[idx] = existing_campaign
                return existing_campaign
        return True

    async def delete_ticket_campaign(self, campaign_id: int) -> None:
        global mock_ticket_campaigns
        mock_ticket_campaigns = [campaign for campaign in mock_ticket_campaigns if campaign.id != campaign_id]


    # Mock TicketCampaignTicketType methods
    async def list_ticket_campaign_ticket_types(self) -> List[ticket_schema.TicketCampaignTicketType]:
        return mock_ticket_campaign_ticket_types

    async def get_ticket_campaign_ticket_type(self, tctt_id: int) -> Optional[ticket_schema.TicketCampaignTicketType]:
        for tctt in mock_ticket_campaign_ticket_types:
            if tctt.id == tctt_id:
                return tctt
        return None

    async def create_ticket_campaign_ticket_type(self, tctt: ticket_schema.TicketCampaignTicketTypeCreate) -> ticket_schema.TicketCampaignTicketType:
        global mock_ticket_campaign_ticket_type_id
        new_tctt = ticket_schema.TicketCampaignTicketType(
            id=mock_ticket_campaign_ticket_type_id,
            campaign_id=tctt.campaign_id,
            ticket_type_id=tctt.ticket_type_id,
            amount=tctt.amount,
            expiration_date=tctt.expiration_date,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )
        mock_ticket_campaign_ticket_types.append(new_tctt)
        mock_ticket_campaign_ticket_type_id += 1
        return new_tctt

    async def update_ticket_campaign_ticket_type(self, tctt_id: int, tctt: ticket_schema.TicketCampaignTicketTypeUpdate) -> Optional[ticket_schema.TicketCampaignTicketType]:
        for idx, existing_tctt in enumerate(mock_ticket_campaign_ticket_types):
            if existing_tctt.id == tctt_id:
                updated_tctt = existing_tctt.model_copy(update=tctt.model_dump(exclude_unset=True))
                updated_tctt.updated_at = datetime.datetime.now()
                mock_ticket_campaign_ticket_types[idx] = updated_tctt
                return updated_tctt
        return None

    async def delete_ticket_campaign_ticket_type(self, tctt_id: int) -> None:
        global mock_ticket_campaign_ticket_types
        mock_ticket_campaign_ticket_types = [tctt for tctt in mock_ticket_campaign_ticket_types if tctt.id != tctt_id]
        return None
    
