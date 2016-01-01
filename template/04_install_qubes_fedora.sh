#!/bin/bash -e
# vim: set ts=4 sw=4 sts=4 et :

source "${SCRIPTSDIR}/distribution.sh"

echo "--> Installing Qubes Canadapop repo."
yumInstall qubes-canadapop-repo-vm
