from typing import Tuple, Optional, List, Dict
from copy import deepcopy

from rest_framework.authtoken.models import Token

from internals.toolkit import validate_error, existence_error, ERROR
from apps.user.serializers import CustomUserSerializer
from apps.user.models import CustomUser

# ---------------------- mobile_number validation ----------------------------


def mobile_number_validator(mobile_number: str) -> bool:
    if (
        (mobile_number is not None)
        and (mobile_number[0:2] == '09')
        and (len(mobile_number) == 11)
    ):
        return True
    return False


# --------------------------- Create -------------------------------


def create_token(user_obj: object) -> str:
    token, _ = Token.objects.get_or_create(user=user_obj)
    token_value = f'Token {token.key}'
    return token_value


def create_user(name: str, mobile_number: str, password: str) -> CustomUser:
    user_obj = CustomUser.objects.create_user(
        name=name,
        mobile_number=mobile_number,
        password=password,
    )
    return user_obj


#
# def upload_avatar(data: Dict) -> Tuple[Optional[dict], ERROR]:
#     err = None
#
#     avatar_serialized = CostumUserAvatarSerializer(
#         data=data,
#     )
#
#     if not avatar_serialized.is_valid():
#         err = validate_error(avatar_serialized)
#         return None, err
#     avatar_serialized.save()
#
#     return avatar_serialized.data, err


# --------------------------- GET ----------------------------------


def get_user_obj_by_mobile_number(
    mobile_number: str,
) -> Tuple[Optional[CustomUser], ERROR]:
    err = None
    user_obj = CustomUser.objects.filter(mobile_number=mobile_number).first()
    if user_obj is None:
        err = existence_error('CustomUser')
        return None, err

    return user_obj, err


def get_user_obj_by_id(_id: int) -> Tuple[Optional[CustomUser], ERROR]:
    err = None
    user_obj = CustomUser.objects.filter(id=_id).first()
    if user_obj is None:
        err = existence_error('CustomUser')
        return None, err

    return user_obj, err


def get_user_data(user_obj: object) -> Tuple[Optional[dict], ERROR]:
    err = None
    if user_obj is None:
        err = existence_error('CustomUser')
        return None, err

    user_serialized = CustomUserSerializer(user_obj)
    return user_serialized.data, err


def get_user_objs() -> Optional[List[CustomUser]]:
    user_objs = CustomUser.objects.all()
    return user_objs


def get_user_all_data(
    user_objs: List[CustomUser],
) -> Tuple[Optional[List[CustomUser]], ERROR]:
    err = None

    if user_objs.count() == 0:
        err = existence_error('CustomUser')
        return None, err

    users_serialized = CustomUserSerializer(
        user_objs,
        many=True,
    )

    return users_serialized.data, err


# --------------------------- update --------------------------------


def update_user(user_obj: object, data: Dict) -> Tuple[Optional[dict], ERROR]:
    err = None

    copy_data = deepcopy(data)
    if copy_data['password']:
        copy_data['password'].drop()

    user_serialized = CustomUserSerializer(
        user_obj,
        data=data,
        partial=True,
    )
    if not user_serialized.is_valid():
        err = validate_error(user_serialized)
        return None, err
    user_serialized.save()

    return user_serialized.data, err


def rate_zeroer(user_id: int) -> ERROR:
    user_obj = CustomUser.objects.filter(id=user_id).first()
    if user_obj is None:
        err = existence_error('CustomUser')
        return err

    user_serialized = CustomUserSerializer(user_obj, data={'rate': 0}, partial=True)
    if not user_serialized.is_valid():
        err = validate_error(user_serialized)
        return err
    user_serialized.save()

    return None


# ---------------------------  Set new Password -------------------------------


def set_password(user_obj: object, data: Dict) -> Tuple[Optional[dict], ERROR]:
    err = None

    user_serialized = CustomUserSerializer(
        user_obj,
        data=data,
        partial=True,
    )
    if not user_serialized.is_valid():
        err = validate_error(user_serialized)
        return None, err
    user_serialized.save()

    return user_serialized.data, err
