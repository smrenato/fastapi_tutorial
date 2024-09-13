from sqlalchemy import select

from fastapi_tutorial.models import User

#
# def test_create_user_ondb(session):
#     user = User(
#         username='teste',
#         password='12345',
#         email='test@email.com',
#     )
#     session.add(user)
#     session.commit()
#
#     result = session.scalar(
#         select(User).where(User.email == 'email@email.com')
#     )
#     assert result.email == 'email@email.com'
