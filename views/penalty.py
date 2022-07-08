from rest_framework.views import APIView
from rest_framework import status

import repositories.user as repo_user
import repositories.penalty as repo_penalty
from internals.toolkit import response_creator


class Penalty(APIView):
    def post(self, request):
        reason_id = request.data.get('reason_id')
        user_id = request.data.get('user_id')
        rate = request.data.get('penalty_amount')

        err = repo_penalty.create_penalty(
            {
                'user': user_id,
                'rate': rate,
                'reason': reason_id,
            }
        )
        if err:
            return err

        # TODO: add background job
        # TODO: send notification to user

        return response_creator(
            data='penalty added successfully.',
            status='success',
            status_code=status.HTTP_201_CREATED,
        )


class GetPenalties(APIView):
    def get(self, request):
        penalties, err = repo_penalty.get_penalty_objs()
        if err:
            return err

        penalties_data, err = repo_penalty.get_deep_data_list(penalties)
        if err:
            return err

        return response_creator(
            data=penalties_data,
            status='success',
            status_code=status.HTTP_200_OK,
        )


class Pay(APIView):
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
            data='penalty paid successfully.',
            status='success',
            status_code=status.HTTP_200_OK,
        )
