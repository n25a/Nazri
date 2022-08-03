from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status

import repositories.user as repo_user
import repositories.penalty as repo_penalty
from internals.toolkit import response_creator
from internals.jobs import penalizing
from apps.user.serializers import CustomUserSerializer
from apps.user.permissions import IsAdmin
from apps.user.models import CustomUser


class Penalty(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
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

        penalizing.apply_async(eta=user_id)

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
