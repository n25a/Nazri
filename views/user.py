from copy import deepcopy

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.authentication import TokenAuthentication
from rest_framework import status

import repositories.user as repo_user
from toolkit.toolkit import response_creator


class SignUp(APIView):
    def post(self, request):

        mobile_number = request.data.get("mobile_number").strip()
        password = request.data.get("password")

        if not repo_user.mobile_number_validator(mobile_number):
            return Response(
                {
                    "status": "fail",
                    "message": "invalid mobile number.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        repo_user.create_user(
            name=request.data.get("name"),
            mobile_number=mobile_number,
            password=password,
        )

        return response_creator(
            data="user created successfully.",
            status="success",
            status_code=status.HTTP_201_CREATED,
        )


class SignIn(APIView):
    def post(self, request):

        password = request.data.get("password")
        mobile_number = request.data.get("mobile_number").strip()

        if not repo_user.mobile_number_validator(mobile_number):
            return Response(
                {
                    "status": "fail",
                    "message": "permission denied.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        user_obj, err = repo_user.get_user_obj_by_mobile_number(
            mobile_number=mobile_number,
        )
        if err:
            return err

        if user_obj.check_password(password):
            token = repo_user.create_token(user_obj)
            return response_creator(
                data={"token": token},
                status="success",
                status_code=200,
            )

        return Response(
            {"status": "fail", "message": "permission denied."},
            status=status.HTTP_403_FORBIDDEN,
        )


class UploadAvatar(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):

        data = deepcopy(request.data)
        data["user"] = request.user.id

        avatar_data, err = repo_user.upload_avatar(
            data=request.data,
        )
        if err:
            return err

        return response_creator(
            data={"avatar": avatar_data},
            status="success",
            status_code=status.HTTP_201_CREATED,
        )


class DeleteAvatar(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):

        err = repo_user.delete_avatar(
            user_id=request.user.id,
        )
        if err:
            return err

        return Response(status=status.HTTP_204_NO_CONTENT)
