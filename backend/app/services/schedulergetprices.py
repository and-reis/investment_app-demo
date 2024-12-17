# -*- coding: utf-8 -*-
"""
Integration service for periodic price capture.

This module provides functionality to schedule and execute periodic price captures
from external APIs using APScheduler. The service can be activated or deactivated
for testing or operational purposes.

Created on Sat Nov 30 16:19:22 2024

@author: Derson
"""

from apscheduler.schedulers.background import BackgroundScheduler
from app.dbconfig import Database
from app.services.prices import PriceService
from datetime import datetime as dt

scheduler = BackgroundScheduler()


def capture_prices_manually():
    """
    Manually captures prices for active assets and stores OHLC data.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    db = Database()
    price_service = PriceService()

    with db.get_session() as session:
        active_assets = price_service.get_active_assets(session)
        schedule_execution_time = dt.now().strftime('%H:%M')

        for asset in active_assets:
            try:
                price_service.save_ohlc(f"{asset.symbol}", "1h", session)
                print(f"Prices for {asset.symbol} captured at {schedule_execution_time}")
            except Exception as e:
                print(f"Error capturing prices for {asset.symbol}: {e}")


def start_price_capture():
    """
    Starts the periodic price capture service.

    Parameters
    ----------
    None

    Returns
    -------
    apscheduler.job.Job
        The scheduled job instance.
    """
    db = Database()
    price_service = PriceService()

    def capture_prices():
        with db.get_session() as session:
            active_assets = price_service.get_active_assets(session)
            schedule_execution_time = dt.now().strftime('%H:%M')

            for asset in active_assets:
                try:
                    price_service.save_ohlc(f"{asset.symbol}", "1h", session)
                    print(f"Prices for {asset.symbol} captured at {schedule_execution_time}")
                except Exception as e:
                    print(f"Error capturing prices for {asset.symbol}: {e}")

    job = scheduler.add_job(capture_prices, "interval", minutes=1, id="price_capture")
    scheduler.start()

    return job


def stop_price_capture(job_id: str = None):
    """
    Stops a specific scheduled price capture job.

    Parameters
    ----------
    job_id : str, optional
        The ID of the job to stop. If not provided, no action is taken.

    Returns
    -------
    None
    """
    if job_id:
        scheduler.remove_job(job_id)


def stop_all_jobs():
    """
    Stops all scheduled jobs.

    Returns
    -------
    None
    """
    scheduler.remove_all_jobs()


# Example activation for testing purposes
job_name = start_price_capture()

# Uncomment to stop the job or manually capture prices
# stop_price_capture(job_name.id)
# capture_prices_manually()
