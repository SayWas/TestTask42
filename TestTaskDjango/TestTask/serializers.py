from rest_framework import serializers
from .models import Contract, Subsidiary, Contractor, ContractRole, User


class OrganizationSerializer(serializers.ModelSerializer):
    """
    Base serializer for organization models like Subsidiary and Contractor.
    """
    class Meta:
        model = None
        fields = ['id', 'name']


class SubsidiarySerializer(OrganizationSerializer):
    """
    Serializer for Subsidiary model, extending OrganizationSerializer.
    """
    class Meta(OrganizationSerializer.Meta):
        model = Subsidiary
        fields = OrganizationSerializer.Meta.fields + ['is_system_owner']


class ContractorSerializer(OrganizationSerializer):
    """
    Serializer for Contractor model, extending OrganizationSerializer.
    """
    class Meta(OrganizationSerializer.Meta):
        model = Contractor
        fields = OrganizationSerializer.Meta.fields + ['licensed']


class ContractRoleSerializer(serializers.ModelSerializer):
    """
    Serializer for ContractRole model, includes user
    full name and role display.
    """
    full_name = serializers.CharField(source='user.get_full_name')
    role_display = serializers.CharField(source='get_role_display')

    class Meta:
        model = ContractRole
        fields = ['full_name', 'role_display', 'user']


class ContractSerializer(serializers.ModelSerializer):
    """
    Serializer for Contract model, includes detailed organization and
    participant information.
    """
    organization_do = SubsidiarySerializer(read_only=True)
    organization_po = ContractorSerializer(read_only=True)
    participants = serializers.SerializerMethodField()

    class Meta:
        model = Contract
        fields = ['id', 'title', 'start_date', 'end_date', 'status',
                  'organization_do', 'organization_po', 'participants']

    def get_participants(self, obj):
        """
        Retrieves a list of participants with their roles in the contract.
        """
        participants_data = []
        roles = ContractRole.objects.filter(
            contract=obj).select_related('user')
        for role in roles:
            serializer = UserContractRoleSerializer(role)
            participants_data.append(serializer.data)
        return participants_data


class UserContractRoleSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for users in the context of their role within
    a contract.
    """
    username = serializers.CharField(source='user.get_username')
    full_name = serializers.CharField(source='user.get_full_name')
    contract_role = serializers.CharField(source='get_role_display')
    organization = serializers.SerializerMethodField()

    class Meta:
        model = ContractRole
        fields = ['username', 'full_name', 'contract_role', 'organization']

    def get_organization(self, obj):
        """
        Retrieves the organization associated with the user,
        serialized based on the specific type of organization.
        """
        user = obj.user
        if user.content_type and user.object_id:
            OrganizationModel = user.content_type.model_class()
            organization = OrganizationModel.objects.filter(
                id=user.object_id).first()
            if organization:
                if isinstance(organization, Subsidiary):
                    return SubsidiarySerializer(organization).data
                elif isinstance(organization, Contractor):
                    return ContractorSerializer(organization).data
        return None


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name']
