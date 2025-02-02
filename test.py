import re

text = """
"Perfection Requirements" means any and all registrations, filings, notices and other
actions and steps required to be made in any jurisdiction in order to perfect security created
by the Transaction Security Documents or in order to achieve the relevant priority for such
Security;

"Permitted Acquisition" means:

(a) the Acquisition;

(b) any acquisition permitted by the Majority Lenders;

(c) an acquisition by a member of the Group of an asset sold, leased, transferred or
otherwise disposed of by another member of the Group in circumstances constituting
a Permitted Disposal;

(d) an acquisition of shares or securities pursuant to a Permitted Share Issue or
Permitted Joint Venture;

(e) an acquisition of securities which are Cash Equivalent Investments so long as, if
acquired by an Obligor, those Cash Equivalent Investments become (subject to the
Agreed Security Principles) subject to the Transaction Security as soon as is
reasonably practicable;

(f) the incorporation of a company or the acquisition of an off-the-shelf company (in
each case, other than by the Parent) which on incorporation or acquisition becomes
a member of the Group, but only if that company is incorporated in a Permitted
Jurisdiction with limited liability;

(g) an acquisition of (A) a Controlling Interest of a limited liability person or (B) a
business or undertaking carried on as a going concern (in each case the

38
EUS\HCB\400080815 15


-----

"Acquisition Target") by a member of the Group (other than the Parent), but only
if:

(i) no Event of Default or Material Event of Default is continuing as at the date a
member of the Group legally commits to make the acquisition or would (by
reference to the facts and circumstances existing at that date) occur as a
result of the acquisition;

(ii) the Acquisition Target is and, if the Acquisition Target is the Holding Company
of one or more Subsidiaries, its Subsidiaries are, or are engaged in, a business
substantially the same as, complementary or related to that carried on by the
Group (for the avoidance of doubt, technology related acquisitions shall be
considered as the same as, complementary or related to the business carried
on by the Group);

(iii) the Acquisition Target is and, if the Acquisition Target is the Holding Company
of one or more Subsidiaries, its Subsidiaries are, incorporated, established
and/or carries on its principal business or is a business or undertaking carried
on (as applicable) in a Permitted Jurisdiction;

(iv) the Acquisition Target and, if the Acquisition Target is the Holding Company
of one or more Subsidiaries which will become members of the Group at the
same time as the Acquisition Target, the Acquisition Target and each such
Subsidiary will, once acquired, have, so far as the Parent is aware having
made due and careful enquiries, no contingent or off-balance sheet liabilities
which did not arise in the ordinary course of business and are material and
which would be required to be shown on a balance sheet in accordance with
the relevant Accounting Principles other than:

(A) any such liability which is indemnified or cash collateralised in full by
or on behalf of the relevant vendor or insured by a reputable insurer
or guaranteed by an Acceptable Bank;

(B) where the maximum amount of such liability which is likely to become
an actual liability is fully taken into account in determining the
purchase price payable for the Acquisition Target;

(C) where the proceeds of Acceptable Funding Sources (Excluding Debt
and Retained Cash) will be and are invested in the Group to fund the
maximum amount of such liability which is likely to become an actual
liability on or before such liability becomes due for payment; or

(D) where such liability would be permitted, or not restricted, under the
terms of the Finance Documents;

(v) with respect to any acquisition which is funded in whole or in part from the
proceeds of any Facility, the Parent has delivered a certificate, signed by its
finance director or chief executive officer, to the Facility Agent at least three
Business Days prior to the date a member of the Group legally commits to the
proposed acquisition (accompanied by reasonably detailed calculations and
assumptions) confirming that Adjusted Leverage (as at the most recent
Quarter Date for which financial information is available to calculate such ratio
before the relevant member of the Group legally commits to make the
proposed acquisition and pro forma for the acquisition) did not exceed 5.75:1;
and

(vi) the Parent has delivered a certificate, signed by its finance director or chief
executive officer, to the Facility Agent at least three Business Days prior to

39
EUS\HCB\400080815 15


-----

the date a member of the Group legally commits to the proposed acquisition
(accompanied by reasonably detailed calculations and assumptions)
confirming that the Parent:

(A) was in compliance with the financial covenants set out in clause 26.2
(Financial condition) as at the most recent Quarter Date for which
financial information is available to calculate such ratio before the
relevant member of the Group legally commits to make the proposed
acquisition; and

(B) would have been in compliance with the financial covenants set out in
clause 26.2 (Financial condition) as at the most recent Quarter Date
for which financial information is available to calculate such ratio before
the relevant member of the Group legally commits to make the
proposed acquisition if the calculations were adjusted to be pro forma
for the acquisition;

(vii) save where the Total Purchase Price is fully funded by New Shareholder
Injections (other than any New Shareholder Injection contributed for the
purpose of an equity cure pursuant to clause 26.4 (Equity Cure)), in the case
of a single acquisition the Total Purchase Price of which (less the amount
funded by Acceptable Funding Sources (Excluding Debt and Retained Cash))
is greater than £50,000,000 (or its equivalent in any other currency) but less
than or equal to £75,000,000 (or its equivalent in any other currency), the
Parent shall supply to the Facility Agent for the Lenders by no later than five
Business Days prior to the date a member of the Group legally commits to
make the relevant acquisition, a copy of any due diligence reports obtained
by the Group in relation to the Acquisition Target, on a non-reliance basis
(subject to the Facility Agent and any other relevant Reliance Party signing
any required hold harmless letter) and the acquisition agreement under which
the Acquisition Target is to be acquired; and

(viii) save where the Total Purchase Price is fully funded by New Shareholder
Injections (other than any New Shareholder Injection contributed for the
purpose of an equity cure pursuant to clause 26.4 (Equity Cure)), in the case
of a single acquisition the Total Purchase Price of which (less the amount
funded by Acceptable Funding Sources (Excluding Debt and Retained Cash))
is greater than £75,000,000 (or its equivalent in any other currency), the
Parent shall supply to the Facility Agent for the Lenders by no later than five
Business Days prior to the date a member of the Group legally commits to
make the relevant acquisition, a copy of financial and legal due diligence (if
such diligence has been commissioned by the Group) and any other due
diligence reports obtained by the Group in relation to the Acquisition Target,
and shall use all reasonable endeavours to do so on a reliance basis (subject
to the Facility Agent and any other relevant Reliance Party signing any
required reliance letter) and the acquisition agreement under which the
Acquisition Target is to be acquired;

(h) any acquisition which is funded entirely using New Shareholder Injections; and

(i) if a Controlling Interest which is less than 100 per cent of the issued share capital or
equivalent ownership interest of an Acquisition Target has been the subject of a
Permitted Acquisition under paragraph (g) above or if a member of the Group intends
to acquire the shares or other ownership interests which it does not already own in
a Joint Venture which is already a Permitted Joint Venture, the acquisition of all or
part of the balance of the shares or other ownership interest in such Acquisition
Target or Permitted Joint Venture provided that:

40
EUS\HCB\400080815 15


-----

(i) no Event of Default or Material Event of Default is continuing as at the date a
member of the Group legally commits to make the acquisition or would (by
reference to the facts and circumstances existing at that date) occur as a
result of the acquisition; and

(ii) with respect to such acquisition which is funded in whole or in part from the
proceeds of any Facility the Parent has delivered a certificate, signed by its
finance director or chief executive officer, to the Facility Agent at least three
Business Days prior to the date a member of the Group legally commits to the
proposed acquisition (accompanied by reasonably detailed calculations and
assumptions) confirming that Adjusted Leverage (as at the most recent
Quarter Date for which financial information is available to calculate such ratio
before the relevant member of the Group legally commits to make the
proposed acquisition) did not exceed 5.75:1,

in each case, pro-forma for the acquisition, any Utilisation in connection with the acquisition
and taking into account Permitted Synergies;

For the purposes of this definition, an acquisition of a "Controlling Interest" means more
than 50 per cent of the voting share capital (or equivalent ownership interest);

"Permitted Bolt-on Acquisition" means a Permitted Acquisition under paragraph (g)
and/or (i) of the definition of that term;

"Permitted Acquisition Clean-Up Period" means, in relation to a Permitted Bolt-on
Acquisition, the period beginning on the closing date for that acquisition and ending on the
date falling 90 days after that closing date or on such other date agreed by the Majority
Lenders;
"""

pattern = r'"Permitted ([A-Za-z\s-]+)" means:(.*?)(?=(?:\n\n|")"Permitted|$)'
matches = re.findall(pattern, text, re.DOTALL)

definitions = {key.strip(): value.strip() for key, value in matches}

for key, value in definitions.items():
    print(f"{key}:\n{value}\n")