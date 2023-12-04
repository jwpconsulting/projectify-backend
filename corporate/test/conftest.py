"""Corporate conftest."""

import pytest
from faker import Faker

from corporate.models import Customer
from corporate.services.customer import (
    customer_activate_subscription,
    customer_create,
)
from user.models import User
from workspace.models.const import WorkspaceUserRoles
from workspace.models.workspace import Workspace
from workspace.models.workspace_user import WorkspaceUser
from workspace.services.workspace import workspace_add_user


@pytest.fixture
def stripe_publishable_key(faker: Faker) -> str:
    """Return a convincing looking stripe publishable key."""
    key: str = faker.hexify(
        "pk_test_^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
    )
    return key


@pytest.fixture
def stripe_secret_key(faker: Faker) -> str:
    """Return a convincing looking stripe secret key."""
    key: str = faker.hexify(
        "sk_test_^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
    )
    return key


@pytest.fixture
def stripe_price_object(faker: Faker) -> str:
    """Return a convincing looking stripe price object."""
    key: str = faker.hexify("price_^^^^^^^^^^^^^^^^^^^^^^^^")
    return key


@pytest.fixture
def stripe_endpoint_secret(faker: Faker) -> str:
    """Return a convincing looking stripe endpoint secret."""
    key: str = faker.hexify(
        "whsec_^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
    )
    return key


@pytest.fixture
def workspace(faker: Faker) -> Workspace:
    """Create a workspace."""
    return Workspace.objects.create(title=faker.company())


@pytest.fixture
def workspace_user(user: User, workspace: Workspace) -> WorkspaceUser:
    """Create a workspace user."""
    return workspace_add_user(
        workspace=workspace,
        user=user,
        role=WorkspaceUserRoles.OWNER,
    )


@pytest.fixture
def unpaid_customer(
    workspace_user: WorkspaceUser, workspace: Workspace, faker: Faker
) -> Customer:
    """Create customer."""
    return customer_create(
        who=workspace_user.user,
        workspace=workspace,
        seats=faker.pyint(min_value=1, max_value=98),
    )


@pytest.fixture
def stripe_customer_id(faker: Faker) -> str:
    """Return a convincing stripe customer id."""
    stripe_customer_id: str = faker.bothify("stripe_###???###")
    return stripe_customer_id


@pytest.fixture
def paid_customer(
    unpaid_customer: Customer, stripe_customer_id: str
) -> Customer:
    """Create customer."""
    customer_activate_subscription(
        customer=unpaid_customer,
        stripe_customer_id=stripe_customer_id,
    )
    return unpaid_customer
