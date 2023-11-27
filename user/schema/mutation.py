"""User schema mutations."""
from typing import (
    TYPE_CHECKING,
    Optional,
    Type,
    cast,
)

from django.contrib import (
    auth,
)

import strawberry
from graphql import (
    GraphQLResolveInfo,
)

from user.services.user import user_sign_up

from ..emails import (
    UserPasswordResetEmail,
)
from . import (
    types,
)

if TYPE_CHECKING:
    from ..models import User as _User  # noqa: F401


@strawberry.input
class SignupInput:
    """Signup input."""

    email: str
    password: str


@strawberry.input
class EmailConfirmationInput:
    """EmailConfirmation input."""

    email: str
    token: str


@strawberry.input
class LoginInput:
    """Login input."""

    email: str
    password: str


@strawberry.input
class RequestPasswordResetInput:
    """RequestPasswordReset input."""

    email: str


@strawberry.input
class ConfirmPasswordResetInput:
    """ConfirmPasswordReset input."""

    email: str
    token: str
    new_password: str


@strawberry.input
class UpdateProfileInput:
    """UpdateProfile input."""

    full_name: str


@strawberry.type
class Mutation:
    """."""

    @strawberry.mutation
    def signup(self, input: SignupInput) -> types.User:
        """Mutate."""
        return user_sign_up(
            email=input.email,
            password=input.password,
        )  # type: ignore[return-value]

    @strawberry.mutation
    def email_confirmation(
        self,
        input: EmailConfirmationInput,
    ) -> types.User | None:
        """Mutate."""
        User = cast(Type["_User"], auth.get_user_model())
        user = User.objects.get_by_natural_key(input.email)
        if user.check_email_confirmation_token(input.token):
            user.is_active = True
            user.save()
            return user  # type: ignore
        return None

    @strawberry.mutation
    def login(
        self, input: LoginInput, info: GraphQLResolveInfo
    ) -> types.User | None:
        """Mutate."""
        from django.contrib.auth.backends import (
            ModelBackend,
        )

        user = cast(
            "Optional[_User]",
            ModelBackend().authenticate(
                info.context,
                username=input.email,
                password=input.password,
            ),
        )
        if user is None:
            return None
        auth.login(
            info.context,
            user,
            backend="django.contrib.auth.backends.ModelBackend",
        )
        return user  # type: ignore

    @strawberry.mutation
    def logout(self, info: GraphQLResolveInfo) -> types.User | None:
        """Mutate."""
        user = cast("_User", info.context.user)
        if user.is_anonymous:
            return None
        auth.logout(info.context)
        return user  # type: ignore

    @strawberry.mutation
    def request_password_reset(self, input: RequestPasswordResetInput) -> str:
        """Mutate."""
        User = cast(Type["_User"], auth.get_user_model())
        user = User.objects.get_by_natural_key(input.email)
        password_reset_email = UserPasswordResetEmail(user)
        password_reset_email.send()
        return input.email

    @strawberry.mutation
    def confirm_password_reset(
        self,
        input: ConfirmPasswordResetInput,
    ) -> types.User | None:
        """Mutate."""
        User = cast(Type["_User"], auth.get_user_model())
        user = User.objects.get_by_natural_key(input.email)
        if user.check_password_reset_token(input.token):
            user.set_password(input.new_password)
            user.save()
            return user  # type: ignore
        return None

    @strawberry.mutation
    def update_profile(
        self,
        input: UpdateProfileInput,
        info: GraphQLResolveInfo,
    ) -> types.User | None:
        """Mutate."""
        user = cast("_User", info.context.user)
        if not user.is_authenticated:
            return None
        user.full_name = input.full_name
        user.save()
        return user  # type: ignore
