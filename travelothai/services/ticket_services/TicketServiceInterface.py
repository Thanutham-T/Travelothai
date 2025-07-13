from abc import ABC, abstractmethod
from typing import List, Optional

from travelothai.schemas import ticket_schema


class TicketServiceInterface(ABC):
    # TicketType methods
    @abstractmethod
    async def list_ticket_types(self) -> List[ticket_schema.TicketType]:
        """List all ticket types."""
        pass

    @abstractmethod
    async def get_ticket_type(self, type_id: int) -> Optional[ticket_schema.TicketType]:
        """Get a specific ticket type by ID."""
        pass

    @abstractmethod
    async def create_ticket_type(self, type: ticket_schema.TicketTypeCreate) -> ticket_schema.TicketType:
        """Create a new ticket type."""
        pass

    @abstractmethod
    async def update_ticket_type(self, type_id: int, type: ticket_schema.TicketTypeUpdate) -> Optional[ticket_schema.TicketType]:
        """Update an existing ticket type."""
        pass

    @abstractmethod
    async def delete_ticket_type(self, type_id: int) -> None:
        """Delete a ticket type."""
        pass


    # TicketUsageRules methods
    @abstractmethod
    async def list_ticket_usage_rules(self) -> List[ticket_schema.TicketUsageRule]:
        """List all ticket usage rules."""
        pass

    @abstractmethod
    async def get_ticket_usage_rule(self, rule_id: int) -> Optional[ticket_schema.TicketUsageRule]:
        """Get a specific ticket usage rule by ID."""
        pass

    @abstractmethod
    async def create_ticket_usage_rule(self, rule: ticket_schema.TicketUsageRuleCreate) -> ticket_schema.TicketUsageRule:
        """Create a new ticket usage rule."""
        pass

    @abstractmethod
    async def update_ticket_usage_rule(self, rule_id: int, rule: ticket_schema.TicketUsageRuleUpdate) -> Optional[ticket_schema.TicketUsageRule]:
        """Update an existing ticket usage rule."""
        pass

    @abstractmethod
    async def delete_ticket_usage_rule(self, rule_id: int) -> None:
        """Delete a ticket usage rule."""
        pass


    # Ticket methods
    @abstractmethod
    async def list_tickets(self) -> List[ticket_schema.Ticket]:
        """List all tickets."""
        pass

    @abstractmethod
    async def get_ticket(self, ticket_id: int) -> Optional[ticket_schema.Ticket]:
        """Get a specific ticket by ID."""
        pass

    @abstractmethod
    async def create_ticket(self, ticket: ticket_schema.TicketCreate) -> ticket_schema.Ticket:
        """Create a new ticket."""
        pass

    @abstractmethod
    async def update_ticket(self, ticket_id: int, ticket: ticket_schema.TicketUpdate) -> Optional[ticket_schema.Ticket]:
        """Update an existing ticket."""
        pass

    @abstractmethod
    async def collect_ticket(self, ticket_id: int) -> Optional[ticket_schema.Ticket]:
        """Collect a ticket for a traveler."""
        pass

    @abstractmethod
    async def delete_ticket(self, ticket_id: int) -> None:
        """Delete a ticket."""
        pass

    # TicketCampaign methods
    @abstractmethod
    async def list_ticket_campaigns(self) -> List[ticket_schema.TicketCampaign]:
        """List all ticket campaigns."""
        pass

    @abstractmethod
    async def get_ticket_campaign(self, campaign_id: int) -> Optional[ticket_schema.TicketCampaign]:
        """Get a specific ticket campaign by ID."""
        pass

    @abstractmethod
    async def create_ticket_campaign(self, campaign: ticket_schema.TicketCampaignCreate) -> ticket_schema.TicketCampaign:
        """Create a new ticket campaign."""
        pass

    @abstractmethod
    async def update_ticket_campaign(self, campaign_id: int, campaign: ticket_schema.TicketCampaignUpdate) -> Optional[ticket_schema.TicketCampaign]:
        """Update an existing ticket campaign."""
        pass

    @abstractmethod
    async def register_ticket_campaign(self, campaign_id: int) -> bool:
        """Register a user for a ticket campaign."""
        pass

    @abstractmethod
    async def update_ticket_campaign_is_active(self, campaign_id: int) -> bool:
        """Update an existing ticket campaign's active status."""
        pass

    @abstractmethod
    async def delete_ticket_campaign(self, campaign_id: int) -> None:
        """Delete a ticket campaign."""
        pass

    # TicketCampaignTicketType methods
    @abstractmethod
    async def list_ticket_campaign_ticket_types(self) -> List[ticket_schema.TicketCampaignTicketType]:
        """List all ticket campaign ticket types."""
        pass

    @abstractmethod
    async def get_ticket_campaign_ticket_type(self, tctt_id: int) -> Optional[ticket_schema.TicketCampaignTicketType]:
        """Get a specific ticket campaign ticket type by ID."""
        pass

    @abstractmethod
    async def create_ticket_campaign_ticket_type(self, tctt: ticket_schema.TicketCampaignTicketTypeCreate) -> ticket_schema.TicketCampaignTicketType:
        """Create a new ticket campaign ticket type."""
        pass

    @abstractmethod
    async def update_ticket_campaign_ticket_type(self, tctt_id: int, tctt: ticket_schema.TicketCampaignTicketTypeUpdate) -> Optional[ticket_schema.TicketCampaignTicketType]:
        """Update an existing ticket campaign ticket type."""
        pass

    @abstractmethod
    async def delete_ticket_campaign_ticket_type(self, tctt_id: int) -> None:
        """Delete a ticket campaign ticket type."""
        pass
