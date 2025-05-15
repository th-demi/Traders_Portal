from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
import os
import firebase_admin
from firebase_admin import auth as firebase_auth, credentials
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from dotenv import load_dotenv
from companies.models import Company
from watchlist.models import Watchlist
from users.serializers import UserRegistrationSerializer

User = get_user_model()
load_dotenv()


def home_view(request):
    return render(request, 'core/home.html')


def company_list_view(request):
    search_query = request.GET.get('search', '')

    # Base queryset
    companies = Company.objects.all().order_by('company_name')

    # Apply search if provided
    if search_query:
        companies = companies.filter(
            Q(company_name__icontains=search_query) |
            Q(symbol__icontains=search_query)
        )

    # Get user's watchlist companies for highlighting
    user_watchlist = []
    if request.user.is_authenticated:
        watchlist_company_ids = Watchlist.objects.filter(
            user=request.user).values_list('company_id', flat=True)
        user_watchlist = Company.objects.filter(id__in=watchlist_company_ids)

    # Pagination
    paginator = Paginator(companies, 25)  # Show 25 companies per page
    page_number = request.GET.get('page')
    companies_page = paginator.get_page(page_number)

    context = {
        'companies': companies_page,
        'search_query': search_query,
        'user_watchlist': user_watchlist,
    }

    return render(request, 'core/company_list.html', context)


@login_required
def watchlist_view(request):
    watchlist_items = Watchlist.objects.filter(
        user=request.user).select_related('company').order_by('-added_at')

    # Pagination
    paginator = Paginator(watchlist_items, 10)  # Show 10 items per page
    page_number = request.GET.get('page')
    watchlist_page = paginator.get_page(page_number)

    context = {
        'watchlist_items': watchlist_page,
    }

    return render(request, 'core/watchlist.html', context)


@login_required
def add_to_watchlist(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    # Check if already in watchlist
    if not Watchlist.objects.filter(user=request.user, company=company).exists():
        Watchlist.objects.create(user=request.user, company=company)
        messages.success(
            request, f'{company.company_name} added to your watchlist.')
    else:
        messages.info(
            request, f'{company.company_name} is already in your watchlist.')

    # Redirect back to the page they came from, or companies list
    return redirect(request.META.get('HTTP_REFERER', 'company_list'))


@login_required
def remove_from_watchlist(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    # Try to find and delete the watchlist item
    watchlist_item = Watchlist.objects.filter(
        user=request.user, company=company).first()
    if watchlist_item:
        watchlist_item.delete()
        messages.success(
            request, f'{company.company_name} removed from your watchlist.')
    else:
        messages.info(
            request, f'{company.company_name} is not in your watchlist.')

    # Redirect back to the page they came from, or watchlist
    return redirect(request.META.get('HTTP_REFERER', 'watchlist'))


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')

            # Redirect to the page they were trying to access, or home
            next_page = request.GET.get('next', 'home')
            return redirect(next_page)
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'core/login.html')


def register_view(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.POST)
        if serializer.is_valid():
            user = serializer.save()
            messages.success(
                request, 'Account created successfully! You can now log in.')
            return redirect('login')
        else:
            # Format errors for display
            for field, errors in serializer.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    return render(request, 'core/register.html')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


def google_login_view(request):
    return render(request, 'core/google_login.html')


@csrf_exempt
@require_POST
def google_login_callback(request):
    try:
        # Parse JSON data from request body
        data = json.loads(request.body.decode('utf-8'))
        id_token = data.get('id_token')

        if not id_token:
            return JsonResponse({'success': False, 'error': 'No ID token provided'}, status=400)

        # Initialize Firebase Admin if not already initialized
        if not firebase_admin._apps:
            try:
                cred_dict = get_firebase_credentials_from_env()
                cred = credentials.Certificate(cred_dict)
                firebase_admin.initialize_app(cred)
            except Exception as e:
                print(f"Firebase initialization error: {str(e)}")
                return JsonResponse({'success': False, 'error': 'Failed to initialize Firebase'}, status=500)

        try:
            # Verify ID token with error handling
            try:
                # Use check_revoked=False and verify_expiry=True
                # The audience parameter is not needed as we'll verify the token against the FirebaseApp instance
                decoded_token = firebase_auth.verify_id_token(
                    id_token,
                    check_revoked=False
                )
                email = decoded_token.get('email')

                if not email:
                    return JsonResponse({'success': False, 'error': 'No email found in token'}, status=400)

            except ValueError as ve:
                print(f"Token validation error: {str(ve)}")
                return JsonResponse({'success': False, 'error': 'Invalid token format'}, status=400)

            except firebase_auth.InvalidIdTokenError as ie:
                print(f"Invalid ID token: {str(ie)}")
                return JsonResponse({'success': False, 'error': 'Invalid ID token'}, status=400)

            # Get or create user
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    # Use part before @ as username
                    'username': email.split('@')[0],
                    'first_name': decoded_token.get('name', '').split(' ')[0] if decoded_token.get('name') else '',
                    'last_name': ' '.join(decoded_token.get('name', '').split(' ')[1:]) if decoded_token.get('name', '') and len(decoded_token.get('name', '').split(' ')) > 1 else ''
                }
            )

            # Log the user in
            login(request, user)

            return JsonResponse({'success': True})

        except Exception as e:
            print(f"Token verification error: {str(e)}")
            return JsonResponse({'success': False, 'error': f'Failed to verify token: {str(e)}'}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return JsonResponse({'success': False, 'error': f'An unexpected error occurred: {str(e)}'}, status=500)


def get_firebase_credentials_from_env():
    return {
        "type": os.environ.get("FIREBASE_TYPE"),
        "project_id": os.environ.get("FIREBASE_PROJECT_ID"),
        "private_key_id": os.environ.get("FIREBASE_PRIVATE_KEY_ID"),
        "private_key": os.environ.get("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
        "client_email": os.environ.get("FIREBASE_CLIENT_EMAIL"),
        "client_id": os.environ.get("FIREBASE_CLIENT_ID"),
        "auth_uri": os.environ.get("FIREBASE_AUTH_URI"),
        "token_uri": os.environ.get("FIREBASE_TOKEN_URI"),
        "auth_provider_x509_cert_url": os.environ.get("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": os.environ.get("FIREBASE_CLIENT_X509_CERT_URL"),
        "universe_domain": os.environ.get("FIREBASE_UNIVERSE_DOMAIN"),
    }
