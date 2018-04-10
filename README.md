# Non True Awaitable

Awaitable objects in Python, such as coroutines, evaluate to `True` in Python.

This can cause problems when a coroutine function returns a boolean value, especially if it is security critical, such as a coroutine function that checks a user password.

Non True Awaitable aims at making such coroutine functions a little safer, by making their returned coroutine evaluate to `False`. In other words, unawaited coroutine functions evaluate to `False`. 

Take the following code:

```python
async def check_user_password(username: str, password: str) -> bool:
    user = await get_user_from_db(username)
    password_hash = hash_password(password)
    return constant_time_compare(user.password_hash, password_hash)


async def login(request):
    if check_user_password(request.username, request.password):
        set_secure_cookie("user", request.username)
        return redirect("/secret/")

    else:
        return error("wrong username or password")
```

Can you spot the mistake? The login function does not actually await the `check_user_password` coroutine and will accept any username and password as valid!

Your automated test suite *should* catch this bug, but in case it doesn't it could have horrendous results.

If instead you use Non True Awaitable, the scenario gets less scary:

```python

from nta import nta


@nta
async def check_user_password(username: str, password: str) -> bool:
    user = await get_user_from_db(username)
    password_hash = hash_password(password)
    return constant_time_compare(user.password_hash, password_hash)


async def login(request):
    if check_user_password(request.username, request.password):
        set_secure_cookie("user", request.username)
        return redirect("/secret/")

    else:
        return error("wrong username or password")
```

Now, no login will be accepted. This is still not good, but a better default than allowing everyone access.

For completeness sake, here is the correct code:

```python
from nta import nta


@nta
async def check_user_password(username: str, password: str) -> bool:
    user = await get_user_from_db(username)
    password_hash = hash_password(password)
    return constant_time_compare(user.password_hash, password_hash)


async def login(request):
    if await check_user_password(request.username, request.password):
        set_secure_cookie("user", request.username)
        return redirect("/secret/")

    else:
        return error("wrong username or password")

```