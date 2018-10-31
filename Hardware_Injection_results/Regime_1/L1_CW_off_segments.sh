#!/bin/bash

/usr/bin/ligolw_segment_query_dqsegdb --segment-url https://segments.ligo.org --query-segments --include-segments L1:DCH-PCALX_SHUTTERED --gps-start-time 1164556817 --gps-end-time 1187733618 | /usr/bin/ligolw_print --table segment --column start_time --column end_time --delimiter ' ' > L1_no_injection_segments.txt
