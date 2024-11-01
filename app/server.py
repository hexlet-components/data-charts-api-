import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime
from typing import List

import asyncpg
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Query

load_dotenv()

DATABASE_URL = "postgres://student:student@65.108.223.44:5432/chartsdb"

# Менеджер контекста для подключения к БД
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаем пул соединений при старте
    app.state.pool = await asyncpg.create_pool(
        DATABASE_URL,
        min_size=5,
        max_size=20
    )
    yield
    # Закрываем пул при выключении
    await app.state.pool.close()

app = FastAPI(lifespan=lifespan)

# Зависимость для получения соединения с БД
async def get_db():
    async with app.state.pool.acquire() as conn:
        yield conn

@app.get("/")
async def index():
    return {"status": "It Works"}

@app.get("/visits")
async def get_visits(
    begin: datetime = Query(..., description="Start date in ISO format"),
    end: datetime = Query(..., description="End date in ISO format"),
    db = Depends(get_db)
):
    try:
        query = """
            SELECT *
            FROM visits
            WHERE visits.datetime BETWEEN $1 AND $2;
        """
        records = await db.fetch(query, begin, end)
        return records
    except Exception as e:
        logging.error(f"Error fetching visits: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error occurred while fetching visits"
        )

@app.get("/registrations")
async def get_registrations(
    begin: datetime = Query(..., description="Start date in ISO format"),
    end: datetime = Query(..., description="End date in ISO format"),
    db = Depends(get_db)
):
    try:
        query = """
            SELECT *
            FROM registrations
            WHERE registrations.datetime BETWEEN $1 AND $2;
        """
        records = await db.fetch(query, begin, end)
        return records
    except Exception as e:
        logging.error(f"Error fetching registrations: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error occurred while fetching registrations"
        )
