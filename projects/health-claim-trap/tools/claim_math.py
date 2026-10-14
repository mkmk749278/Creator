#!/usr/bin/env python3
"""Every number the film computes itself (on screen: OUR CALCULATION · ...). Run to re-derive them.

1. Proportionate deduction, method as in current Arogya Sanjeevani policy wordings (Go Digit 2026: the cut applies to all
   hospital expenses except pharmacy and consumables, implants and devices, diagnostics; some wordings exempt only medicines).
   The IRDAI 2020 guidelines that set these exemptions were repealed by the 29 May 2024 master circular.
2. Insurance Ombudsman outcomes for health insurance, FY 2024-25 (CIO Annual Report 2024-25, Statement H3, totals row,
   read from the scanned table on page 47 of the report).
"""

# 1. Room rent: policy limit vs the room actually taken (illustrative example used in the VO)
LIMIT, ROOM = 5000, 8000
paid_share = LIMIT / ROOM
print(f"room limit {LIMIT}, room taken {ROOM}: insurer pays {paid_share:.1%} of room-linked charges, "
      f"cuts {1 - paid_share:.1%}")
# A worked bill for the BOARD scene: surgery + doctor + nursing are room-linked; medicines, implants, tests are not.
linked = {"room (3 days)": 3 * ROOM, "surgeon and doctor fees": 120000, "nursing": 15000}
not_linked = {"medicines and consumables": 60000, "tests": 25000}
cut = {k: round(v * (1 - paid_share)) for k, v in linked.items()}
print("  cut per head:", cut, "total cut", sum(cut.values()))
print("  no cut on:", not_linked)
# Without the rule the whole room difference would be only 3 * (ROOM - LIMIT):
print(f"  room difference alone {3 * (ROOM - LIMIT)} vs proportionate cut {sum(cut.values())}")

# 2. Ombudsman, health insurance, 1 Apr 2024 to 31 Mar 2025 (Statement H3 totals)
H3 = dict(outstanding_start=4928, received=32503, recommendations=9417, awards_for_complainant=6126,
          awards_for_insurer=4897, withdrawn=3649, non_entertainable=4928, disposed=29017,
          within_3_months=22791, three_to_12_months=4343, over_1_year=1883)
assert H3["recommendations"] + H3["awards_for_complainant"] + H3["awards_for_insurer"] + H3["withdrawn"] \
    + H3["non_entertainable"] == H3["disposed"]
assert H3["within_3_months"] + H3["three_to_12_months"] + H3["over_1_year"] == H3["disposed"]
decided = H3["recommendations"] + H3["awards_for_complainant"] + H3["awards_for_insurer"]
won = H3["recommendations"] + H3["awards_for_complainant"]
print(f"Ombudsman health FY25: received {H3['received']:,}; decided on merits {decided:,}; "
      f"for the policyholder {won:,} = {won / decided:.1%}")
print(f"  closed within 3 months {H3['within_3_months'] / H3['disposed']:.1%} of {H3['disposed']:,} disposed")
print(f"  for the policyholder as a share of all disposed: {won / H3['disposed']:.1%}")
