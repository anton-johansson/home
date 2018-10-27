#!/usr/bin/env python3

import xmlrpc.client;
from sys import argv;

# Constants
endpoint = "https://api.loopia.se/RPCSERV";
subdomain = "home";

def main():
    if len(argv) != 5:
        print("Expected exactly 4 arguments");
        return 1;

    # Input
    username = argv[1];
    password = argv[2];
    domain = argv[3];
    address = argv[4];

    # Create the XMLRPC client
    with xmlrpc.client.ServerProxy(endpoint) as client:
        records = client.getZoneRecords(username, password, domain, subdomain);
        print("Found records: " + str(records));

        # Find an existing record
        recordId = 0;
        if len(records) > 0:
            if records[0]["rdata"] == address:
                print("No need to update the record, because it has the same value, exiting...");
                return;
            recordId = records[0]["record_id"];

        # Build the object
        record = {
            "type": "A",
            "rdata": address,
            "record_id": recordId,
            "ttl": 3600,
            "priority": 0
        };

        if recordId > 0:
            # Update the existing record
            print("Updating record " + str(recordId) + " for '" + subdomain + "." + domain + "' with address: " + address);
            response = client.updateZoneRecord(username, password, domain, subdomain, record);
            print("Response: " + str(response));
        else:
            # Create a new record
            print("Creating a new record for '" + subdomain + "." + domain + "' with address: " + address);
            response = client.addZoneRecord(username, password, domain, subdomain, record);
            print("Response: " + str(response));

# Run main method
if __name__ == '__main__':
    main();
