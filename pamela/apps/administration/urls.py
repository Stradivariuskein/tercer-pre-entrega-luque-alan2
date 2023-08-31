from django.urls import path, include 

from .views import TypeSessionCreate, TypeSessionUpdate, TypeSessionDelete, AcountListView, AccountUpdate, AccountDelet, TurnUpdate, view_typeSession, admin_turn, turnCreate

from decorators import add_general_context, admin_only
from .views import HomeUpdate, HomeSectionCreate, HomeSectionUpdate, HomeSectionDelete, home_edit


urlpatterns = [
    path('typeSession/', admin_only(add_general_context(view_typeSession)), name= "typeSession"),
    path('typeSession/create/', admin_only(add_general_context(TypeSessionCreate.as_view())), name= "typeSession-create"),
    path('typeSession/update/<int:pk>/', admin_only(add_general_context(TypeSessionUpdate.as_view())), name= "typeSession-update"),
    path('typeSession/delete/<int:pk>/', admin_only(add_general_context(TypeSessionDelete.as_view())), name= "typeSession-delete"),

    path('cuentas/', admin_only(add_general_context(AcountListView.as_view())), name= "cuentas"),
    path('cuentas/update/<int:pk>/', admin_only(add_general_context(AccountUpdate.as_view())), name= "account-update"),
    path('cuentas/delete/<int:pk>/', admin_only(add_general_context(AccountDelet.as_view())), name= "account-delete"),

    path('home/edit', admin_only(add_general_context(home_edit)), name='home-edit'),
    path('home/update/<int:pk>/', admin_only(add_general_context(HomeUpdate.as_view())), name='home-update'),
    path('home/section/create/', admin_only(add_general_context(HomeSectionCreate.as_view())), name='home-section-create'),
    path('home/section/update/<int:pk>/', admin_only(add_general_context(HomeSectionUpdate.as_view())), name='home-section-update'),
    path('home/section/delete/<int:pk>/', admin_only(add_general_context(HomeSectionDelete.as_view())), name='home-section-delete'),

    path('turns/<int:p_week>/', admin_only(add_general_context(admin_turn)), name='admin_turn'),
    path('edit-turn/<int:pk>/', admin_only(add_general_context(TurnUpdate.as_view())), name='turn-update'),
    path('turns/create/', admin_only(add_general_context(turnCreate)), name='admin_create_turn'),
    ]

