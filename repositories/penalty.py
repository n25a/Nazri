from typing import Tuple, Optional, List, Dict

from internals.toolkit import validate_error, existence_error, ERROR
from apps.penalty.serializers import PenaltySerializer, PenaltyDeepSerializer
from apps.penalty.models import Penalty

# --------------------- create ---------------------


def create_penalty(data: Dict) -> Tuple[Optional[Dict], ERROR]:
    penalty_serialized = PenaltySerializer(data=data)
    if not penalty_serialized.is_valid():
        err = validate_error(penalty_serialized)
        return None, err
    penalty_serialized.save()

    return penalty_serialized.data, None


# --------------------- get ---------------------


def get_penalty_objs() -> Tuple[List[Penalty], ERROR]:
    penaltys = Penalty.objects.filter(payed=False)
    return penaltys, None


def get_penalty_obj(_id: int) -> Tuple[Optional[Penalty], ERROR]:
    try:
        penalty = Penalty.objects.get(id=_id)
    except Exception:
        return None, existence_error('Penalty')
    return penalty, None


def get_penalty_objs_by_user_id(
    user_id: int,
) -> Tuple[Optional[List[Penalty]], ERROR]:
    try:
        penalties = Penalty.objects.filter(user=user_id)
    except Exception:
        return None, existence_error('Penalty')
    return penalties, None


def get_data(penalty: Penalty) -> Tuple[Dict, ERROR]:
    penalty_serialized = PenaltySerializer(penalty)
    return penalty_serialized.data, None


def get_deep_data_list(penaltys: List[Penalty]) -> Tuple[List[Dict], ERROR]:
    penalty_serialized = PenaltyDeepSerializer(penaltys, many=True)
    return penalty_serialized.data, None


def get_data_list(penalties: List[Penalty]) -> Tuple[List[Dict], ERROR]:
    penalty_serialized = PenaltySerializer(penalties, many=True)
    return penalty_serialized.data, None


# --------------------- delete ---------------------


def delete(_id: int) -> ERROR:
    try:
        Penalty.objects.get(id=_id).delete()
    except Exception:
        return existence_error('Penalty')
    return None


# --------------------- patch ---------------------


def pay_penalty(user_id: int) -> ERROR:
    penalties = Penalty.objects.filter(user=user_id, payed=False)

    for penalty in penalties:
        penalty_serialized = PenaltySerializer(penalty, data={'payed': True}, partial=True)
        if not penalty_serialized.is_valid():
            err = validate_error(penalty_serialized)
            return err
        penalty_serialized.save()

    return None
