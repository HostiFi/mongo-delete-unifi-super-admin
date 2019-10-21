import crypt
import os
import string
from random import SystemRandom
import argparse
import pymongo

parser = argparse.ArgumentParser()
parser.add_argument('-u','--username', help='UniFi username of Super Admin to delete')
args = parser.parse_args()

if args.username is not None:
    print "Deleting UniFi Super Admin"
    print "Connecting to MongoDB..."
    site_ids = []
    client = pymongo.MongoClient("mongodb://127.0.0.1:27117/ace")
    mdb = client.ace
    print "Finding Admin ID..."
    db_dump = mdb.site.find()
    admin_list = mdb.admin.find()
    for admin in admin_list:
        try:
            if admin["name"] == args.username:
                admin_id = str(admin["_id"])
        except:
            continue
    print "Deleting Admin..."
    mdb.admin.remove({'name': args.username})
    for site in db_dump:
        site_id = str(site["_id"])
        site_ids.append(site_id)
    print "Removing privileges from all sites..."
    for site_id in site_ids:
        mdb.privilege.remove({"admin_id" : admin_id, "site_id" : site_id})
    print "Done!"

else:
    print "Error: Missing argument. --username is required."
