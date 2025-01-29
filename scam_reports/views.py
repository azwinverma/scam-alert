from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics
from .models import ScamReport, Comment, Reaction
from .serializers import ScamReportSerializer, CommentSerializer, ReactionSerializer,ScamReportImage
from .forms import CommentForm, ReactionForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser



class ScamReportCreateView(APIView):
    parser_classes = (MultiPartParser, FormParser)  # To handle file uploads


@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def addScamReport(request):
    title = request.data.get("title")
    description = request.data.get("description")
    images = request.FILES.getlist("images")  # List of images

    if not title or not description:
        return JsonResponse(
            {"status": "error", "message": "Title and description are required."},
            status=400,
        )

    scam_report = ScamReport.objects.create(
        title=title,
        description=description,
        # reported_by=request.user,
    )

    for image in images:
        ScamReportImage.objects.create(scam_report=scam_report, image=image)

    serializer = ScamReportSerializer(scam_report)
    return JsonResponse(
        {"status": "success", "message": "Scam report created successfully.", "data": serializer.data},
        status=201,
    )

# def addScamReport(self, request, *args, **kwargs):
#         title = request.data.get('title')
#         description = request.data.get('description')
#         # links = request.data.getlist('links[]')  # List of links
#         images = request.FILES.getlist('images')  # List of images

#         if not title or not description:
#             return Response({
#                 "status": "error",
#                 "message": "Title and description are required."
#             }, status=status.HTTP_400_BAD_REQUEST)

#         scam_report = ScamReport.objects.create(
#             title=title,
#             description=description,
#             reported_by=request.user
#         )

#         # Add links
#         # for link in links:
#         #     ScamReportLink.objects.create(scam_report=scam_report, url=link)

#         # Add images
#         for image in images:
#             ScamReportImage.objects.create(scam_report=scam_report, image=image)

#         serializer = ScamReportSerializer(scam_report)
#         return Response({
#             "status": "success",
#             "message": "Scam report created successfully.",
#             "data": serializer.data
#         }, status=status.HTTP_201_CREATED)
#         # serializer = ScamReportSerializer(data=request.data)
#         # if serializer.is_valid():
#         #     serializer.save()
#         #     # Wrap the response in a custom format
#         #     response_data = {
#         #         "status": "success",
#         #         "message": "Scam report created successfully",
#         #         "data": serializer.data
#         #     }
#         #     return Response(response_data, status=status.HTTP_201_CREATED)
#         # # Handle validation errors
#         # response_data = {
#         #     "status": "error",
#         #     "message": "Invalid data",
#         #     "errors": serializer.errors
#         # }
#         # return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

class ScamReportListCreateView(generics.ListCreateAPIView):
    queryset = ScamReport.objects.all()
    serializer_class = ScamReportSerializer
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        # Wrap the response in a custom format
        response_data = {
            "status": "success",
            "message": "Scam reports retrieved successfully",
            "data": response.data
        }
        return Response(response_data)

class ScamReportDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ScamReport.objects.all()
    serializer_class = ScamReportSerializer

class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        scam_report = ScamReport.objects.get(id=self.kwargs['scam_report_id'])
        serializer.save(scam_report=scam_report, commented_by=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        # Wrap the response in a custom format
        response_data = {
            "status": "success",
            "message": "Comment added successfully",
            "data": response.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

class ReactionCreateView(generics.CreateAPIView):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer

    def perform_create(self, serializer):
        scam_report = ScamReport.objects.get(id=self.kwargs['scam_report_id'])
        serializer.save(scam_report=scam_report, reacted_by=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        # Wrap the response in a custom format
        response_data = {
            "status": "success",
            "message": "Reaction added successfully",
            "data": response.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    

class UserRegistrationView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not username or not password:
            return Response({
                "status": "error",
                "message": "Username and password are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({
                "status": "error",
                "message": "Username already exists."
            }, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)

        # Generate tokens for the new user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response({
            "status": "success",
            "message": "User registered successfully.",
            "data": {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            }
        }, status=status.HTTP_201_CREATED)
    


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            # Extract the username from the request
            username = request.data.get('username')
            # Fetch the user object
            user = User.objects.get(username=username)

            # Wrap the response in a custom format
            response_data = {
                "status": "success",
                "message": "User logged in successfully",
                "data": {
                    "access_token": response.data['access'],
                    "refresh_token": response.data['refresh'],
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                    }
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)

        # Handle invalid credentials
        return Response({
            "status": "error",
            "message": "Invalid credentials",
            "errors": response.data
        }, status=status.HTTP_400_BAD_REQUEST)


    
# class UserRegistrationView(generics.CreateAPIView):
#     serializer_class = UserRegistrationSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 "status": "success",
#                 "message": "User registered successfully",
#                 "data": serializer.data
#             }, status=status.HTTP_201_CREATED)
#         return Response({
#             "status": "error",
#             "message": "Invalid data",
#             "errors": serializer.errors
#         }, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            return Response({
                "status": "success",
                "message": "User logged in successfully",
                "data": response.data
            })
        return Response({
            "status": "error",
            "message": "Invalid credentials",
            "errors": response.data
        }, status=status.HTTP_400_BAD_REQUEST)

# def add_comment(request, pk):
#     scam_report = get_object_or_404(ScamReport, pk=pk)
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.scam_report = scam_report
#             comment.user = request.user
#             comment.save()
#             return redirect('admin:scam_report_change', pk=scam_report.pk)
#     else:
#         form = CommentForm()
#     return redirect('admin:scam_report_change', pk=scam_report.pk)

# def add_reaction(request, pk):
#     scam_report = get_object_or_404(ScamReport, pk=pk)
#     if request.method == 'POST':
#         form = ReactionForm(request.POST)
#         if form.is_valid():
#             reaction = form.save(commit=False)
#             reaction.scam_report = scam_report
#             reaction.user = request.user
#             reaction.save()
#             return redirect('admin:scam_report_change', pk=scam_report.pk)
#     else:
#         form = ReactionForm()
#     return redirect('admin:scam_report_change', pk=scam_report.pk)