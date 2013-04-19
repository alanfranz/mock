#!/usr/bin/python -tt

import os
import os.path
import grp

import mockbuild.util
import mockbuild.exception
from mockbuild.trace_decorator import traceLog, decorate

class MountPoint(object):
    '''base class for mounts'''
    decorate(traceLog())
    def __init__(self, mountsource, mountpath):
        self.mountpath = mountpath
        self.mountsource = mountsource

    decorate(traceLog())
    def ismounted(self):
        if self.mountpath in [ x.split()[1] for x in open('/proc/mounts') ]:
            return True
        return False

class FileSystemMountPoint(MountPoint):
    '''class for managing filesystem mounts in the chroot'''
    decorate(traceLog())
    def __init__(self, path, filetype=None, device=None, options=None):
        if not path:
            raise RuntimeError, "no path specified for mountpoint"
        if not filetype:
            raise RuntimeError, "no filetype specified for mountpoint"
        if filetype == 'pts' or filetype == 'proc' or filetype == 'sys':
            device = filetype
        if not device:
            raise RuntimeError, "no device file specified for mountpoint"

        MountPoint.__init__(self, mountsource=device, mountpath=path)
        self.device = device
        self.path = path
        self.filetype = filetype
        self.options = options
        self.mounted = self.ismounted()

    decorate(traceLog())
    def mount(self):
        if self.mounted:
            return

        cmd = ['/bin/mount', '-n', '-t', self.filetype ]
        if self.options:
            cmd += ['-o', self.options ]
        cmd += [self.device, self.path]
        try:
            mockbuild.util.do(cmd)
        except mockbuild.exception.Error, e:
            return False
        self.mounted = True
        return True

    decorate(traceLog())
    def umount(self, force=False, nowarn=False):
        if not self.mounted:
            return
        cmd = ['/bin/umount', '-n', '-l', self.path]
        try:
            mockbuild.util.do(cmd)
        except mockbuild.exception.Error, e:
            return False
        self.mounted = False
        return True

class BindMountPoint(MountPoint):
    '''class for managing bind-mounts in the chroot'''
    decorate(traceLog())
    def __init__(self, srcpath, bindpath):
        MountPoint.__init__(self, mountsource=srcpath, mountpath=bindpath)
        self.srcpath = srcpath
        self.bindpath = bindpath
        self.mounted = self.ismounted()

    decorate(traceLog())
    def mount(self):
        if not self.mounted:
            cmd = ['/bin/mount', '-n',
                   '--bind', self.srcpath, self.bindpath ]
            try:
                mockbuild.util.do(cmd)
            except mockbuild.exception.Error, e:
                return False
        self.mounted = True
        return True

    decorate(traceLog())
    def umount(self):
        if self.mounted:
            cmd = ['/bin/umount', '-n', self.bindpath ]
            try:
                mockbuild.util.do(cmd)
            except mockbuild.exception.Error, e:
                return False
        self.mounted = False
        return True

class Mounts(object):
    '''class to manage all mountpoints'''
    decorate(traceLog())
    def __init__(self, rootObj):
        self.rootObj = rootObj
        self.mounts = [ FileSystemMountPoint(filetype='proc', device='mock_chroot_proc', path=rootObj.makeChrootPath('/proc')),
                        FileSystemMountPoint(filetype='sysfs', device='mock_chroot_sys', path=rootObj.makeChrootPath('/sys')),
                        FileSystemMountPoint(filetype='tmpfs', device='mock_chroot_shmfs', path=rootObj.makeChrootPath('/dev/shm')),
                      ]
        opts = 'gid=%d,mode=0620,ptmxmode=0666' % grp.getgrnam('tty').gr_gid
        if mockbuild.util.cmpKernelVer(os.uname()[2], '2.6.29') >= 0:
            opts += ',newinstance'
        self.mounts.append(FileSystemMountPoint(filetype='devpts', device='mock_chroot_devpts', path=rootObj.makeChrootPath('/dev/pts'), options=opts))

    decorate(traceLog())
    def add(self, mount):
        self.mounts.append(mount)

    decorate(traceLog())
    def mountall(self):
        for m  in self.mounts:
            m.mount()

    decorate(traceLog())
    def umountall(self, force=False, nowarn=False):
        for m in reversed(self.mounts):
            m.umount()

    decorate(traceLog())
    def get_mounted(self):
        return [ m.mountpath for m in self.mounts if m.ismounted() ]

    decorate(traceLog())
    def get_mountpoints(self):
        return [ m.mountpath for m in self.mounts ]
