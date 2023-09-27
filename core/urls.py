from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import budget_views, expense_views, auth_views  # and any other modules you have

urlpatterns = [
    path('', budget_views.home, name='home'),
    path('login/', auth_views.login_view, name='login'),
    path('signup/', auth_views.signup_view, name='signup'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('profile/', auth_views.profile_view, name='profile'),
    path('profile/edit/', auth_views.edit_profile, name='edit_profile'),
    path('budgets/', budget_views.budget_list, name='budget_list'),
    path('budgets/create/', budget_views.budget_create, name='budget_create'),
    path('budgets/<int:budget_id>/', budget_views.budget_detail, name='budget_detail'),
    path('budgets/<int:budget_id>/edit/', budget_views.edit_budget, name='edit_budget'),
    path('budgets/<int:budget_id>/delete/', budget_views.delete_budget, name='delete_budget'),
    path('budgets/<int:budget_id>/expense/', expense_views.expense_create, name='expense_create'),
    path('expenses/<int:expense_id>/edit/', expense_views.edit_expense, name='edit_expense'),
    path('expenses/<int:expense_id>/delete/', expense_views.delete_expense, name='delete_expense'),
]

if settings.DEBUG:  # Only serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)