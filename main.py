from fastmcp import FastMCP
from models import CreateAccount, Amount
import database as db

mcp = FastMCP("Bank MCP Server")


@mcp.tool()
def create_account(payload: CreateAccount):
    acct = db.create_account(payload.owner, payload.initial_deposit)
    return {
        "account_id": acct["id"],
        "owner": acct["owner"],
        "balance": acct["balance"]
    }


@mcp.tool()
def deposit(account_id: int, payload: Amount):
    acct = db.get_account(account_id)
    if not acct:
        return {"error": "account not found"}

    db.update_balance(account_id, payload.amount)
    db.add_transaction(account_id, "deposit", payload.amount)

    updated = db.get_account(account_id)
    return {
        "account_id": account_id,
        "new_balance": updated["balance"]
    }


@mcp.tool()
def withdraw(account_id: int, payload: Amount):
    acct = db.get_account(account_id)
    if not acct:
        return {"error": "account not found"}

    if acct["balance"] < payload.amount:
        return {"error": "insufficient funds"}

    db.update_balance(account_id, -payload.amount)
    db.add_transaction(account_id, "withdraw", payload.amount)

    updated = db.get_account(account_id)
    return {
        "account_id": account_id,
        "new_balance": updated["balance"]
    }


@mcp.tool()
def balance(account_id: int):
    acct = db.get_account(account_id)
    if not acct:
        return {"error": "account not found"}

    return {
        "account_id": account_id,
        "balance": acct["balance"]
    }


@mcp.tool()
def transactions(account_id: int, limit: int = 20):
    acct = db.get_account(account_id)
    if not acct:
        return {"error": "account not found"}

    txs = db.get_transactions(account_id, limit)
    return {
        "account_id": account_id,
        "transactions": txs
    }
if __name__ == "__main__":
    mcp.run()

