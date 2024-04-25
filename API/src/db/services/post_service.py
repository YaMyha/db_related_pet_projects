import re

from sqlalchemy import select

from db.database import async_session_factory
from db.modelsORM import User, Post


class PostService:
    @staticmethod
    async def insert_post(author_id: int, title: str, description: str, tags: str = None):
        async with async_session_factory() as session:
            post = Post(author_id=author_id, title=title, description=description, tags=tags)
            session.add(post)
            await session.flush()
            post_id = post.id
            await session.commit()
            return post_id

    @staticmethod
    async def select_posts():
        async with async_session_factory() as session:
            query = select(Post)
            result = await session.execute(query)
            posts = result.scalars().all()
            return posts

    @staticmethod
    async def select_posts_by_author(author_name: str):
        async with async_session_factory() as session:
            """select *
                from posts
                where author_id in (
                    select id
                    from users
                    where username like '%Steven%'
                );"""
            subquery = select(User.id).select_from(User).filter(User.username.contains(author_name))
            query = select(Post).select_from(Post).filter(Post.author_id.in_(subquery))

            result = await session.execute(query)
            posts = result.scalars().all()
            return posts

    @staticmethod
    async def select_posts_by_tags(tags: str):
        async with async_session_factory() as session:
            """select *
                from posts
                WHERE tags ~* '(?=.*(\W|^)secrets(\W|$))(?=.*(\W|^)men(\W|$)).*';"""
            tags = re.findall(r'\w+', tags)
            print(tags)
            tags.append('.*')
            regex_pattern = ''.join(fr"(?=.*(\W|^){tag}(\W|$))" for tag in tags)

            query = select(Post).where(Post.tags.regexp_match(regex_pattern.replace('\\\\', '\\')))
            result = await session.execute(query)
            posts = result.scalars().all()
            return posts

    @staticmethod
    async def update_post(post_id: int, attrs: dict = None):
        async with async_session_factory() as session:
            post = await session.get(Post, post_id)
            if attrs:
                for key, value in attrs.items():
                    if key:
                        setattr(post, key, value)
                        await session.commit()

    @staticmethod
    async def delete_post(post_id: int):
        async with async_session_factory() as session:
            post = await session.get(Post, post_id)
            if post:
                print("________________________")
                await session.delete(post)
                await session.commit()