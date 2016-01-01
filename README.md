
====
TODO
====
1.  Create separate keys for Fedora and Debian

2.  How to install from my repo:
       
        Enabling testing, since nothing in current yet 
    
        Add 'cost=10' into repo; will take from mine (unless qubes version is
        greater?)
    
        Maybe compiling with debug or test incrementing versons would work?  If
        dev versions install over release version with same version number;
        that is ideal

        *** So test this theory against a qubes version ***

3.  Implement split-gpg
4.  Implement DisposibleVM building -- Maybe create dom0 salt formula
5.  Implement proxy to speed up build times
6.  Consider using a shared 'src' directory
  
7.  How to use repo-latest-snapshot

8.  ADD hook in DOM installation to install repo, or install via a salt-formula
9.  ADD dom0 build + template repos for dom0

10. Move these notes into a README for both linux-yum and linux-deb
11. Move non specific stuff into own repo; maybe a config repo; instead
    of qubes-tools otherwise items like check, and KEYS are displaced
    among packages -- qubes-builder-release or qubes-linux-release

12. Figure out that GUI gpg password asked, since it seems to cache password
    and would be useful to use when signing stags as well as signing each commit
    - Also need for Debian Release signing to prevent entering password twice

XXX: Important Details
----------------------
    - NEED to update Makefile.debian to have a sign target, even if we do not
      needd to sign, then just return True

    - Include nginix setup within this repo to be able to easily reproduce it

    - Maybe COMBINE these scripts into *-release as submodules...
    - Modify Makefile to allow var paths to linux-yum
    - Modify linux-yum and linux-deb to allow vars so they need not be
      over-written


=======================
SIGNING DEBIAN PACKAGES
=======================
- Debian packages are currently not being signed
- Would need to change Debian configuration to verify signed packages since
  that feature is disabled by default (/etc/dpkg/dpkg)
- Either install devscripts in Fedora build ENV or use the chroot environment
  to sign

Dependencies
------------
devscripts -- For debsign
debsigs -- Not available for Fedora?

Sign packages source file
-------------------------
debsign -k 5A4C6DAD package.dsc
gpg --verify package.dsc

Sign a deb package
------------------
debsigs --sign=[origin|maint|archive] -k 5A4C6DAD package.deb


COMPLETED TASKS
===============
- Create a BUILDER_PLUGIN to install nrgaway repo when building templates
- Create a nrgaway branch of 'linux-yum' and 'linux-deb'
- Work on better web permissions, ssh certificate to update haswell
- Create better web url for canadapop.com ... translate qubes-yum to path


=============================================
Initial Development and Server Configurations
=============================================
-   XXX: Need  to update keys.conf to import separate keys for Fedora and
Debian.
    Should there are be separate keys for each version as well?

-   First need to import key into rpm so rpm's can be verified.  keys.conf
should take care of this step:
    sudo rpm --import nrgaway-qubes-signing-key.asc

-   Make sure release.conf is included in builder.conf and configured to liking.

-   Copy ssh public key to remote-host using ssh-copy-id
    ssh-copy-id -i ~/.ssh/id_rsa.pub remote-host

- On web server, install createrepo
    apt-get install createrepo

Create keys
-----------
Make sure they created using proper security settings and expire dates

Export keys
-----------
        gpg --list-keys
        gpg --output release_key_debian.asc --armor --export 5A4C6DAD

Create Debian keyring
---------------------
http://blog.jonliv.es/blog/2011/04/26/creating-your-own-signed-apt-repository-and-debian-packages/

1.  Export an existing release  key
        gpg --list-keys
        gpg --output release-key-debian.asc --armor --export 5A4C6DAD

2.  Copy `release-key-debian.asc` to `chroot_debian`
        sudo cp release-key-debian.asc ~/qubes/chroot_debian

3.  Use `apt-key` to create a Debian keyring
        cd ~/qubes
        sudo chroot chroot_jessie
        rm /etc/apt/trusted*
        apt-key add release-key-debian.asc
        cp /etc/apt/trusted.gpg release-archive-keyring.gpg
        exit

4.  Copy the generated keyring for use

--------------
Build Packages
--------------
Increment version number, if needed
    See doc/ReleaseManagerWorkflow.md

Build all packages as normal
    make qubes-vm

---------------------------------
Signing and Updating Fedora Repos
---------------------------------

Check release status
    make check-release-status

Uploading Fedora packages to current-testing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    make sign-vm update-repo-current-testing

Uploading Fedora packages to current
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    make sign-vm update-repo-current

-----------------------------
Syncing to Active Remote Repo
-----------------------------
To test, run in 'dry' mode
    cd qubes-src/linux-yum
    DRY=-n ./sync_qubes-os.org_repo.sh r3.1

To proceed with actual update to remote repo
    cd qubes-src/linux-yum
    ./sync_qubes-os.org_repo.sh r3.1


Release Manager Workflow
========================

Release Manager is person responsible for deciding when the packages should be
released, which changes should be included in each package release, and finally
managing packages repository - including building the packages.

When the package is ready to be released, Release Manager does the following things:
1. Increment version number, commit that **as a separate commit** and add a
   signed version tag.
2. Transfer that commits to release build VM (used only for building packages
   to be released, no code modifications, no test builds).
3. Build the package(s).
4. Sign the package(s).
5. Upload the packages to the 'current-testing' repository.
6. Upload code used to build the packages to official repository.
7. Wait some time for a feedback from testers.
8. Commit package(s) to the 'current' repository.


Build environment
-----------------
To build packages for multiple Qubes releases (like R2 and R3.0), **separate**
build clones **must** be used. Otherwise packages will be linked with wrong
versions of each other.  It is a good idea to use totally separated
directories, but theoretically you can use just separate builder and common
source directories. To achieve that you can either set `SRC_DIR` variable in
`builder.conf`, or replace `qubes-src` directory with a symlink.

Additionally some `builder.conf` settings are especially useful in release
build environment:

    # Ensure the value is empty - packages will be signed
    NO_SIGN = 

    # Set proper signing key, choose the right ID depending on Qubes release
    # for which you build packages here
    SIGN_KEY = 0A40E458
    DEBIAN_SIGN_KEY = 47FD92FA

    # Sanity check - verify if you are on the right branch before building the
    # component. Note that this does not fully work for vmm-xen, because of
    # additional components used during the build.
    CHECK_BRANCH = 1

    # Target repositories (depending on target release)
    LINUX_REPO_fc20_BASEDIR = $(SRC_DIR)/linux-yum/r3.0
    LINUX_REPO_fc21_BASEDIR = $(SRC_DIR)/linux-yum/r3.0
    LINUX_REPO_fc22_BASEDIR = $(SRC_DIR)/linux-yum/r3.0
    LINUX_REPO_wheezy_BASEDIR = $(SRC_DIR)/linux-deb/r3.0
    LINUX_REPO_jessie_BASEDIR = $(SRC_DIR)/linux-deb/r3.0

    # Automatically upload the packages when update-repo-* targets are called
    AUTOMATIC_UPLOAD = 1

    # Template labels
    TEMPLATE_LABEL += fc20:fedora-20
    TEMPLATE_LABEL += fc21:fedora-21
    TEMPLATE_LABEL += wheezy:debian-7
    TEMPLATE_LABEL += jessie:debian-8

    # Handy shortcuts
    ifdef C
    COMPONENTS := $(C)
    endif

    ifdef V
    VERBOSE := $(V)
    endif


Incrementing version
--------------------

(Almost) each component have `version` file in its root directory, which
contains current package version.  Some of them additionally contains `rel`
file, which contains package release revision - mostly because package version
is directly based on upstream version.  Those files should be changed in
separate 'version commit'.

To streamline the task, this script can be used:

    #!/bin/sh
    set -e
    set -x
    export DIST=wheezy
    if [ -f debian/changelog ]; then
        rm -f debian/changelog.*
        ../builder-debian/scripts/debian-changelog.sh
        add=`readlink -f debian/changelog`
    fi
    V=`cat version`
    R=`cat rel 2>/dev/null || :`
    if [ -n "$R" ]; then
        V="$V-$R"
        add="$add `readlink -f rel`"
    fi
    git commit -m "version $V" version $add
    git tag -s -m "version $V" v$V

Example usage:

    [user@devel ~/src/core-agent-linux]$ vim version # increment version number
    [user@devel ~/src/core-agent-linux]$ ../commit-v.sh
    + export DIST=wheezy
    + DIST=wheezy
    + '[' -f debian/changelog ']'
    + ../builder-debian/scripts/debian-changelog.sh
    libdistro-info-perl is not installed, Debian release names are not known.
    libdistro-info-perl is not installed, Ubuntu release names are not known.
    ++ readlink -f debian/changelog
    + add=/home/user/src/core-agent-linux/debian/changelog
    ++ cat version
    + V=3.0.9
    ++ cat rel
    ++ :
    + R=
    + '[' -n '' ']'
    + git commit -m 'version 3.0.9' version /home/user/src/core-agent-linux/debian/changelog
    [master 60f519c] version 3.0.9
     2 files changed, 7 insertions(+), 1 deletion(-)
    + git tag -s -m 'version 3.0.9' v3.0.9


Transferring the commits
------------------------

The most straightforward way is just to use git for that. Qubes builder provides
convenient scripts for that.

### make prepare-merge

This target allows to fetch the commits from some repository, verify signed
tags and show you a shortlog of the changes. Then you can decide whether you
want to merge them or not. This target can be useful together with overriding
some builder.conf parameters, especially `COMPONENTS` and `GIT_PREFIX` (or
`GIT_REMOTE` if you've set git remotes in the components):

    [user@build ~/qubes-R3]$ make prepare-merge COMPONENTS="vmm-xen core-vchan-xen" GIT_PREFIX=marmarek/qubes-
    -> Updating sources for vmm-xen...   
    --> Fetching from git://github.com/marmarek/qubes-vmm-xen.git xen-4.4...
    --> Verifying tags...

    -> Updating sources for core-vchan-xen...
    --> Fetching from git://github.com/marmarek/qubes-core-vchan-xen.git master...
    --> Verifying tags...

    -> Updating sources for builder-fedora...
    --> Fetching from git://github.com/marmarek/qubes-builder-fedora.git master...
    --> Verifying tags...

    -> Updating sources for builder...
    --> Fetching from git://github.com/marmarek/qubes-builder.git master...
    --> Verifying tags...

    Changes to be merged:
    > qubes-src/core-vchan-xen merge: git merge FETCH_HEAD
    edc7c4f version 3.0.4
    62c822b Check if remote domain is still alive
    > . fast-forward: git merge FETCH_HEAD
    6b11d03 Fix sign-all target, introduce sign-vm and sign-dom0
    9921503 doc: update SplitGPG
    [user@devel ~/qubes-R3]$ 

Then, if you decide to merge the changes, you can call `do-merge` target with the same arguments:

    [user@build ~/qubes-R3]$ make do-merge COMPONENTS="vmm-xen core-vchan-xen" GIT_PREFIX=marmarek/qubes-

### make show-vtags

This target shows you the version tag (on HEAD) for every component.
Additionally it show you branch names. Green color mean the branch is the same
as in `builder.conf`, yellow branch name means it is different.


Building and signing the packages
---------------------------------

### make check-release-status

This targets iterate over each component with a version tag at the top, and
check if the package is already included in repository. Additionally it shows
you which repository (current, current-testing, unstable). Note that the check
requires the builder plugin to support optional `check-repo` target.

**Warning:** plugin for Debian and for Fedora checks only in local repository
directory, it does not check what is really present on the updates server.

Example usage:

    [user@build ~/qubes-R3]$ make check-release-status
    -> Checking packages for fc20 dom0
    vmm-xen: v4.4.2-3 current
    core-libvirt: v1.2.12-2 current
    core-vchan-xen: v3.0.4 testing
    core-qubesdb: v3.0.2 current
    linux-utils: v3.0.7 testing
    core-admin: v3.0.10 not released
    core-admin-linux: v3.0.4 not released
    linux-kernel: v3.18.10-2 current
    artwork: v3.0.1 current
    gui-common: v3.0.2 current
    gui-daemon: v3.0.2 current
    app-linux-split-gpg: v2.0.11 current
    app-linux-pdf-converter: v2.0.3 current
    desktop-linux-kde: no version tag
    desktop-linux-xfce4: no version tag
    manager: v3.0.3 current
    installer-qubes-os: no version tag
    antievilmaid: v2.0.8 testing
    --> Not released: core-admin core-admin-linux
    --> Testing: core-vchan-xen linux-utils core-admin core-admin-linux antievilmaid
    -> Checking packages for fc20 vm
    vmm-xen: v4.4.2-3 current
    core-vchan-xen: v3.0.4 testing
    (...)

This shows you a lists of components to build for each distribution (separate
for dom0 and VM). Then you can use those lists to really build (and sign) the packages:

    [user@build ~/qubes-R3]$ make DISTS_DOM0=fc20 DISTS_VM= COMPONENTS="core-admin core-admin-linux" qubes sign-all

The above command will build the packages only for dom0 (empty `DISTS_VM`), then sign them.


Uploading the packages to the 'current-testing' repository
----------------------------------------------------

Same as above, you can specify desired components and distributions, then call
`make update-repo-current-testing`. Actually you can call it at the same line
as the build:

    [user@build ~/qubes-R3]$ make DISTS_DOM0=fc20 DISTS_VM= COMPONENTS="core-admin core-admin-linux" qubes sign-all update-repo-current-testing

If you have not enabled `AUTOMATIC_UPLOAD` in `builder.conf`, you need to really upload them now:

    [user@build ~/src/linux-yum]$ ./sync_qubes-os.org_repo.sh r3.0

You can first call it in dry mode:

    [user@build ~/src/linux-yum]$ DRY=-n ./sync_qubes-os.org_repo.sh r3.0


Committing the packages to the 'current' repository
---------------------------------------------------

This need to be done from exactly the same instance of qubes builder where the
packages were compiled.
As the packages are already compiled you can just link them to the 'current' repository:

    [user@build ~/qubes-R3]$ make DISTS_DOM0=fc20 DISTS_VM= COMPONENTS="core-admin core-admin-linux" update-repo-current

The script will not allow you to upload there packages which were less than 7 days in 'current-testing' repository.

Other relivent Qubes Documentation
----------------------------------

Other relivent documentation is located within the `qubes-builder/docs` directory:
 
    doc/ReleaseManagerWorkflow.md
    doc/SplitGPG.md
    doc/TemplateDispVMBuild.md

