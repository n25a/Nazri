from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status

import repositories.user as repo_user
import repositories.penalty as repo_penalty
from internals.toolkit import response_creator
from apps.user.serializers import CustomUserSerializer
from apps.user.permissions import IsAdmin
from apps.user.models import CustomUser

max_penalty_level = 11
max_penalty_number = 8


class Penalty(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
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

        reason_id = request.data.get('reason_id')
        user_id = request.data.get('user_id')
        rate = request.data.get('level')

        err = repo_penalty.create_penalty(
            {
                'user': user_id,
                'level': rate,
                'reason': reason_id,
            }
        )
        if err:
            return err

        penalizing(user_id=user_id)

        # TODO: send notification to user

        return response_creator(
            data='penalty added successfully.',
            status='success',
            status_code=status.HTTP_201_CREATED,
        )


class GetPenalties(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        penalties, err = repo_penalty.get_penalty_objs()
        if err:
            return err

        penalties_data, err = repo_penalty.get_deep_data_list(penalties)
        if err:
            return err

        return response_creator(
            data={'penalties': penalties_data},
            status='success',
            status_code=status.HTTP_200_OK,
        )


class NazriGiver(APIView):
    def get(self):
        user_objs = CustomUser.objects.filter(rate__gte=1)
        user_serialized = CustomUserSerializer(user_objs, many=True)
        return response_creator(
            data={'nazri_givers': user_serialized.data},
            status='success',
            status_code=status.HTTP_200_OK,
        )


class Pay(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request):
        user_id = request.data.get('user_id')

        err = repo_penalty.pay_penalty(user_id)
        if err:
            return err

        err = repo_user.rate_zeroer(user_id)
        if err:
            return err

        # TODO: send notification to user

        return response_creator(
            data='penalty payed successfully.',
            status='success',
            status_code=status.HTTP_200_OK,
        )
