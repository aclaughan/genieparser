import re

from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Any, Optional


# =================================
# Schema for:
#  * 'show wireless fabric summary'
# =================================
class ShowWirelessFabricSummarySchema(MetaParser):
    """Schema for show wireless fabric summary."""

    schema = {
        "fabric_status": str,
        Optional("control_plane"): {
            Optional("ip_address"): {
                Optional(str): {
                    Optional("name"): str,
                    Optional("key"): str,
                    Optional("status"): str
                }
            }
        },
        Optional("fabric_vnid_mapping"): {
            Optional("l2_vnid"): {
                Optional(int): {
                    Optional("name"): str,
                    Optional("l3_vnid"): int,
                    Optional("control_plane_name"): str,
                    Optional("ip_address"): str,
                    Optional("subnet"): str
                }
            }
        }
    }


# =================================
# Parser for:
#  * 'show wireless fabric summary'
# =================================
class ShowWirelessFabricSummary(ShowWirelessFabricSummarySchema):
    """Parser for show wireless fabric summary"""

    cli_command = 'show wireless fabric summary'

    def cli(self, output=None):
        if output is None:
            output = self.device.execute(self.cli_command)
        else:
            output=output

        # Fabric Status      : Enabled
        #
        #
        # Control-plane:
        # Name                             IP-address        Key                              Status
        # --------------------------------------------------------------------------------------------
        # default-control-plane            10.10.90.16       099fff                           Up
        # default-control-plane            10.10.90.22       099fff                           Up
        #
        #
        # Fabric VNID Mapping:
        # Name               L2-VNID        L3-VNID        IP Address             Subnet        Control plane name
        # ----------------------------------------------------------------------------------------------------------------------
        # Data                8192           0                                  0.0.0.0            default-control-plane 
        # Guest               8189           0                                  0.0.0.0            default-control-plane 
        # Voice               8191           0                                  0.0.0.0            default-control-plane
        # Fabric_B_INFRA_VN     8188           4097           10.10.40.0          255.255.254.0      default-control-plane
        # Physical_Security     8190           0                                  0.0.0.0            default-control-plane



        # Fabric Status      : Enabled
        p_status = re.compile(r"^Fabric\s+Status\s+:\s+(?P<status>(Enabled|Disabled))$")

        # Control-plane:
        p_control = re.compile(r"^Control-plane:$")

        # Name                             IP-address        Key                              Status
        p_header_1 = re.compile(r"^Name\s+IP-address\s+Key\s+Status$")

        # --------------------------------------------------------------------------------------------
        p_delimiter_1 = re.compile(r"^--------------------------------------------------------------------------------------------$")

        # default-control-plane            10.10.90.11       fa85ff                           Up
        p_cp_client = re.compile(r"^(?P<cp_name>\S+)\s+(?P<cp_ip_address>\S+)\s+(?P<cp_key>\S+)\s+(?P<cp_status>\S+)$")

        # Fabric VNID Mapping:
        p_vnid = re.compile(r"^Fabric\s+VNID\s+Mapping:$")

        # Name               L2-VNID        L3-VNID        IP Address             Subnet        Control plane name
        p_header_2 = re.compile(r"^Name\s+L2-VNID\s+L3-VNID\s+IP\s+Address\s+Subnet\s+Control\s+plane\s+name$")

        # ----------------------------------------------------------------------------------------------------------------------
        p_delimiter_2 = re.compile(r"^----------------------------------------------------------------------------------------------------------------------$")

        # Data                8192           0                                  0.0.0.0            default-control-plane
        p_vnid_mappings = re.compile(r"^(?P<vnid_name>\S+)\s+(?P<vnid_l2>\d+)\s+(?P<vnid_l3>\d+)\s+(?P<vnid_ip_address>\S+)\s+(?P<vnid_subnet>\S+)\s+(?P<vnid_cp_name>\S+)$")

        # Voice               8191           0                                  0.0.0.0            default-control-plane
        p_vnid_mappings_no_ip = re.compile(r"^(?P<vnid_name>\S+)\s+(?P<vnid_l2>\d+)\s+(?P<vnid_l3>\d+)\s+(?P<vnid_subnet>\S+)\s+(?P<vnid_cp_name>\S+)$")


        show_wireless_fabric_summary_dict = {}

        for line in output.splitlines():
            line = line.strip()
            # Fabric Status      : Enabled
            if p_status.match(line):
                match = p_status.match(line)
                status = match.group("status")
                if status == "Enabled":
                    if not show_wireless_fabric_summary_dict.get("fabric_status"):
                        show_wireless_fabric_summary_dict.update({ "fabric_status" : status })
                else:
                    if not show_wireless_fabric_summary_dict.get("fabric_status"):
                        show_wireless_fabric_summary_dict.update({ "fabric_status" : status })
                continue
            # Control-plane:
            elif p_control.match(line):
                continue
            # Name                             IP-address        Key                              Status
            elif p_header_1.match(line):
                continue
            # --------------------------------------------------------------------------------------------
            elif p_delimiter_1.match(line):
                continue
            # default-control-plane            10.10.90.11       fa85ff                           Up
            elif p_cp_client.match(line):
                if not show_wireless_fabric_summary_dict.get("control_plane"):
                    show_wireless_fabric_summary_dict.update({ "control_plane" : { "ip_address" : {} }})
                match = p_cp_client.match(line)
                groups = match.groupdict()
                show_wireless_fabric_summary_dict["control_plane"]["ip_address"].update({ groups["cp_ip_address"] : { "name" : groups["cp_name"], "key": groups["cp_key"], "status" : groups["cp_status"]} })
                continue
            # Fabric VNID Mapping:
            elif p_vnid.match(line):
                if not show_wireless_fabric_summary_dict.get("fabric_vnid_mapping"):
                    show_wireless_fabric_summary_dict.update({ "fabric_vnid_mapping": { "l2_vnid" : {} }})
                continue
            # Name               L2-VNID        L3-VNID        IP Address             Subnet        Control plane name
            elif p_header_2.match(line):
                continue
            # ----------------------------------------------------------------------------------------------------------------------
            elif p_delimiter_2.match(line):
                continue
            # Fabric_B_INFRA_VN     8188           4097           10.10.40.0          255.255.254.0      default-control-plane
            elif p_vnid_mappings.match(line):
                match = p_vnid_mappings.match(line)
                groups = match.groupdict()
                show_wireless_fabric_summary_dict["fabric_vnid_mapping"]["l2_vnid"].update({ int(groups["vnid_l2"]) : { "name": groups["vnid_name"], "l3_vnid": int(groups["vnid_l3"]), "ip_address": groups["vnid_ip_address"], 
                                                                                "subnet": groups["vnid_subnet"], "control_plane_name": groups["vnid_cp_name"]}})
                continue
            # Voice               8191           0                                  0.0.0.0            default-control-plane
            elif p_vnid_mappings_no_ip.match(line):
                match = p_vnid_mappings_no_ip.match(line)
                groups = match.groupdict()
                show_wireless_fabric_summary_dict["fabric_vnid_mapping"]["l2_vnid"].update({ int(groups["vnid_l2"]) : { "name": groups["vnid_name"], "l3_vnid": int(groups["vnid_l3"]), "control_plane_name": groups["vnid_name"] }})
                continue
        print(show_wireless_fabric_summary_dict)
        return show_wireless_fabric_summary_dict