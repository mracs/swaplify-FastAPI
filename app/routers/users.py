from datetime import datetime, timedelta

from fastapi import APIRouter, Request, HTTPException, status, Response, Body

from app.models.users import tokens_table, get_source_by_token
from app.core.config import database
from app.core.utils import (
    conv_to_json, encode_base64, decode_base64, get_token, is_valid_uuid)

router = APIRouter()


@router.post('/pydict-to-json')
async def pydict_to_json(source: str = Body(..., embed=True)):
    try:
        return {'res': conv_to_json(source)}
    except (ValueError, SyntaxError, TypeError) as err:
        return {'err': str(err)}


@router.post('/save-and-share', status_code=201)
async def save_and_share(request: Request, response: Response,
                         source: str = Body(..., embed=True)):
    token = get_token(f'{request.client.host}:{source}')
    has_saved = await get_source_by_token(token)
    if has_saved:
        response.status_code = status.HTTP_200_OK
        return {'token': token}
    query = (
        tokens_table.insert()
        .values(token=token,
                user_ip=request.client.host,
                source=encode_base64(source),
                expires=datetime.now() + timedelta(weeks=1))
        .returning(tokens_table.c.token, tokens_table.c.user_ip)
    )
    return await database.fetch_one(query)


@router.get('/source/{token}')
async def get_source(token):
    if not is_valid_uuid(token):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='UUID is not valid',
        )
    source = await get_source_by_token(token)
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Source not found',
        )
    return {'source': decode_base64(source)}


@router.patch('/source/{token}', status_code=204)
async def update_source(token: str, source: str = Body(..., embed=True)):
    if not is_valid_uuid(token):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='UUID is not valid',
        )
    has_saved = await get_source_by_token(token)
    if not has_saved:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Source not found',
        )
    query = (
        tokens_table.update()
        .where(tokens_table.c.token == token)
        .values(source=encode_base64(source),
                expires=datetime.now() + timedelta(weeks=1))
    )
    await database.execute(query)
