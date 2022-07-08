from typing import Tuple, Optional, List, Dict

from internals.toolkit import validate_error, existence_error, ERROR
from apps.reason.serializers import ReasonSerializer
from apps.reason.models import Reason

# --------------------- create ---------------------


def create_reason(data: Dict) -> Tuple[Optional[Dict], ERROR]:
    reason_serialized = ReasonSerializer(data=data)
    if not reason_serialized.is_valid():
        err = validate_error(reason_serialized.errors)
        return None, err
    reason_serialized.save()

    return reason_serialized.data, None


# --------------------- get ---------------------


def get_reason_objs() -> Tuple[List[Reason], ERROR]:
    reasons = Reason.objects.all()
    return reasons, None


def get_reason_obj(_id: int) -> Tuple[Optional[Reason], ERROR]:
    try:
        reason = Reason.objects.get(id=_id)
    except Exception:
        return None, existence_error('Reason')
    return reason, None


def get_data(reason: Reason) -> Tuple[Dict, ERROR]:
    reason_serialized = ReasonSerializer(reason)
    return reason_serialized.data, None


def get_data_list(reasons: List[Reason]) -> Tuple[List[Dict], ERROR]:
    reason_serialized = ReasonSerializer(reasons, many=True)
    return reason_serialized.data, None


# --------------------- delete ---------------------


def delete(_id: int) -> ERROR:
    try:
        Reason.objects.get(id=_id).delete()
    except Exception:
        return existence_error('Reason')
    return None
