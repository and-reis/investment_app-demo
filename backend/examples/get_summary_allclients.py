from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.dependencies import get_database_instance
from app.models import Portfolio, User

def get_manager_clients_portfolios(manager_id: int, session: Session):
    """
    Retrieves the portfolio details of clients managed by a specific manager.
    """
    query = (
        session.query(
            User.user_id,
            User.username,
            Portfolio.asset_symbol,
            Portfolio.trade_type,
            Portfolio.qty,
            Portfolio.net_val
        )
        .outerjoin(Portfolio, Portfolio.user_id == User.user_id)
        .filter(User.manager_id == manager_id)
    )
    
    return [dict(row._mapping) for row in query.all()]

def get_summarized_manager_clients_portfolios(manager_id: int, session: Session):
    """
    Retrieves a summarized view of the portfolios of clients managed by a specific manager.
    """
    query = (
        session.query(
            User.user_id,
            User.username,
            Portfolio.asset_symbol,            
            func.abs(func.sum(func.coalesce(Portfolio.qty, 0))).label("total_qty"),
            func.abs(func.sum(func.coalesce(Portfolio.net_val, 0))).label("total_value"),
        )
        .outerjoin(Portfolio, Portfolio.user_id == User.user_id)
        .filter(User.manager_id == manager_id)
        .group_by(User.user_id, User.username, Portfolio.asset_symbol)
    )
    
    return [dict(row._mapping) for row in query.all()]

# Example usage
session = get_database_instance().get_session()

# Retrieve detailed portfolio view
clients_portfolio = get_manager_clients_portfolios(11, session=session)
print(clients_portfolio)

# Uncomment to retrieve summarized portfolio view
# clients_portfolio_summarized = get_summarized_manager_clients_portfolios(11, session=session)
# print(clients_portfolio_summarized)
