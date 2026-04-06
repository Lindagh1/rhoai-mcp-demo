import uvicorn
from typing import Any
from fastapi import FastAPI
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from starlette.requests import Request
import mcp.types as types

# Mocked Jira Database
MOCK_TICKETS = {
    "JIRA-404": {"status": "In Progress", "assignee": "Alice", "description": "The website shows a 404 error on the checkout page."},
    "JIRA-123": {"status": "Resolved", "assignee": "Bob", "description": "Update the logo on the homepage."},
    "JIRA-999": {"status": "Open", "assignee": "Unassigned", "description": "Customer is unable to log in to their account."}
}

mcp_server = Server("jira-mock-mcp")

@mcp_server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="get_jira_ticket",
            description="Retrieve details of a Jira ticket using its ID (e.g., JIRA-404)",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticket_id": {"type": "string", "description": "The Jira ticket ID (e.g., JIRA-404)"}
                },
                "required": ["ticket_id"]
            }
        )
    ]

@mcp_server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any] | None) -> list[types.TextContent]:
    if name == "get_jira_ticket":
        ticket_id = arguments.get("ticket_id")
        ticket = MOCK_TICKETS.get(ticket_id)
        if ticket:
            return [types.TextContent(type="text", text=str(ticket))]
        return [types.TextContent(type="text", text=f"Ticket {ticket_id} not found.")]
    raise ValueError(f"Unknown tool: {name}")

app = FastAPI()
transport: SseServerTransport | None = None

@app.get("/sse")
async def sse_endpoint(request: Request):
    global transport
    transport = SseServerTransport("/messages")
    await mcp_server.connect(transport)
    return await transport.handle_sse(request)

@app.post("/messages")
async def messages_endpoint(request: Request):
    if transport is None:
        raise RuntimeError("Not connected to SSE")
    await transport.handle_post_message(request)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)