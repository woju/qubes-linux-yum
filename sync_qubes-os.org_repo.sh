#!/bin/sh

#DRY="-n"
USERNAME=www-admin
HOST=10.0.0.10
HOST_BASEDIR="/var/www/canadapop.com/html/pub/qubes/repo/yum"

if ! [ $# -eq 1 ]; then
    echo "usage ${0} <release>"
    exit
fi

pushd `dirname $0`
    if [ -n "$1" ]; then
        RELS_TO_SYNC=`basename "$1"`
    else
        RELS_TO_SYNC="`readlink current-release|tr -d /`"
    fi
    REPOS_TO_SYNC="current current-testing security-testing"

    for rel in $RELS_TO_SYNC; do
        # Create release directory structure if it does not exist
        [ -z "$DRY" ] && ssh $USERNAME@$HOST mkdir -p "$HOST_BASEDIR/$rel"

        rsync_args=
        for repo in $REPOS_TO_SYNC; do
            rsync_args="$rsync_args $rel/$repo"
        done

        echo "Syncing $rel..."
        rsync $DRY --partial --progress --hard-links --exclude repodata -air $rsync_args $USERNAME@$HOST:"$HOST_BASEDIR/$rel/"
        rsync $DRY update_repo.sh update_repo-arg.sh $USERNAME@$HOST:

	for repo in $REPOS_TO_SYNC; do
            [ -z "$DRY" ] && ssh $USERNAME@$HOST ./update_repo-arg.sh "$HOST_BASEDIR/$rel/$repo/dom0/fc*" "$HOST_BASEDIR/$rel/$repo/vm/fc*"
        done
    done
popd
