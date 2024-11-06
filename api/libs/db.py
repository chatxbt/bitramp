import os
# from pq import PQ
# from fastapi import Depends
# from typing import Annotated
# from sqlmodel import create_engine, SQLModel, Session
from supabase._async.client import AsyncClient as Client, create_client


async def get_supabase_client() -> Client:
    return await create_client(
        supabase_url=os.environ.get("SUPABASE_URL"),
        supabase_key=os.environ.get("SUPABASE_KEY")
    )

# supabase_postgres_password: str = os.environ.get("SUPABASE_POSTGRES_PASSWORD")
# supabase_postgres_url: str = os.environ.get("SUPABASE_CONNECTION_STRING")
#
# supabase_postgres_engine = create_engine(supabase_postgres_url)
#
#
# def create_db_and_tables():
#     SQLModel.metadata.create_all(supabase_postgres_engine)
#
#
# def get_session():
#     with Session(supabase_postgres_engine) as session:
#         yield session
#
#
# pq = PQ(create_engine(supabase_postgres_url).raw_connection(), async_=True)
# pq.create()
#
# SessionDep = Annotated[Session, Depends(get_session)]
# SupabaseDep = Annotated[Client, Depends(get_supabase_client)]
