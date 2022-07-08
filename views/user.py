from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import repositories.user as repo_user
from internals.toolkit import response_creator


class SignUp(APIView):
    def post(self, request):
        mobile_number = request.data.get('mobile_number').strip()
        password = request.data.get('password')

        if not repo_user.mobile_number_validator(mobile_number):
            return Response(
                {
                    'status': 'fail',
                    'message': 'invalid mobile number.',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        repo_user.create_user(
            name=request.data.get('name'),
            mobile_number=mobile_number,
            password=password,
        )

        return response_creator(
            data='user created successfully.',
            status='success',
            status_code=status.HTTP_201_CREATED,
        )


class SignIn(APIView):
    def post(self, request):
        password = request.data.get('password')
        mobile_number = request.data.get('mobile_number').strip()

        if not repo_user.mobile_number_validator(mobile_number):
            return Response(
                {
                    'status': 'fail',
                    'message': 'permission denied.',
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        user_obj, err = repo_user.get_user_obj_by_mobile_number(
            mobile_number=mobile_number,
        )
        if err:
            return err

        if not user_obj.check_password(password):
            return Response(
                {'status': 'fail', 'message': 'permission denied.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        token = repo_user.create_token(user_obj)
        return response_creator(
            data={'token': token},
            status='success',
            status_code=200,
        )


class Users(APIView):
    def get(self):
        users, err = repo_user.get_user_objs()
        if err:
            return err

        users_data, err = repo_user.get_user_all_data(users)
        if err:
            return err

        return response_creator(
            data=users_data,
            status='success',
            status_code=status.HTTP_200_OK,
        )
