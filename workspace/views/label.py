"""Label views."""
from uuid import UUID

from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from workspace.models.label import Label
from workspace.models.workspace import Workspace
from workspace.serializers.base import LabelBaseSerializer
from workspace.services.label import label_create, label_update


# Create
class LabelCreate(APIView):
    """View for creating labels."""

    class InputSerializer(serializers.ModelSerializer[Label]):
        """Serializer for label creation."""

        workspace_uuid = serializers.UUIDField()

        class Meta:
            """Meta."""

            fields = "name", "color", "workspace_uuid"
            model = Label

    def post(self, request: Request) -> Response:
        """Create the label."""
        user = request.user
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        workspace_uuid: UUID = data["workspace_uuid"]
        try:
            workspace = Workspace.objects.filter_for_user_and_uuid(
                uuid=workspace_uuid,
                user=user,
            ).get()
        except Workspace.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "workspace_uuid": _(
                        "No workspace could be found for given workspace_uuid"
                    ),
                }
            )
        label = label_create(
            workspace=workspace,
            name=data["name"],
            color=data["color"],
            who=user,
        )
        output_serializer = LabelBaseSerializer(instance=label)
        return Response(output_serializer.data, status=201)


class LabelUpdate(APIView):
    """View for updating labels."""

    class InputSerializer(serializers.ModelSerializer[Label]):
        """Serializer for Label update."""

        class Meta:
            """Meta."""

            fields = "name", "color"
            model = Label

    def put(self, request: Request, label_uuid: UUID) -> Response:
        """Handle PUT."""
        label_qs = Label.objects.filter_for_user_and_uuid(
            user=request.user, uuid=label_uuid
        )
        label = get_object_or_404(label_qs)
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        label = label_update(
            who=request.user,
            label=label,
            name=data["name"],
            color=data["color"],
        )
        output_serializer = LabelBaseSerializer(instance=label)
        return Response(data=output_serializer.data, status=HTTP_200_OK)
