from fastapi import APIRouter, Depends, Response
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from travelothai.core.config import get_settings
from travelothai.services.ticket_services.TicketServiceInterface import TicketServiceInterface
from travelothai.services.ticket_services.MockTicketService import MockTicketService
from travelothai.services.ticket_services.DBTicketService import DBTicketService

from travelothai.schemas import ticket_schema
from travelothai.models import get_session

router = APIRouter(prefix="/tickets", tags=["tickets"])


def get_ticket_service(session: AsyncSession = Depends(get_session)) -> TicketServiceInterface:
    settings = get_settings()
    if settings.USE_MOCK:
        return MockTicketService()
    return DBTicketService(session=session)


# TicketType Endpoints
@router.get(
        "/types",
        summary="List all ticket types",
        description="Retrieve a list of all ticket types available in the system.",
        response_model=list[ticket_schema.TicketType]
    )
async def read_ticket_types(ticket_service: TicketServiceInterface = Depends(get_ticket_service)) -> List[ticket_schema.TicketType]:
    return await ticket_service.list_ticket_types()

@router.get(
        "/types/{type_id}",
        summary="Get a specific ticket type",
        description="Retrieve details of a specific ticket type by its ID.",
        response_model=ticket_schema.TicketType
    )
async def read_ticket_type(type_id: int, ticket_service: TicketServiceInterface = Depends(get_ticket_service)) -> Optional[ticket_schema.TicketType]:
    return await ticket_service.get_ticket_type(type_id)

@router.post(
        "/types",
        summary="Create a new ticket type",
        description="Create a new ticket type in the system.",
        response_model=ticket_schema.TicketType
    )
async def create_ticket_type(type: ticket_schema.TicketTypeCreate, ticket_service: TicketServiceInterface = Depends(get_ticket_service)) -> ticket_schema.TicketType:
    return await ticket_service.create_ticket_type(type)

@router.put(
        "/types/{type_id}",
        summary="Update a ticket type",
        description="Update an existing ticket type in the system.",
        response_model=ticket_schema.TicketType
    )
async def update_ticket_type(type_id: int, type: ticket_schema.TicketTypeUpdate, ticket_service: TicketServiceInterface = Depends(get_ticket_service)) -> Optional[ticket_schema.TicketType]:
    return await ticket_service.update_ticket_type(type_id, type)

@router.delete(
        "/types/{type_id}",
        summary="Delete a ticket type",
        description="Delete a ticket type from the system.",
        response_model=None
    )
async def delete_ticket_type(type_id: int, ticket_service: TicketServiceInterface = Depends(get_ticket_service)) -> None:
    await ticket_service.delete_ticket_type(type_id)
    return Response(status_code=204, content=None)


# TicketUsageRule Endpoints
@router.get(
        "/usage-rules",
        summary="List all ticket usage rules",
        description="Retrieve a list of all ticket usage rules available in the system.",
        response_model=list[ticket_schema.TicketUsageRule]
    )
async def read_ticket_usage_rules(ticket_service: TicketServiceInterface = Depends(get_ticket_service)) -> List[ticket_schema.TicketUsageRule]:
    return await ticket_service.list_ticket_usage_rules()

@router.get(
        "/usage-rules/{rule_id}",
        summary="Get a specific ticket usage rule",
        description="Retrieve details of a specific ticket usage rule by its ID.",
        response_model=ticket_schema.TicketUsageRule
    )
async def read_ticket_usage_rule(rule_id: int, ticket_service: TicketServiceInterface = Depends(get_ticket_service)) -> Optional[ticket_schema.TicketUsageRule]:
    return await ticket_service.get_ticket_usage_rule(rule_id)

@router.post(
        "/usage-rules",
        summary="Create a new ticket usage rule",
        description="Create a new ticket usage rule in the system.",
        response_model=ticket_schema.TicketUsageRule
    )
async def create_ticket_usage_rule(rule: ticket_schema.TicketUsageRuleCreate, ticket_service: TicketServiceInterface = Depends(get_ticket_service)) -> ticket_schema.TicketUsageRule:
    return await ticket_service.create_ticket_usage_rule(rule)

@router.put(
        "/usage-rules/{rule_id}",
        summary="Update a ticket usage rule",
        description="Update an existing ticket usage rule in the system.",
        response_model=ticket_schema.TicketUsageRule
    )
async def update_ticket_usage_rule(rule_id: int, rule: ticket_schema.TicketUsageRuleUpdate, ticket_service: TicketServiceInterface = Depends(get_ticket_service)) -> Optional[ticket_schema.TicketUsageRule]:
    return await ticket_service.update_ticket_usage_rule(rule_id, rule)

@router.delete(
        "/usage-rules/{rule_id}",
        summary="Delete a ticket usage rule",
        description="Delete a ticket usage rule from the system.",
        response_model=None
    )
async def delete_ticket_usage_rule(rule_id: int, ticket_service: TicketServiceInterface = Depends(get_ticket_service)) -> None:
    await ticket_service.delete_ticket_usage_rule(rule_id)
    return Response(status_code=204, content=None)


# TicketCampaignTicketTypes Endpoints
@router.get(
        "/campaigns/ticket-types",
        summary="List all ticket types for a specific campaign",
        description="Retrieve a list of all ticket types associated with a specific ticket campaign.",
        response_model=list[ticket_schema.TicketCampaignTicketType]
    )
async def read_ticket_campaign_ticket_types(ticket_service: TicketServiceInterface = Depends(get_ticket_service)) -> List[ticket_schema.TicketCampaignTicketType]:
    return await ticket_service.list_ticket_campaign_ticket_types()

@router.get(
        "/campaigns/ticket-types/{tctt_id}",
        summary="Get a specific ticket type for a specific campaign",
        description="Retrieve details of a specific ticket type associated with a specific ticket campaign.",
        response_model=ticket_schema.TicketCampaignTicketType
    )
async def read_ticket_campaign_ticket_type(tctt_id: int, ticket_service: TicketServiceInterface = Depends(get_ticket_service)) -> Optional[ticket_schema.TicketCampaignTicketType]:
    return await ticket_service.get_ticket_campaign_ticket_type(tctt_id)

@router.post(
        "/campaigns/ticket-types/",
        summary="Create a new ticket type for a specific campaign",
        description="Create a new ticket type associated with a specific ticket campaign.",
        response_model=ticket_schema.TicketCampaignTicketType
    )
async def create_ticket_campaign_ticket_type(tctt: ticket_schema.TicketCampaignTicketTypeCreate, ticket_service: TicketServiceInterface = Depends(get_ticket_service)) -> ticket_schema.TicketCampaignTicketType:
    return await ticket_service.create_ticket_campaign_ticket_type(tctt)

@router.put(
        "/campaigns/ticket-types/{tctt_id}",
        summary="Update a ticket type for a specific campaign",
        description="Update a ticket type associated with a specific ticket campaign.",
        response_model=ticket_schema.TicketCampaignTicketType
    )
async def update_ticket_campaign_ticket_type(tctt_id: int, tctt: ticket_schema.TicketCampaignTicketTypeUpdate, ticket_service: TicketServiceInterface = Depends(get_ticket_service)) -> Optional[ticket_schema.TicketCampaignTicketType]:
    return await ticket_service.update_ticket_campaign_ticket_type(tctt_id, tctt)

@router.delete(
        "/campaigns/ticket-types/{tctt_id}",
        summary="Delete a ticket type from a specific campaign",
        description="Delete a ticket type associated with a specific ticket campaign.",
        response_model=None
    )
async def delete_ticket_campaign_ticket_type(tctt_id: int, ticket_service: TicketServiceInterface = Depends(get_ticket_service)) -> None:
    await ticket_service.delete_ticket_campaign_ticket_type(tctt_id)
    return Response(status_code=204, content=None)


# TicketCampaigns Endpoints
@router.get(
        "/campaigns",
        summary="List all ticket campaigns",
        description="Retrieve a list of all ticket campaigns available in the system.",
        response_model=list[ticket_schema.TicketCampaign]
    )
async def read_ticket_campaigns(ticket_service: TicketServiceInterface = Depends(get_ticket_service)) -> List[ticket_schema.TicketCampaign]:
    return await ticket_service.list_ticket_campaigns()

@router.get(
        "/campaigns/{campaign_id}",
        summary="Get a specific ticket campaign",
        description="Retrieve details of a specific ticket campaign by its ID.",
        response_model=ticket_schema.TicketCampaign
    )
async def read_ticket_campaign(campaign_id: int, ticket_service: TicketServiceInterface = Depends(get_ticket_service)) -> Optional[ticket_schema.TicketCampaign]:
    return await ticket_service.get_ticket_campaign(campaign_id)

@router.post(
        "/campaigns",
        summary="Create a new ticket campaign",
        description="Create a new ticket campaign in the system.",
        response_model=ticket_schema.TicketCampaign
    )
async def create_ticket_campaign(campaign: ticket_schema.TicketCampaignCreate, ticket_service: TicketServiceInterface = Depends(get_ticket_service)) -> ticket_schema.TicketCampaign:
    return await ticket_service.create_ticket_campaign(campaign)

@router.put(
        "/campaigns/{campaign_id}",
        summary="Update a ticket campaign",
        description="Update an existing ticket campaign in the system.",
        response_model=ticket_schema.TicketCampaign
    )
async def update_ticket_campaign(campaign_id: int, campaign: ticket_schema.TicketCampaignUpdate, ticket_service: TicketServiceInterface = Depends(get_ticket_service)) -> Optional[ticket_schema.TicketCampaign]:
    return await ticket_service.update_ticket_campaign(campaign_id, campaign)

@router.post(
        "/campaigns/register/{campaign_id}",
        summary="Register for a ticket campaign",
        description="Register a user for a specific ticket campaign.",
        response_model=bool
    )
async def register_ticket_campaign(campaign_id: int, ticket_service: TicketServiceInterface = Depends(get_ticket_service)) -> bool:
    return await ticket_service.register_ticket_campaign(campaign_id)

@router.put(
        "/campaigns/is-active/{campaign_id}",
        summary="Update the active status of a ticket campaign",
        description="Update the active status of a specific ticket campaign.",
        response_model=bool
    )
async def update_ticket_campaign_is_active(campaign_id: int, ticket_service: TicketServiceInterface = Depends(get_ticket_service)) -> bool:
    return await ticket_service.update_ticket_campaign_is_active(campaign_id)

@router.delete(
        "/campaigns/{campaign_id}",
        summary="Delete a ticket campaign",
        description="Delete a ticket campaign from the system.",
        response_model=None
    )
async def delete_ticket_campaign(campaign_id: int, ticket_service: TicketServiceInterface = Depends(get_ticket_service)) -> None:
    await ticket_service.delete_ticket_campaign(campaign_id)
    return Response(status_code=204, content=None)


# Ticket Endpoints
@router.get(
        "/",
        summary="List all tickets",
        description="Retrieve a list of all tickets available in the system.",
        response_model=list[ticket_schema.Ticket]
    )
async def read_tickets(ticket_service: TicketServiceInterface = Depends(get_ticket_service)) -> List[ticket_schema.Ticket]:
    return await ticket_service.list_tickets()

@router.get(
        "/{ticket_id}",
        summary="Get a specific ticket",
        description="Retrieve details of a specific ticket by its ID.",
        response_model=ticket_schema.Ticket
    )
async def read_ticket(ticket_id: int, ticket_service: TicketServiceInterface = Depends(get_ticket_service)) -> Optional[ticket_schema.Ticket]:
    return await ticket_service.get_ticket(ticket_id)

@router.post(
        "/",
        summary="Create a new ticket",
        description="Create a new ticket in the system.",
        response_model=ticket_schema.Ticket
    )
async def create_ticket(ticket: ticket_schema.TicketCreate, ticket_service: TicketServiceInterface = Depends(get_ticket_service)) -> ticket_schema.Ticket:
    return await ticket_service.create_ticket(ticket)

@router.put(
        "/{ticket_id}",
        summary="Update a ticket",
        description="Update an existing ticket in the system.",
        response_model=ticket_schema.Ticket
    )
async def update_ticket(ticket_id: int, ticket: ticket_schema.TicketUpdate, ticket_service: TicketServiceInterface = Depends(get_ticket_service)) -> Optional[ticket_schema.Ticket]:
    return await ticket_service.update_ticket(ticket_id, ticket)

@router.put(
        "/{ticket_id}/traveler",
        summary="Traveler collects the ticket",
        description="Update the traveler information for a specific ticket.",
        response_model=ticket_schema.Ticket
    )
async def collect_ticket(ticket_id: int, ticket_service: TicketServiceInterface = Depends(get_ticket_service)) -> Optional[ticket_schema.Ticket]:
    return await ticket_service.collect_ticket(ticket_id)

@router.delete(
        "/{ticket_id}",
        summary="Delete a ticket",
        description="Delete a ticket from the system.",
        response_model=None
    )
async def delete_ticket(ticket_id: int, ticket_service: TicketServiceInterface = Depends(get_ticket_service)) -> None:
    await ticket_service.delete_ticket(ticket_id)
    return Response(status_code=204, content=None)
