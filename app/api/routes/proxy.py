from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_partner
from app.db.session import get_db
from app.models import Partner
from app.services import ProxyService


router = APIRouter(prefix="/proxy", tags=["proxy"])
proxy_service = ProxyService()


@router.get("/users")
async def proxy_users(
    partner: Partner = Depends(get_current_partner),
    db: AsyncSession = Depends(get_db),
):
    return await proxy_service.proxy_get(
        db,
        partner=partner,
        proxy_path="/proxy/users",
        upstream_path="users",
    )


@router.get("/users/{user_id}")
async def proxy_user_detail(
    user_id: int,
    partner: Partner = Depends(get_current_partner),
    db: AsyncSession = Depends(get_db),
):
    return await proxy_service.proxy_get(
        db,
        partner=partner,
        proxy_path=f"/proxy/users/{user_id}",
        upstream_path=f"users/{user_id}",
    )


@router.get("/posts")
async def proxy_posts(
    partner: Partner = Depends(get_current_partner),
    db: AsyncSession = Depends(get_db),
):
    return await proxy_service.proxy_get(
        db,
        partner=partner,
        proxy_path="/proxy/posts",
        upstream_path="posts",
    )


@router.get("/posts/{post_id}")
async def proxy_post_detail(
    post_id: int,
    partner: Partner = Depends(get_current_partner),
    db: AsyncSession = Depends(get_db),
):
    return await proxy_service.proxy_get(
        db,
        partner=partner,
        proxy_path=f"/proxy/posts/{post_id}",
        upstream_path=f"posts/{post_id}",
    )


@router.get("/comments")
async def proxy_comments(
    partner: Partner = Depends(get_current_partner),
    db: AsyncSession = Depends(get_db),
):
    return await proxy_service.proxy_get(
        db,
        partner=partner,
        proxy_path="/proxy/comments",
        upstream_path="comments",
    )


@router.get("/comments/{comment_id}")
async def proxy_comment_detail(
    comment_id: int,
    partner: Partner = Depends(get_current_partner),
    db: AsyncSession = Depends(get_db),
):
    return await proxy_service.proxy_get(
        db,
        partner=partner,
        proxy_path=f"/proxy/comments/{comment_id}",
        upstream_path=f"comments/{comment_id}",
    )


@router.get("/todos")
async def proxy_todos(
    partner: Partner = Depends(get_current_partner),
    db: AsyncSession = Depends(get_db),
):
    return await proxy_service.proxy_get(
        db,
        partner=partner,
        proxy_path="/proxy/todos",
        upstream_path="todos",
    )


@router.get("/todos/{todo_id}")
async def proxy_todo_detail(
    todo_id: int,
    partner: Partner = Depends(get_current_partner),
    db: AsyncSession = Depends(get_db),
):
    return await proxy_service.proxy_get(
        db,
        partner=partner,
        proxy_path=f"/proxy/todos/{todo_id}",
        upstream_path=f"todos/{todo_id}",
    )


@router.get("/albums")
async def proxy_albums(
    partner: Partner = Depends(get_current_partner),
    db: AsyncSession = Depends(get_db),
):
    return await proxy_service.proxy_get(
        db,
        partner=partner,
        proxy_path="/proxy/albums",
        upstream_path="albums",
    )


@router.get("/albums/{album_id}")
async def proxy_album_detail(
    album_id: int,
    partner: Partner = Depends(get_current_partner),
    db: AsyncSession = Depends(get_db),
):
    return await proxy_service.proxy_get(
        db,
        partner=partner,
        proxy_path=f"/proxy/albums/{album_id}",
        upstream_path=f"albums/{album_id}",
    )


@router.get("/photos")
async def proxy_photos(
    partner: Partner = Depends(get_current_partner),
    db: AsyncSession = Depends(get_db),
):
    return await proxy_service.proxy_get(
        db,
        partner=partner,
        proxy_path="/proxy/photos",
        upstream_path="photos",
    )


@router.get("/photos/{photo_id}")
async def proxy_photo_detail(
    photo_id: int,
    partner: Partner = Depends(get_current_partner),
    db: AsyncSession = Depends(get_db),
):
    return await proxy_service.proxy_get(
        db,
        partner=partner,
        proxy_path=f"/proxy/photos/{photo_id}",
        upstream_path=f"photos/{photo_id}",
    )
