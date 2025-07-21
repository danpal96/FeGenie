#!/usr/bin/env python3

import gzip
from pathlib import Path

from pyhmmer.plan7 import HMMFile
import requests

for path in Path("hmms/iron/").glob("*/*.hmm"):
    accession_list = []
    with HMMFile(path) as file:
        for hmm in file:
            if hmm.accession:
                accession = hmm.accession.decode()
                if accession.startswith("PF"):
                    accession_list.append(accession.split(".")[0])
    if accession_list:
        with open(path, "wb") as out_file:
            for accession in accession_list:
                print(f"Downloading {accession}...")
                res = requests.get(f"https://www.ebi.ac.uk/interpro/wwwapi//entry/pfam/{accession}?annotation=hmm")
                res.raise_for_status()
                out_file.write(gzip.decompress(res.content))

