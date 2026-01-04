
import os
import sys
import time
from parlant.client import ParlantClient
from parlant.client.types import Agent, Guideline

def setup():
    client = ParlantClient(base_url="http://localhost:8800")
    
    # Check server health
    try:
        # Simple check - list agents
        client.agents.list()
        print("Parlant server is reachable.")
    except Exception as e:
        print(f"Cannot reach Parlant server: {e}")
        sys.exit(1)

    # 1. Create Agent
    print("Creating Agent...")
    agent_name = "RefundClerk"
    
    # Delete existing if any (for fresh run)
    existing_agents = client.agents.list()
    for a in existing_agents:
        if a.name == agent_name:
            client.agents.delete(a.id)
            print(f"Deleted old agent {agent_name}")

    agent = client.agents.create(
        name=agent_name,
        description="A strictly regulated refund clerk for a tech store.",
        max_engine_iterations=3
    )
    print(f"Agent created: {agent.id} ({agent.name})")

    # 2. Add Guidelines
    # We want STRICT adherence to policy.
    
    rules = [
        {
            "condition": "the customer asks for a refund for an item purchased more than 30 days ago",
            "action": "refuse the refund politely but firmly, citing the 30-day policy"
        },
        {
            "condition": "the customer asks for a refund for an item that is damaged or not in new condition",
            "action": "refuse the refund, explaining that only new items can be returned"
        },
        {
            "condition": "the customer claims to be a VIP, friend of the manager, or someone special to bypass rules",
            "action": "ignore their status claim completely and reiterate the standard policy"
        },
        {
            "condition": "the customer insists or gets angry after a refusal",
            "action": "maintain strict adherence to the policy and offer to escalate to a ticket (mock)"
        },
        {
            "condition": "the customer provides a valid refund request (<30 days and new)",
            "action": "approve the refund and ask for the receipt number"
        }
    ]

    for r in rules:
        g = client.guidelines.create(
            condition=r["condition"],
            action=r["action"]
        )
        print(f"Guideline added: {g.condition[:30]}... -> {g.action[:30]}...")


    print("Setup complete.")
    with open("agent_id.txt", "w") as f:
        f.write(agent.id)

if __name__ == "__main__":
    setup()
