from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import string
import random
from .serializers import EmailAndPasswordSerializer
from .emails import send_password_to_email

# Create your views here.



class GeneratePasswordView(APIView):
    def post(self, request):
        try:
            length = request.data.get('length', 12)
            choice = request.data.get('choice', ["uppercase", "lowercase", "numbers", "special"])
            
            if not isinstance(length, int) or not isinstance(choice, list):
                return Response({'error':'invalid input'},status=status.HTTP_400_BAD_REQUEST)
            
            characters = ''
            
            if "uppercase" in choice:
                characters += string.ascii_uppercase
            if "lowercase" in choice:
                characters += string.ascii_lowercase
            if "numbers" in choice:
                characters += string.digits
            if "special" in choice:
                characters += string.punctuation
            if "emojis" in choice:
                characters += "😀😍🔒🌟🎉🚀🔑🌈"
            if "math" in choice:
                characters += "+-*/=^"   
                
            password = ''.join(random.choice(characters) for i in range(length))   
            
            response = {
                'password':password,
                'message':'password created succesfully',

            } 
            
            return Response(response,status=status.HTTP_201_CREATED)
        
        except Exception as e:
            response = {
                'error':f'an error occured : {str(e)}',
                'message':'password generation failed'
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class SendPasswordView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = EmailAndPasswordSerializer(data=data)

            if serializer.is_valid():
                email = serializer.data["email"]
                password = serializer.data["password"]

                send_password_to_email(email=email, password=password)

                response = {
                    "message": "Password sent to email successfully",
                    "status": "success",
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    "data": serializer.errors,
                    "message": "Something went wrong. Please retry.",
                    "status": "fail",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            response = {
                "message": f"An error occurred: {str(e)}",
                "status": "error",
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        