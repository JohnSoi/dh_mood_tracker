"""Модуль общих валидаторов данных"""

__author__: str = "Digital Horizons"

import re

from dh_mood_tracker.utils.consts import EMAIL_PATTERN


def email_validator(email: str) -> bool:
    """
    Валидатор адреса электронной почты

    :param email: электронная почта
    :type email: str
    :return: признак валидного email`а
    :rtype: bool

    .. code-block:: python
        from fastapi import HTTPException, status

        if not email_validator("<EMAIL>"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Неверный адрес электронной почты",
            )
    """
    return bool(re.match(EMAIL_PATTERN, email))
