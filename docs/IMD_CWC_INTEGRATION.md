# IMD and CWC API integration

The India Meteorological Department API reference at https://api.imd.gov.in/public/api_reference.html documents GET https://api.imd.gov.in/api/v1/districtwarning?id=573 and fields Obj_id, Date, UTC, District, Day_1 through Day_5 and Day1_Color through Day5_Color.

The implemented adapter decodes warning codes 1–17 and IMD district color values: 1 red, 2 orange, 3 yellow and 4 green. It fails closed on empty, unsupported, future-dated and stale bulletins (over 36 hours old). It cannot turn a provider outage into a safety statement.

Access is controlled with IMD_API_ENABLED=true and an optional IMD_API_BEARER_TOKEN if an authorized IMD account specifies that mechanism. No credentials have been supplied. See https://api.imd.gov.in/public/register.php for registration and terms.

The Central Water Commission publishes official flood forecasts at https://ffs.india-water.gov.in/ and seven-day advisories at https://aff.india-water.gov.in/. This repository only links those sources; no licensed CWC machine-readable feed has been integrated.

The project is neither approved nor endorsed by IMD/CWC, and cannot autonomously dispatch responders, issue evacuations, or announce all-clear conditions.