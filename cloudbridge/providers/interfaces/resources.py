"""
Specifications for data objects exposed through a provider or service
"""
from abc import ABCMeta, abstractmethod, abstractproperty


class CloudProviderServiceType(object):

    """
    Defines possible service types that are offered by providers.

    Providers can implement the ``has_service`` method and clients can check
    for the availability of a service with::

        if (provider.has_service(CloudProviderServiceTypes.OBJECTSTORE))
            ...

    """
    COMPUTE = 'compute'
    IMAGE = 'image'
    SECURITY = 'security'
    VOLUME = 'volume'
    BLOCKSTORE = 'block_store'
    OBJECTSTORE = 'object_store'


class WaitStateException(Exception):

    """
    Marker interface for object wait exceptions.
    Thrown when a timeout or errors occurs waiting for an object does not reach
    the expected state within a specified time limit.
    """
    pass


class ObjectLifeCycleMixin(object):

    """
    A mixin for an object with a defined life-cycle, such as an Instance,
    Volume, Image or Snapshot. An object that supports ObjectLifeCycleMixin
    will always have a state, defining which point in its lifecycle it is
    currently at.

    It also defines a wait_till_ready operation, which indicates that the
    object is in a state in its lifecycle where it is ready to be used by an
    end-user.

    A refresh operation allows the object to synchronise its state with the
    service provider.
    """
    __metaclass__ = ABCMeta

    @abstractproperty
    def state(self):
        """
        Get the current state of this object.

        :rtype: ``str``
        :return: The current state as a string
        """
        pass

    @abstractmethod
    def refresh(self):
        """
        Refreshs this object's state and synchronize it with the underlying
        service provider.
        """
        pass

    @abstractmethod
    def wait_till_ready(self, timeout, interval):
        """
        Wait till the current object is in a ready state, which is any
        state where the end-user can successfully interact with the object.
        Will throw a WaitStateException if the object is not ready within
        the specified timeout.

        :type timeout: int
        :param timeout: The maximum length of time (in seconds) to wait for the
        object to become ready.

        :type interval: int
        :param interval: How frequently to poll the object's ready state (in
        seconds)

        :rtype: ``True``
        :return: Returns True if successful. A WaitStateException exception may
        be thrown by the underlying service if the object cannot get into a
        ready state (e.g. If the object is in an error state)
        """
        pass


class InstanceState(object):

    """
    Standard states for a node

    :cvar UNKNOWN: Instance state unknown.
    :cvar PENDING: Instance is pending
    :cvar CONFIGURING: Instance is being reconfigured in some way.
    :cvar RUNNING: Instance is running.
    :cvar REBOOTING: Instance is rebooting.
    :cvar TERMINATED: Instance is terminated. No further operations possible.
    :cvar STOPPED: Instance is stopped. Instance can be resumed.
    :cvar ERROR: Instance is in an error state. No further operations possible.

    """
    UNKNOWN = "unknown"
    PENDING = "pending"
    CONFIGURING = "configuring"
    RUNNING = "running"
    REBOOTING = "rebooting"
    TERMINATED = "terminated"
    STOPPED = "stopped"
    ERROR = "error"


class Instance(ObjectLifeCycleMixin):

    __metaclass__ = ABCMeta

    @abstractproperty
    def instance_id(self):
        """
        Get the instance identifier.

        :rtype: str
        :return: ID for this instance as returned by the cloud middleware.
        """
        pass

    @abstractproperty
    def name(self):
        """
        Get the instance name.

        :rtype: str
        :return: Name for this instance as returned by the cloud middleware.
        """
        pass

    @abstractproperty
    def public_ips(self):
        """
        Get all the public IP addresses for this instance.

        :rtype: list
        :return: A list of public IP addresses associated with this instance.
        """
        pass

    @abstractproperty
    def private_ips(self):
        """
        Get all the private IP addresses for this instance.

        :rtype: list
        :return: A list of private IP addresses associated with this instance.
        """
        pass

    @abstractproperty
    def instance_type(self):
        """
        Get the instance type.

        :rtype: str
        :return: API type of this instance (e.g., ``m1.large``)
        """
        pass

    @abstractmethod
    def reboot(self):
        """
        Reboot this instance (using the cloud middleware API).

        :rtype: bool
        :return: ``True`` if the reboot was succesful; ``False`` otherwise.
        """
        pass

    @abstractmethod
    def terminate(self):
        """
        Permanently terminate this instance.

        :rtype: bool
        :return: ``True`` if the termination of the instance was succesfully
                 initiated; ``False`` otherwise.
        """
        pass

    @abstractproperty
    def image_id(self):
        """
        Get the image ID for this insance.

        :rtype: str
        :return: Image ID (i.e., AMI) this instance is using.
        """
        pass

    @abstractproperty
    def placement_zone(self):
        """
        Get the placement zone where this instance is running.

        :rtype: str
        :return: Region/zone/placement where this instance is running.
        """
        pass

    @abstractproperty
    def mac_address(self):
        """
        Get the MAC address for this instance.

        :rtype: str
        :return: MAC address for ths instance.
        """
        pass

    @abstractproperty
    def security_groups(self):
        """
        Get the security groups associated with this instance.

        :rtype: list or :class:``SecurityGroup`` objects
        :return: A list of SecurityGroup objects associated with this instance.
        """
        pass

    @abstractproperty
    def key_pair_name(self):
        """
        Get the name of the key pair associated with this instance.

        :rtype: str
        :return: Name of the ssh key pair associated with this instance.
        """
        pass

    @abstractmethod
    def create_image(self, name):
        """
        Create a new image based on this instance.
        :return:  an Image object
        :rtype: ``object`` of :class:`.Image`
        """
        pass


class MachineImageState(object):

    """
    Standard states for a machine image

    :cvar UNKNOWN: Image state unknown.
    :cvar PENDING: Image is pending
    :cvar AVAILABLE: Image is available
    :cvar ERROR: Image is in an error state. Not recoverable.

    """
    UNKNOWN = "unknown"
    PENDING = "pending"
    AVAILABLE = "available"
    ERROR = "error"


class MachineImage(ObjectLifeCycleMixin):

    __metaclass__ = ABCMeta

    @abstractproperty
    def image_id(self):
        """
        Get the image identifier.

        :rtype: ``str``
        :return: ID for this instance as returned by the cloud middleware.
        """
        pass

    @abstractproperty
    def name(self):
        """
        Get the image name.

        :rtype: ``str``
        :return: Name for this image as returned by the cloud middleware.
        """
        pass

    @abstractproperty
    def description(self):
        """
        Get the image description.

        :rtype: ``str``
        :return: Description for this image as returned by the cloud middleware
        """
        pass

    @abstractmethod
    def delete(self):
        """
        Delete this image

        :rtype: ``bool``
        :return: True if the operation succeeded
        """
        pass


class VolumeState(object):

    """
    Standard states for a volume

    :cvar UNKNOWN: Volume state unknown.
    :cvar CREATING: Volume is being created.
    :cvar CONFIGURING: Volume is being configured in some way.
    :cvar AVAILABLE: Volume is available and can be attached to an instance.
    :cvar IN_USE: Volume is attached and in-use.
    :cvar DELETED: Volume has been deleted. No further operations possible.
    :cvar ERROR: Volume is in an error state. No further operations possible.

    """
    UNKNOWN = "unknown"
    CREATING = "creating"
    CONFIGURING = "configuring"
    AVAILABLE = "available"
    IN_USE = "in-use"
    DELETED = "deleted"
    ERROR = "error"


class Volume(ObjectLifeCycleMixin):

    __metaclass__ = ABCMeta

    @abstractproperty
    def volume_id(self):
        """
        Get the volume identifier.

        :rtype: ``str``
        :return: ID for this instance as returned by the cloud middleware.
        """
        pass

    @abstractproperty
    def name(self):
        """
        Get the volume name.

        :rtype: ``str``
        :return: Name for this volume as returned by the cloud middleware.
        """
        pass

    @abstractmethod
    def attach(self, instance_id, device):
        """
        Attach this volume to an instance.

        :type instance_id: str
        :param instance_id: The ID of the instance to which it will
                            be attached.

        :type device: str
        :param device: The device on the instance through which the
                       volume will be exposed (e.g. /dev/sdh)

        :rtype: bool
        :return: True if successful
        """
        pass

    @abstractmethod
    def detach(self, force=False):
        """
        Detach this volume from an instance.

        :type force: bool
        :param force: Forces detachment if the previous detachment
            attempt did not occur cleanly. This option is supported on select
            clouds only. This option can lead to data loss or a corrupted file
            system. Use this option only as a last resort to detach a volume
            from a failed instance. The instance will not have an opportunity
            to flush file system caches nor file system meta data. If you
            use this option, you must perform file system check and
            repair procedures.

        :rtype: bool
        :return: True if successful
        """
        pass

    @abstractmethod
    def create_snapshot(self, description=None):
        """
        Create a snapshot of this Volume.

        :type description: str
        :param description: A description of the snapshot.
                            Limited to 256 characters.

        :rtype: :class:`.Snapshot`
        :return: The created Snapshot object
        """
        pass

    @abstractmethod
    def delete(self):
        """
        Delete this volume.

        :rtype: bool
        :return: True if successful
        """
        pass


class SnapshotState(object):

    """
    Standard states for a snapshot

    :cvar UNKNOWN: Snapshot state unknown.
    :cvar PENDING: Snapshot is pending.
    :cvar CONFIGURING: Snapshot is being configured in some way.
    :cvar AVAILABLE: Snapshot has been completed and is ready for use.
    :cvar ERROR: Snapshot is in an error state. No further operations possible.

    """
    UNKNOWN = "unknown"
    PENDING = "pending"
    CONFIGURING = "configuring"
    AVAILABLE = "available"
    ERROR = "error"


class Snapshot(ObjectLifeCycleMixin):

    __metaclass__ = ABCMeta

    @abstractmethod
    def create_volume(self, placement, size=None, volume_type=None, iops=None):
        """
        Create a new Volume from this Snapshot.

        :type zone: str
        :param zone: The availability zone in which the Volume will be created.

        :type size: int
        :param size: The size of the new volume, in GiB (optional). Defaults to
                     the size of the snapshot.

        :type volume_type: str
        :param volume_type: The type of the volume (optional). Availability and
                            valid values depend on the provider.

        :type iops: int
        :param iops: The provisioned IOPs you want to associate with
                     this volume (optional). Availability depends on the
                     provider.

        :rtype: :class:`.Volume`
        :return: An instance of the created Volume
        """
        pass

    @abstractmethod
    def share(self, user_ids=None):
        """
        Share this Snapshot.

        :type user_ids: list of strings
        :param user_ids: A list of cloud provider compatible user IDs. If no
                         IDs are specified, the snapshot is made public.

        :rtype: bool
        :return: True if successful
        """
        pass

    @abstractmethod
    def unshare(self, user_ids=None):
        """
        Unshare this Snapshot.

        :type user_ids: list of strings
        :param user_ids: A list of cloud provider compatible user IDs. If no
                         IDs are specified, the snapshot is made private.

        :rtype: bool
        :return: True if successful
        """
        pass

    @abstractmethod
    def delete(self):
        """
        Delete this snapshot.

        :rtype: bool
        :return: True if successful
        """
        pass


class KeyPair(object):

    __metaclass__ = ABCMeta

    @abstractproperty
    def name(self):
        """
        Return the name of this key pair.

        :rtype: str
        :return: A name of this ssh key pair
        """
        pass

    @abstractproperty
    def material(self):
        """
        Unencrypted private key.

        :rtype: str
        :return: Unencrypted private key or ``None`` if not available.
        """
        pass

    @abstractmethod
    def delete(self):
        """
        Delete this key pair.

        :rtype: bool
        :return: ``True`` is successful.
        """
        pass


class Region(object):

    """
    Represents a cloud region, typically a separate geographic area and will
    contain at least one placement zone.
    """
    __metaclass__ = ABCMeta

    @abstractproperty
    def id(self):
        """
        The id for this region

        :rtype: str
        :return: Id of the region.
        """
        pass

    @abstractproperty
    def name(self):
        """
        Name of the region.

        :rtype: str
        :return: Name of the region.
        """
        pass

    @abstractproperty
    def zones(self):
        """
        Accesss information about placement zones within this region.

        :rtype: iterable
        :return: Iterable of  available placement zones in this region.
        """
        pass


class PlacementZone(object):

    """
    Represents a placement zone. A placement zone is contained within a Region.
    """
    __metaclass__ = ABCMeta

    @abstractproperty
    def name(self):
        """
        Name of the placement zone.

        :rtype: str
        :return: Name of the placement zone.
        """
        pass

    @abstractproperty
    def region(self):
        """
        A region this placement zone is associated with.

        :rtype: str
        :return: The name of the region the zone is associated with.
        """
        pass


class InstanceType(object):

    """
    An instance type object.
    """
    __metaclass__ = ABCMeta

    @abstractproperty
    def id(self):
        pass

    @abstractproperty
    def name(self):
        pass

    @abstractproperty
    def family(self):
        """
        The family/group that this instance type belongs to. For example,
        General Purpose Instances or High-Memory Instances. If the provider
        does not support such a grouping, it may return None.

        :rtype: str
        :return: Name of the instance family.
        """
        pass

    @abstractproperty
    def vcpus(self):
        """
        The number of VCPUs supported by this instance type.

        :rtype: int
        :return: Number of VCPUs
        """
        pass

    @abstractproperty
    def ram(self):
        """
        The amount of RAM (in mb) supported by this instance type.

        :rtype: int
        :return: Total RAM (in MB).
        """
        pass

    @abstractproperty
    def size_root_disk(self):
        """
        The size of this instance types's root disk (in GB).

        :rtype: int
        :return: Size of root disk (in GB).
        """
        pass

    @abstractproperty
    def size_ephemeral_disks(self):
        """
        The size of this instance types's total ephemeral storage (in GB).

        :rtype: int
        :return: Size of ephemeral disks (in GB).
        """
        pass

    @abstractproperty
    def num_ephemeral_disks(self):
        """
        The total number of ephemeral disks on this instance type.

        :rtype: int
        :return: Number of ephemeral disks available.
        """
        pass

    @abstractproperty
    def size_total_disk(self):
        """
        The total disk space available on this instance type.
        (root_disk + ephemeral)

        :rtype: int
        :return: Size of total disk space (in GB).
        """
        pass

    @abstractproperty
    def extra_data(self):
        """
        A dictionary of extra data about this instance. May contain
        nested dictionaries, but all key value pairs are strings or integers.

        :rtype: dict
        :return: Extra attributes for this instance type
        """
        pass


class SecurityGroup(object):

    __metaclass__ = ABCMeta

    @abstractproperty
    def id(self):
        """
        Get the ID of this security group.

        :rtype: str
        :return: Security group ID
        """
        pass

    @abstractproperty
    def name(self):
        """
        Return the name of this security group.

        :rtype: str
        :return: A name of this security group.
        """
        pass

    @abstractproperty
    def description(self):
        """
        Return the description of this security group.

        :rtype: str
        :return: A description of this security group.
        """
        pass

    @abstractproperty
    def rules(self):
        """
        Get the list of rules for this security group.

        :rtype: list of :class:``.SecurityGroupRule``
        :return: A list of security group rule objects
        """
        pass

    @abstractmethod
    def delete(self):
        """
        Delete this security group.

        :rtype: bool
        :return: ``True`` is successful.
        """
        pass

    @abstractmethod
    def add_rule(self, ip_protocol=None, from_port=None, to_port=None,
                 cidr_ip=None, src_group=None):
        """
        Create a security group rule.

        You need to pass in either ``src_group`` OR ``ip_protocol``,
        ``from_port``, ``to_port``, and ``cidr_ip``.  In other words, either
        you are authorizing another group or you are authorizing some
        ip-based rule.

        :type ip_protocol: str
        :param ip_protocol: Either ``tcp`` | ``udp`` | ``icmp``.

        :type from_port: int
        :param from_port: The beginning port number you are enabling.

        :type to_port: int
        :param to_port: The ending port number you are enabling.

        :type cidr_ip: str or list of strings
        :param cidr_ip: The CIDR block you are providing access to.

        :type src_group: ``object`` of :class:`.SecurityGroup`
        :param src_group: The Security Group you are granting access to.

        :rtype: bool
        :return: True if successful.
        """
        pass

    @abstractmethod
    def rule_exists(self, rules, from_port, to_port, ip_protocol, cidr_ip):
        """
        Check if an authorization rule with supplied parameters exists.

        :type rules: list of :class:``.SecurityGroupRule`` SecurityGroupRule
        :param rules: A list of rules to check against

        :type ip_protocol: str
        :param ip_protocol: Either ``tcp`` | ``udp`` | ``icmp``

        :type from_port: int
        :param from_port: The beginning port number

        :type to_port: int
        :param to_port: The ending port number

        :type cidr_ip: str or list of strings
        :param cidr_ip: The CIDR block

        :rtype: bool
        :return: ``True`` if an existing rule matches supplied parameters;
                 ``False`` otherwise.
        """
        pass


class SecurityGroupRule(object):

    """
    Represents a security group rule.
    """
    __metaclass__ = ABCMeta

    @abstractproperty
    def ip_protocol(self):
        """
        IP protocol used. Either ``tcp`` | ``udp`` | ``icmp``.
        """
        pass

    @abstractproperty
    def from_port(self):
        """
        Lowest port number opened as part of this rule.
        """
        pass

    @abstractproperty
    def to_port(self):
        """
        Highest port number opened as part of this rule.
        """
        pass

    @abstractproperty
    def cidr_ip(self):
        """
        CIDR block this security group is providing access to.
        """
        pass

    @abstractproperty
    def group(self):
        """
        Security group given access permissions by this rule.

        :rtype: ``object`` of :class:`.SecurityGroup`
        :return: The Security Group with granting access.
        """
        pass


class ContainerObject(object):

    """
    Represents an object stored within a container.
    """
    __metaclass__ = ABCMeta

    @abstractproperty
    def name(self):
        """
        Get this object's name.

        :rtype: ``str``
        :return: Name of this object as returned by the cloud middleware.
        """
        pass

    @abstractmethod
    def download(self, target_stream):
        """
        Download this object and write its
        contents to the target_stream.

        :rtype: bool
        :return: True if successful
        """
        pass

    @abstractmethod
    def upload(self, source_stream):
        """
        Set the contents of this object to the data read from the source
        stream.

        :rtype: bool
        :return: True if successful
        """
        pass

    @abstractmethod
    def delete(self):
        """
        Delete this object.

        :rtype: bool
        :return: True if successful
        """
        pass


class Container(object):

    __metaclass__ = ABCMeta

    @abstractproperty
    def name(self):
        """
        Get this container's name.

        :rtype: ``str``
        :return: Name of this container as returned by the cloud middleware.
        """
        pass

    @abstractmethod
    def get(self, key):
        """
        Retrieve a given object from this container.

        :type key: ``str``
        :param key: the identifier of the object to retrieve

        :rtype: ContainerObject
        :return: The ContainerObject or None if it cannot be found.
        """
        pass

    @abstractmethod
    def list(self):
        """
        List all objects within this container.

        :rtype: ContainerObject
        :return: List of all available ContainerObjects within this container
        """
        pass

    @abstractmethod
    def delete(self, delete_contents=False):
        """
        Delete this container.

        :type delete_contents: ``bool``
        :param delete_contents: If True, all objects within the container will
        be deleted.

        :rtype: bool
        :return: True if successful
        """
        pass
