# -*- coding: utf-8 -*-
# $Id: //gbl/PyCharm/pySimpleVmCtrl/pySimpleVmCtrl/ESXiHost.py#5 $
from pprint import pprint

import inspect

import ssl
default_context = ssl._create_default_https_context


import logging
logger = logging.getLogger()

from pysphere import VIServer, VIProperty
from pysphere.vi_property import getmembers
from pysphere.resources import VimService_services as VI
from pysphere.vi_task import VITask
from pysphere.vi_mor import VIMor, MORTypes

#
# #PYTHON 2.5 inspect.getmembers does not catches AttributeError, this will do
# def getmembers(object, predicate=None):
#     """Return all members of an object as (name, value) pairs sorted by name.
#     Optionally, only return members that satisfy a given predicate."""
#     results = []
#     for key in dir(object):criti
#
#         try:
#             value = getattr(object, key)
#         except AttributeError:
#             continue
#         if not predicate or predicate(value):
#             results.append((key, value))
#     results.sort()
#     return results


class ESXiHostClass:
    def __init__(self, host, user, passwd):
        self._connection = VIServer()
        logger.info("%s:connecting to '%s' as '%s'", __name__, host, user)
        try:
            ssl._create_default_https_context = ssl._create_unverified_context
            self._connection.connect(host, user, passwd)
            logger.debug("%s:host reports '%s V.%s'", __name__,
                         self._connection.get_server_type(), self._connection.get_api_version())
            self.host_config,n,n,n = self._get_host_config()
        except Exception, err:
            logger.critical("%s:%s", __name__, err )
            quit(2)

    def get_connection(self):
        return self._connection

    def get_guests(self):
        ret = []
        for each in self._connection.get_registered_vms():
            entry = self._connection.get_vm_by_path(each)
            ret.append( entry.get_properties()['name'] )
        logger.debug("%s:found %s guests", __name__, len(ret))
        return ret


    def test_property_types(self):
        hosts = self._connection.get_hosts()
        for hmor, hname in hosts.items():
            p = VIProperty(self.server, hmor)
            assert p.name == hname
            #string
            assert isinstance(p.name, basestring)
            #property mor
            assert VIMor.is_mor(p._obj)
            #nested properties
            assert isinstance(p.configManager, VIProperty)
            #bool
            assert isinstance(p.runtime.inMaintenanceMode, bool)
            #list
            assert isinstance(p.vm, list)
            #mor without traversing
            assert VIMor.is_mor(p.vm[0]._obj)
            #traversing
            assert isinstance(p.vm[0].name, basestring)
            #enum
            assert p.runtime.powerState in ['poweredOff', 'poweredOn', 'standBy', 'unknown']
            #int
            assert isinstance(p.summary.config.port, int)
            #long
            assert isinstance(p.hardware.memorySize, long)
            #short as int
            assert isinstance(p.hardware.cpuInfo.numCpuCores, int)
            #date as tuple
            assert isinstance(p.runtime.bootTime, tuple)
            #check property cache
            assert "runtime" in p.__dict__.keys()
            assert "memorySize" in p.hardware.__dict__.keys()
            assert "numCpuCores" in p.hardware.cpuInfo.__dict__.keys()
            assert "name" in p.vm[0].__dict__.keys()
            #check cache flush
            p._flush_cache()
            assert "runtime" not in p.__dict__.keys()
            assert "memorySize" not in p.hardware.__dict__.keys()
            assert "numCpuCores" not in p.hardware.cpuInfo.__dict__.keys()
            assert "name" not in p.vm[0].__dict__.keys()


    def _get_host_config(self):
        # -> get Datacenter and it's properties
        dc_mor=[k for k,v in self._connection.get_datacenters().items()][-1]   # just take the last one .... good?
        dc_props=VIProperty(self._connection, dc_mor)

        # -> get computer resources MORs
        cr_mors=self._connection._retrieve_properties_traversal( property_names=['name','host'],
                                                         from_node=dc_props.hostFolder._obj,   # hostfolder mor
                                                         obj_type='ComputeResource')


        # -> get host MOR
        host_mor=[k for k,v in self._connection.get_hosts().items()][-1]       # just take the last one .... good?

        # -> get computer resource MOR for host
        cr_mor=None
        for cr in cr_mors:
            if cr_mor:
                break
            for p in cr.PropSet:
                if p.Name=="host":
                    for h in p.Val.get_element_ManagedObjectReference():
                        if h==host_mor:
                             cr_mor=cr.Obj
                             break
                    if cr_mor:
                        break

        # -> get Computer Ressources
        cr_props=VIProperty(self._connection,cr_mor)

        # -> create configuration request()
        request=VI.QueryConfigTargetRequestMsg()
        _this=request.new__this(cr_props.environmentBrowser._obj)
        _this.set_attribute_type(cr_props.environmentBrowser._obj.get_attribute_type())
        request.set_element__this(_this)

        # -> get answer back!
        config_target = self._connection._proxy.QueryConfigTarget(request)._returnval
        return config_target, host_mor, dc_props, cr_props


    def get_networks(self):
        ret = []
        for net in self.host_config.Network:
            ret.append (net.Network.Name)
        logger.debug("%s:found %s networks", __name__, len(ret))
        return ret


    def get_datastores(self):
        ret = []
        for d in self.host_config.Datastore:
            if d.Datastore.Accessible:
                ret.append( d.Datastore.Name)
        logger.debug("%s:found %s datastores", __name__, len(ret))
        return ret

