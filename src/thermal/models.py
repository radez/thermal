import gettext
from django.db import models
from thermal.db import xml_models
gettext.install('heat', unicode=1)
from thermal.helpers import get_heat_client
from thermal.helpers import get_members
HEAT_CLIENT = get_heat_client()

class Stack(xml_models.Model):
    object_xpath = './/member'
    rest_call = HEAT_CLIENT.list_stacks
    StackId = xml_models.CharField(xpath='/member/StackId')
    StackName = xml_models.CharField(xpath='/member/StackName')
    StackStatus = xml_models.CharField(xpath='/member/StackStatus')
    TemplateDescription = xml_models.CharField(xpath='/member/TemplateDescription')
    StackStatusReason = xml_models.CharField(xpath='/member/StackStatusReason')
    CreationTime = xml_models.DateField(xpath='/member/CreationTime', date_format='%Y-%m-%dT%H:%M:%SZ')
    LastUpdatedTime = xml_models.DateField(xpath='/member/LastUpdatedTime', date_format='%Y-%m-%dT%H:%M:%SZ')

    def __unicode__(self):
        return self.StackID


class EventResourceProperties(xml_models.Model):
    NovaSchedulerHints = xml_models.CharField(xpath='/member/ResourceProperties/NovaSchedulerHints')
    UserData = xml_models.CharField(xpath='/member/ResourceProperties/UserData')
    SourceDestCheck = xml_models.CharField(xpath='/member/ResourceProperties/SourceDestCheck')
    AvailabilityZone = xml_models.CharField(xpath='/member/ResourceProperties/AvailabilityZone')
    Monitoring = xml_models.CharField(xpath='/member/ResourceProperties/Monitoring')
    Volumes = xml_models.CharField(xpath='/member/ResourceProperties/Volumes')
    Tags = xml_models.CharField(xpath='/member/ResourceProperties/Tags')
    Tenancy = xml_models.CharField(xpath='/member/ResourceProperties/Tenancy')
    PlacementGroupName = xml_models.CharField(xpath='/member/ResourceProperties/PlacementGroupName')
    ImageId = xml_models.CharField(xpath='/member/ResourceProperties/ImageId')
    SubnetId = xml_models.CharField(xpath='/member/ResourceProperties/SubnetId')
    KeyName = xml_models.CharField(xpath='/member/ResourceProperties/KeyName')
    SecurityGroups = xml_models.CharField(xpath='/member/ResourceProperties/SecurityGroups')
    SecurityGroupIds = xml_models.CharField(xpath='/member/ResourceProperties/SecurityGroupIds')
    KernelId = xml_models.CharField(xpath='/member/ResourceProperties/KernelId')
    RamDiskId = xml_models.CharField(xpath='/member/ResourceProperties/RamDiskId')
    DisableApiTermination = xml_models.CharField(xpath='/member/ResourceProperties/DisableApiTermination')
    InstanceType = xml_models.CharField(xpath='/member/ResourceProperties/InstanceType')
    PrivateIpAddress = xml_models.CharField(xpath='/member/ResourceProperties/PrivateIpAddress')


class Event(xml_models.Model):
    object_xpath = './/member'
    rest_call = HEAT_CLIENT.list_stack_events
    EventId = xml_models.IntField(xpath='/member/EventId')
    StackId = xml_models.CharField(xpath='/member/StackId')
    ResourceStatus = xml_models.CharField(xpath='/member/ResourceStatus')
    ResourceType = xml_models.CharField(xpath='/member/ResourceType')
    Timestamp = xml_models.DateField(xpath='/member/Timestamp', date_format='%Y-%m-%dT%H:%M:%SZ')
    StackName = xml_models.CharField(xpath='/member/StackName')
    ResourceProperties = xml_models.CollectionField(EventResourceProperties, xpath='/member/ResourceProperties')
    PhysicalResourceId = xml_models.CharField(xpath='/member/PhysicalResourceId')
    ResourceStatusData = xml_models.CharField(xpath='/member/ResourceStatusData')
    LogicalResourceId = xml_models.CharField(xpath='/member/LogicalResourceId')
