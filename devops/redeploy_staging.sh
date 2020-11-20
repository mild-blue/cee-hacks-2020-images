#!/bin/bash
set -e

echo "Redeploying staging."
ssh "images@206.189.248.138" "cd /srv/cee-hacks-2020-images && ./redeploy.sh"
echo "Done."