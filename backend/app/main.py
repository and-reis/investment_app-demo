"""
Main module for the Investment App Demo.

This module initializes the FastAPI application, connects to the database,
creates initial data, and includes all API routes.

Created on Thu Nov 28 15:16:38 2024

@author: Derson
"""

from fastapi import FastAPI
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from app.dbconfig import Base
from app.dependencies import get_database_instance
from app.models import Asset, PriceHistory
from app.services.prices import PriceService
from app.routers import user, portfolio, prices, wallet, assets, manager
import logging
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
logging.getLogger("ccxt.base.exchange").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Database connection
db = get_database_instance()


async def verify_database_connection(max_retries: int = 10, retry_delay: int = 2) -> bool:
    """
    Verifies the database connection with retry logic.

    Parameters
    ----------
    max_retries : int, optional
        Maximum number of retries before failing (default is 10).
    retry_delay : int, optional
        Delay in seconds between retries (default is 2).

    Returns
    -------
    bool
        True if the connection is successful, otherwise raises RuntimeError.

    Raises
    ------
    RuntimeError
        If the connection fails after the specified retries.
    """
    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"Attempting to connect to the database... (Attempt {attempt}/{max_retries})")
            with db.get_session() as session:
                session.execute(text("SELECT 1"))
            logger.info("Successfully connected to the database.")
            return True
        except OperationalError:
            logger.warning(f"Database connection failed. Retrying in {retry_delay} seconds...")
            await asyncio.sleep(retry_delay)
        except SQLAlchemyError as e:
            logger.error(f"Unexpected database error: {e}")
            raise RuntimeError("Critical error connecting to the database.") from e

    logger.error("Failed to connect to the database after multiple attempts. Check your configuration.")
    raise RuntimeError("Database connection failed after multiple retries.")


def initialize_database():
    """
    Initializes the database by creating tables and inserting initial data.
    """
    logger.info("Checking and creating database tables...")
    Base.metadata.create_all(bind=db.engine)
    logger.info("Database tables checked and created successfully.")

    with db.get_session() as session:
        insert_initial_assets(session)
        insert_initial_prices(session)


def insert_initial_assets(session: Session):
    """
    Verifies and inserts initial assets into the database.

    Parameters
    ----------
    session : sqlalchemy.orm.Session
        The database session.
    """
    logger.info("Checking initial assets...")
    assets = [
        {"name": "Bitcoin", "symbol": "BTC", "type": "cryptocurrency"},
        {"name": "Ethereum", "symbol": "ETH", "type": "cryptocurrency"},
        {"name": "Solana", "symbol": "SOL", "type": "cryptocurrency"}
    ]
    for asset in assets:
        exists = session.query(Asset).filter_by(symbol=asset["symbol"]).first()
        if not exists:
            new_asset = Asset(
                name=asset["name"],
                symbol=asset["symbol"],
                type=asset["type"],
                active=True,
            )
            session.add(new_asset)
    session.commit()
    logger.info("Initial assets checked and added if necessary.")


def insert_initial_prices(session: Session):
    """
    Verifies and inserts initial prices for active assets.

    Parameters
    ----------
    session : sqlalchemy.orm.Session
        The database session.
    """
    logger.info("Checking initial prices...")
    price_service = PriceService()
    assets = session.query(Asset).filter_by(active=True).all()
    for asset in assets:
        if not session.query(PriceHistory).filter_by(asset_symbol=asset.symbol).first():
            logger.info(f"Importing initial prices for {asset.symbol}...")
            price_service.save_ohlc(asset.symbol, "1h", session)
    logger.info("Initial prices checked and added.")


async def app_lifespan(app: FastAPI):
    """
    Handles application lifespan events, including initialization and teardown.

    Parameters
    ----------
    app : FastAPI
        The FastAPI application instance.

    Yields
    ------
    None
    """
    logger.info("Starting application...")
    await verify_database_connection()
    initialize_database()
    logger.info("Application started successfully.")
    yield
    logger.info("Shutting down the application.")


# FastAPI application initialization
app = FastAPI(title="Investment App Demo", lifespan=app_lifespan)

# Include routers
app.include_router(user.router, prefix="/user", tags=["Users"])
app.include_router(portfolio.router, prefix="/portfolio", tags=["Portfolio"])
app.include_router(prices.router, prefix="/prices", tags=["Prices"])
app.include_router(wallet.router, prefix="/wallet", tags=["Balance"])
app.include_router(assets.router, prefix="/assets", tags=["Assets Admin"])
app.include_router(manager.router, prefix="/manager", tags=["Portfolio Managers"])


@app.get("/", summary="Root endpoint")
def root():
    """
    Root endpoint for health check.

    Returns
    -------
    dict
        A message confirming the application is running.
    """
    return {"message": "Investment App Demo is running!"}
