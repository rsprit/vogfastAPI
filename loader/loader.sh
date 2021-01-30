#!/bin/bash

bash get_data.sh "$VOG_DATA" && python generate_db.py "$VOG_DATA"

