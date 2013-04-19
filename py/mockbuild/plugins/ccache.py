# vim:expandtab:autoindent:tabstop=4:shiftwidth=4:filetype=python:textwidth=0:
# License: GPL2 or later see COPYING
# Written by Michael Brown
# Copyright (C) 2007 Michael E Brown <mebrown@michaels-house.net>

# python library imports

# our imports
from mockbuild.trace_decorator import decorate, traceLog, getLog
import mockbuild.util

from mockbuild.mounts import BindMountPoint

requires_api_version = "1.0"

# plugin entry point
decorate(traceLog())
def init(rootObj, conf):
    CCache(rootObj, conf)

# classes
class CCache(object):
    """enables ccache in buildroot/rpmbuild"""
    decorate(traceLog())
    def __init__(self, rootObj, conf):
        self.rootObj = rootObj
        self.ccache_opts = conf
        self.ccachePath = self.ccache_opts['dir'] % self.ccache_opts
        rootObj.ccacheObj = self
        rootObj.preExistingDeps.append("ccache")
        rootObj.addHook("prebuild", self._ccacheBuildHook)
        rootObj.addHook("preinit",  self._ccachePreInitHook)
        rootObj.mounts.add(BindMountPoint(srcpath=self.ccachePath, bindpath=rootObj.makeChrootPath("/tmp/ccache")))

    # =============
    # 'Private' API
    # =============
    # set the max size before we actually use it during a build. ccache itself
    # manages size and settings. we also set a few variables used by ccache to
    # find the shared cache.
    decorate(traceLog())
    def _ccacheBuildHook(self):
        self.rootObj.doChroot(["ccache", "-M", str(self.ccache_opts['max_cache_size'])], shell=False)

    # set up the ccache dir.
    # we also set a few variables used by ccache to find the shared cache.
    decorate(traceLog())
    def _ccachePreInitHook(self):
        getLog().info("enabled ccache")
        envupd = {"CCACHE_DIR": "/tmp/ccache", "CCACHE_UMASK": "002" }
        if self.ccache_opts.get('compress') is not None:
            envupd["CCACHE_COMPRESS"] = str(self.ccache_opts['compress'])
        self.rootObj.env.update(envupd)
                
        mockbuild.util.mkdirIfAbsent(self.rootObj.makeChrootPath('/tmp/ccache'))
        mockbuild.util.mkdirIfAbsent(self.ccachePath)
        self.rootObj.uidManager.changeOwner(self.ccachePath)
