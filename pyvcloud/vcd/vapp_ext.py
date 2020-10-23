
from pyvcloud.vcd.org import Org
from pyvcloud.vcd.vdc import VDC
from pyvcloud.vcd.vapp import VApp
from pyvcloud.vcd.vapp import VM
from pyvcloud.vcd.client import RelationType
from pyvcloud.vcd.client import EntityType
from pyvcloud.vcd.client import find_link
from pyvcloud.vcd.exceptions import EntityNotFoundException

class VAppX(VApp):

    def get_template(self, catalog, template):
        org_resource = self.client.get_org()
        org = Org(self.client, resource=org_resource)
        catalog_item = org.get_catalog_item(catalog, template)
        template_vapp_resource = self.client.get_resource(
            catalog_item.Entity.get('href'))
        return template_vapp_resource

    def create_vm(self, 
                catalog,
                vapp_template,
                vm_template,
                isAdmin=False,
                name=None,
                hostname=None,
                password=None,
                password_auto=None,
                password_reset=None,
                cust_script=None,
                network=None,
                disk_size=None,
                storage_profile=None,
                sizing_policy_href=None,
                placement_policy_href=None,
                ip_allocation_mode='DHCP'):
        """Creates a vm from a template and recompose the vapp to add the new vm.

        :param str catalog: (required) catalog name cointaining vapp template.
        :param str vapp_template: (required) source vApp template name.
        :param str vm_template: (required) source vm template name.
        :param str bame: (optional) new vm name.
        :param str hostname: (optional) new guest hostname.
        :param str password: (optional) the administrator password of the vm.
        :param str password_auto: (bool): (optional) auto generate administrator
                password.
        :param str password_reset: (bool): (optional) True, if the administrator
                password for this vm must be reset after first use.
        :param str cust_script: (optional) script to run on guest
                customization.
        :param str network: (optional) name of the vApp network to connect.
                If omitted, the vm won't be connected to any network.
        :param str storage_profile: (optional) the name of the storage
                profile to be used for this vm.
        :param str sizing_policy_href: (optional) sizing policy used for
                creating the VM.
        :param str placement_policy_href: (optional) placement policy used
                for creating the VM.
        :param str ip_allocation_mode: (optional) the allocation mode for ip.
                Default is for DHCP.

        :return: an object containing EntityType.VAPP XML data representing the
            updated vApp.

        :rtype: lxml.objectify.ObjectifiedElement
        """
        try:
            template_vapp_resource = self.get_template(catalog, vapp_template)
        except EntityNotFoundException:
                print("Template vapp {0} couldn't be instantiated from {1}".format(vapp_template, catalog))
                
        vm_cfg = {
                "vapp": template_vapp_resource,
                "source_vm_name": vm_template,
        }

        if name:
            vm_cfg["target_vm_name"] = name
        if network:
            vm_cfg["network"] = network
            if ip_allocation_mode:
                vm_cfg["ip_allocation_mode"] = ip_allocation_mode
        if disk_size:
            vm_cfg["disk_size"] = disk_size
        if password:
            vm_cfg["password"] = password
        if password_auto:
            vm_cfg["password_auto"] = password_auto
        if password_reset:
            vm_cfg["password_reset"] = password_reset
        if cust_script:
            vm_cfg["cust_script"] = cust_script
        if hostname:
            vm_cfg["hostname"] = hostname

        return self.add_vms([vm_cfg])
