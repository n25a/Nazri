from rest_framework.views import APIView
from rest_framework import status

import repositories.reason as repo_reason
from internals.toolkit import response_creator


class AddReason(APIView):
    def post(self, request):
        reason, err = repo_reason.create_reason(data=request.data)
        if err:
            return err
        return response_creator(
            data=reason,
            status='success',
            status_code=status.HTTP_201_CREATED,
        )


class GetReasons(APIView):
    def get(self, request):
        reasons, err = repo_reason.get_reason_objs()
        if err:
            return err

        reasons_data, err = repo_reason.get_data_list(reasons)
        if err:
            return err

        return response_creator(
            data=reasons_data,
            status='success',
            status_code=status.HTTP_200_OK,
        )


class DeleteReason(APIView):
    def delete(self, request):
        _id = request.data.get('id')

        err = repo_reason.delete(_id)
        if err:
            return err

        return response_creator(
            data=f'reason {_id} deleted',
            status='success',
            status_code=status.HTTP_200_OK,
        )
