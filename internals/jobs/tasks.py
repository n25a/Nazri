from celery.decorators import task

import repositories.penalty as repo_penalty
from apps.user.serializers import CustomUserSerializer
from apps.user.models import CustomUser
from apps.penalty.models import Penalty

max_penalty_level = 11
max_penalty_number = 8


@task(name='penalizing')
def penalizing(user_id: int):
    """
    This task is used to penalize a user.
    """
    user_obj = CustomUser.objects.get(id=user_id)
    penalty_obj = Penalty.objects.filter(user=user_obj, paid=False)
    if penalty_obj.count() == 0:
        return Exception('No penalty found for this user.')

    penalty_data, err = repo_penalty.get_data_list(penalty_obj)
    if err:
        return err

    new_rate = 0
    if penalty_obj.count() / max_penalty_number > 1:
        new_rate = penalty_obj.count() / max_penalty_number
    else:
        for penalty in penalty_data:
            new_rate += penalty['level'] / max_penalty_level

    user_serialized = CustomUserSerializer(user_obj, data={'rate': new_rate})
    if not user_serialized.is_valid():
        return Exception('User serializer is not valid.')
    user_serialized.save()

    return None
