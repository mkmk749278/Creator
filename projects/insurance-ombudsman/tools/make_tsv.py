#!/usr/bin/env python3
"""One-off generator of script v1 (record only; edit script.full.tsv after this).

The owner's directive (handoff/owner-directive.md, 2026-10-15) kept line by line, in the owner's order and voice. Changes:
formatting for the English VO lint (no ! quotes dashes or digits; acronyms hyphen-spelled as the owner wrote them;
the owner's [sigh]/[pause]/[slight smile] cues moved to the pacing column, CLAUDE.md: no emotion cues in English VO),
and every claim the owner's own asset pack (handoff/asset-pack/SCRIPT_CORRECTIONS.md) or the CIO pages found
unsupported. Each changed line carries a `# was:` comment with the owner's text and the reason.
"""
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
C1, C2, C3, C4 = ("1 The rejection email and the two doors", "2 Bima Bharosa, the Ombudsman and the middleman",
                  "3 The two-step clock", "4 Filing, the hearing and the award")
ILL = "ILLUSTRATIVE FOOTAGE"

# (section, en, visual, onscreen, sound, pacing)
L = [
    # Series continuity (owner, 2026-10-15: "maintain natural flow ... look at the first video"; then: "give glimpses of
    # the first video, but even with the second video they need to understand everything; no need to watch"): Episode 01
    # (projects/health-claim-trap) left a family at a hospital counter at 9 PM with a ₹4.5 lakh bill and a denied
    # cashless claim, and gave a four-step plan ending at the Ombudsman. Episode 02 is step four, opened up: same family,
    # same bill, same SIMULATION documents and the four-step staircase, no contradiction of Episode 01's advice.
    # was: "In our last video, we saw what to do when the hospital desk rejects your cashless claim at nine o'clock at night."
    (C1, "Imagine you are standing at a hospital billing counter at nine o'clock at night. The bill is four and a half lakh rupees, and your cashless claim, where the insurance company pays the hospital directly, has just been denied. We told this story in our last video.",
     "Glimpse from Episode 01's final cut (2–4 s): the counter, then its SIMULATION bill ₹4,50,000 and the red CASHLESS DENIED stamp (same design).",
     "FROM EPISODE 1 · SIMULATION", "Hospital room tone; logo bug from 0:02", "Cold open, no music for 2 s"),
    # new line: the four steps from Episode 01 (E044-E056), so a new viewer knows where this film starts
    (C1, "Here is what you need to know from it. A cashless denial is not the end of your claim. You can pay the hospital, and claim the money back later. And if the company still says no, there is a four-step plan. Collect your papers. File for reimbursement and write to the grievance officer. Register on Bima Bharosa. And step four, the Insurance Ombudsman.",
     "Episode 01's four-step staircase rises lower left; steps 1 to 4 light in turn; step 4 stays lit.", "STEP 1 · 2 · 3 · 4", "Four soft ticks", ""),
    # was: "You paid the bill from your pocket ..." (owner's line, kept)
    (C1, "So you paid the bill from your pocket, collected your hospital papers, came home, and filed for reimbursement.",
     "F01 phone and card insert, PX15 rupee notes; F09 papers to keyboard match cut.", ILL, "Card beep, paper rustle", ""),
    (C1, "Three weeks later, an email lands in your inbox.",
     "PX06/F01 phone in hand; an unbranded email slides in (SIMULATION, no insurer logo).", "SIMULATION",
     "Notification ping", "[sigh] beat before the line (owner's cue)"),
    # was: "out of a four lakh rupee hospital bill, they approve just one lakh twenty thousand, and silently cut the
    # remaining two lakh eighty thousand rupees!" (Episode 01's bill was ₹4.5 lakh; the cut follows from it)
    (C1, "Either the insurance company rejects your claim all over again... or worse, out of your four and a half lakh rupee bill, they approve just one lakh twenty thousand, and silently cut the remaining three lakh thirty thousand rupees.",
     "G01 Claim Deduction (amounts re-set to Episode 01's bill): total, approved part fills, the cut peels away in coral.",
     "₹4,50,000 BILL · ₹1,20,000 PAID · ₹3,30,000 CUT · EXAMPLE", "Small transient on the cut", ""),
    (C1, "At that moment, most middle-class families think they only have two choices.",
     "A dim corridor splits into two doors (ILLUSTRATION).", "", "", ""),
    # was: "spend fifty thousand rupees in legal fees, and wait five years for a verdict" (no source for either number,
    # SCRIPT_CORRECTIONS row 2; consumer commissions do not require a lawyer either)
    (C1, "Choice one. Hire a lawyer, go to consumer court, pay the fees, and wait, often for a long time, for a verdict.",
     "Left door: F02 paper detail, case files stacking (no dusty five-year court graphic).", "", "", ""),
    # was: "Click on one of those flashy Instagram or YouTube ads for a private claim recovery startup... who promises to
    # fight your case, but demands twenty percent of your hospital money as their commission!" (20% kept as the
    # owner's example, framed as "some ask"; fact-check row IO-06)
    (C1, "Or choice two. Answer one of those ads for a private claim recovery service, which promises to fight your case, but some ask for as much as twenty percent of the money they recover as their fee.",
     "Right door: F08 a hand signing an unbranded agreement; phone ad frame (SIMULATION, no real brand).", "SIMULATION", "", ""),
    # was: "[pause] Stop right there. Both of those choices are a trap." (a court can be the right remedy; the film offers
    # a third door instead of calling the court a trap)
    # was: "[pause] Stop right there. Both of those choices are a trap." (a court can be the right remedy)
    (C1, "Stop right there. Before you pick either door, there is a third one. Step four of that plan.",
     "Both doors dim; the lit step 4 of the staircase becomes a third door opening in teal light (ILLUSTRATION).", "STEP 4",
     "Music out 1.5 s before, then a low thud", "[pause] before the line (owner's cue)"),
    # was: "What nobody tells you... is that the Government of India created a special judicial weapon where filing costs
    # zero rupees, the verdict is one hundred percent binding ... a mandatory penalty of five thousand rupees for every
    # single day of delay" (Episode 01 already introduced the Ombudsman, so "nobody tells you" would contradict it; the
    # award binds the insurer only; the penalty is per IRDAI FAQ 45 / master circular para 20)
    (C1, "Today, we open that door fully, from start to finish. Filing a complaint costs zero rupees. If the Ombudsman passes an award, it is binding on the insurance company. And if the company pays that award late, it has to pay you a penalty of five thousand rupees for every day of delay.",
     "G04 Binding Award panel reveal; S01 Rules p11 push-in on the award clause.",
     "FREE TO FILE · AWARD BINDS THE INSURER · ₹5,000 / DAY LATE [IRDAI HEALTH MASTER CIRCULAR | 2024]", "", ""),
    (C1, "Welcome to Be Practical with Kishore.", "Logo sting over F14 Hyderabad (faceless film, owner 2026-10-15).", "", "Logo sting", ""),
    # was: "Today, let's unlock the Insurance Ombudsman. I will show you the exact mistake that got seventeen hundred
    # families thrown out last year, the portal to use, and how to get your money back in sixty days without giving a
    # single rupee to middlemen." (1,715 not verified at table level; no 60-day outcome: Rule 17 gives three months)
    (C1, "Today, I will show you the one mistake that gets complaints turned away at the door, how to file on the official website step by step, what happens at the hearing, and what the company must do after it loses. All without paying a single rupee to middlemen.",
     "Quick preview: RETURNED stamp, cioins.co.in typed, a hearing frame, the ₹5,000 meter (F09, F12, G06).", "", "", ""),
    (C1, "Let's break it down... in plain, simple English.", "Title card over F14.", "THE INSURANCE OMBUDSMAN", "", ""),

    # was: "First... let's clear up the single biggest confusion on the internet. When your claim is rejected, many people
    # tell you: Go file a complaint on the Bima Bharosa portal!" (Episode 01 made Bima Bharosa step three, so this film
    # must not call it a mistake; it explains why step three alone is not the end)
    (C2, "First... step three, Bima Bharosa, the online complaint portal of the insurance regulator, the I-R-D-A-I. Many families stop there, and here is why that is not enough.",
     "Staircase: step 3 lights; S07 Bima Bharosa home page push-in (the same capture as Episode 01).", "STEP 3 · bimabharosa.irdai.gov.in", "", ""),
    # was: "Ten days later, you get the exact same copy-paste rejection letter ... and the case is marked closed!"
    # (kept as a common experience, not a promise of what always happens)
    (C2, "You register on Bima Bharosa, upload your papers, and wait. Many people then get the same rejection letter from the insurance company again, and the complaint is closed.",
     "The same unbranded letter returns (SIMULATION); no fabricated portal screenshot.", "SIMULATION", "", ""),
    (C2, "And you think, even the government portal could not help me.", "PX05 a man in a dim room, head in hand.", ILL, "", ""),
    # was: "Bima Bharosa is NOT a court. It is simply an administrative post-office tracking system run by the regulator
    # ... automatically sends that ticket right back ... zero legal power to order an insurance company to pay"
    (C2, "Here is why. Bima Bharosa is useful. Your complaint goes on the regulator's record, and the company has to answer it. But Bima Bharosa is NOT a court. Your complaint goes to the same insurance company that cut your claim, and the I-R-D-A-I tracks how the company handles it. Bima Bharosa does not decide your claim, and it cannot pass an order telling the company to pay you.",
     "Animated ticket travels from the phone to the insurer's inbox; an IRDAI tracker follows it (ILLUSTRATION).",
     "TRACKS · DOES NOT DECIDE [BIMA BHAROSA | IRDAI]", "", ""),
    # was: "The body that has the statutory power to pass a binding payment order... is the Insurance Ombudsman"
    (C2, "That is why step four exists. The body that can pass a binding award in your case... is the Insurance Ombudsman, set up under the Insurance Ombudsman Rules, twenty seventeen.",
     "S03 FAQ → S01 Rules cover push-in, gold highlighter.", "[INSURANCE OMBUDSMAN RULES | 2017]", "", ""),
    (C2, "Now, look at the second trap. Private claim recovery companies.", "F08 agreement on a desk.", ILL, "", ""),
    # was: "Suppose your four lakh rupee claim is stuck ... give us twenty percent plus G-S-T. That is nearly ninety
    # thousand rupees" (same family as Episode 01: the stuck money is the ₹3.3 lakh cut; 20% = ₹66,000; with 18% GST
    # = ₹77,880; the GST rate is our assumption, labelled on screen)
    (C2, "Suppose your three lakh thirty thousand rupees is stuck. A recovery agency tells you, sign our agreement, and if we get your money back, give us twenty percent plus G-S-T.",
     "G02 Commission Example (re-set to ₹3,30,000): the claim strip.", "EXAMPLE", "", ""),
    (C2, "Twenty percent of three lakh thirty thousand is sixty-six thousand rupees. Add eighteen percent G-S-T, and it is seventy-seven thousand eight hundred and eighty rupees out of your family's medical savings.",
     "G02: fee splits off, GST joins last.", "₹66,000 FEE + 18% GST = ₹77,880 · OUR CALCULATION", "Coin tick per figure", ""),
    # was: "Under Rule Fourteen ... commercial middlemen and recovery companies are strictly NOT allowed to file
    # complaints before the Ombudsman! Only you, the policyholder, or your family heirs, can file."
    (C2, "And here is what they may not tell you. Under Rule fourteen of the Insurance Ombudsman Rules, the complaint is made by you, the person with the grievance, or through your legal heir, nominee or assignee.",
     "S01 Rules p9 crop to Rule 14(1), cyan overlay on the eligible complainants.", "[RULE 14 | INSURANCE OMBUDSMAN RULES]", "", ""),
    # was: "These companies simply take your password ... pocket ninety thousand rupees ... for doing ten minutes of typing."
    # (no stock actor shown as a fraudster; not every service is a racket, SCRIPT_CORRECTIONS row 3)
    (C2, "The form is the same free form on the official website that you can fill in yourself. And never share your passwords or O-T-Ps with anyone.",
     "F01 phone with a lock overlay (original graphic).", "", "", ""),
    # was: "under Section Twenty-Three of the Indian Contract Act, any contract where an agency promises to represent you
    # before the Ombudsman for a commission is legally void!" (no binding decision found for the blanket claim; removed)
    (C2, "So before you sign any agreement and give away a share of your money, remember. You can do this yourself online, for zero rupees.",
     "G02 the fee strip folds back into the family's money (ILLUSTRATION).", "FILING FEE: ₹0 [CIO FAQ]", "", ""),

    (C3, "Now listen carefully. You cannot jump straight to the Ombudsman on the day your claim is rejected.",
     "A closed glass door, the case file in hand (ILLUSTRATION).", "", "", ""),
    (C3, "If you do, your complaint can be turned away at the door.", "A red RETURNED stamp on a file (SIMULATION).", "", "Stamp thud", ""),
    # was: "In the year twenty twenty-four, twenty-five, seventeen hundred and fifteen families had their health complaints
    # thrown out by the Ombudsman for this exact reason." (count and cause not verified, SCRIPT_CORRECTIONS row 5;
    # fact-check row IO-12 may restore a sourced figure)
    (C3, "Every year, many complaints are not even taken up, because one basic step was missed.", "", "", "", ""),
    (C3, "Under Rule fourteen, you must follow a two-step clock.", "G03 Process Clocks: two dials appear.", "THE TWO-STEP CLOCK", "", ""),
    # was: "Clock Step One: Write to the insurance company's Grievance Redressal Officer, the G-R-O." (Rule 14(3)(a):
    # a representation to the insurer; the GRO is the practical address)
    (C3, "Clock step one. This is step two of our plan. Complain in writing to the insurance company, best of all to its Grievance Redressal Officer, the G-R-O.",
     "F09 typing; an illustrative email builds: policy number, claim number, amount, reason (invented numbers).", "SIMULATION", "Keyboard", ""),
    (C3, "Every insurer publishes its grievance officer's email on its website. Send one calm, formal email with your policy number, your claim number, and why their deduction is wrong.", "", "", "", ""),
    (C3, "Keep a copy of that email and every reply. You will need them later.", "F07/F10 the email, the reply and the bills drop into one folder.", "", "", ""),
    (C3, "Under the I-R-D-A-I rules, the company should resolve your grievance within fourteen days.",
     "G03 first dial: fourteen days.", "14 DAYS [IRDAI POLICYHOLDERS' INTERESTS MASTER CIRCULAR | 2024]", "", ""),
    # was: "Clock Step Two: Wait for their reply, or wait for thirty days." (Rule 14(3): one month)
    (C3, "Clock step two. Wait for their reply, or wait one month.", "G03 second dial: one month.", "1 MONTH [RULE 14(3)]", "", ""),
    (C3, "The moment the company rejects your complaint, or you are not happy with its reply, or one month passes with no reply at all... the door to the Ombudsman opens.",
     "G03 two branches: unsatisfactory reply / no reply; the glass door opens.", "", "", ""),
    # was: "for any claim up to fifty lakh rupees" (the limit is on compensation sought / loss payable)
    (C3, "From that day, you have one year to file your complaint with the Ombudsman, for compensation of up to fifty lakh rupees.",
     "S01 Rules p9 (one year) then p11 (cap) as two separate crops.", "1 YEAR · UP TO ₹50 LAKH [CIO FAQ]", "", ""),
    (C3, "That limit was raised to fifty lakh rupees in November twenty twenty-three.",
     "Gazette page push-in.", "[GAZETTE G.S.R. 828(E) | 2023]", "", ""),
    # was: "Do NOT file a case in Consumer Court at the same time. The Ombudsman can only take your dispute if it is not
    # pending in any other court." (the bar also covers cases already decided, and arbitration)
    (C3, "And remember one strict condition. The Ombudsman cannot take your complaint if the same dispute is already pending, or already decided, in any court, consumer forum, or arbitration.",
     "S01 Rules p9 crop: pending OR disposed of.", "PENDING OR DECIDED ELSEWHERE = NOT ALLOWED [RULE 14(3)]", "", ""),

    (C4, "So, how do you actually file, and what happens next?", "", "", "", ""),
    (C4, "Open your browser and go to the official website, c-i-o-i-n-s dot co dot in.", "G07 step 1, cioins.co.in typed (labelled schematic).", "cioins.co.in", "Typing", ""),
    # was: "Click on Online Complaint Registration and log in with your mobile number O-T-P."
    (C4, "Choose Register Complaint, and verify your mobile number with an O-T-P.", "G07 step 1 stepper; no real OTP shown.", "ILLUSTRATION", "", ""),
    # was: "Based on your address proof, the system automatically assigns your case to one of the seventeen regional
    # Ombudsman offices across India" (18 offices since Thane, Dec 2024; the complainant chooses the centre)
    (C4, "Then you choose your Ombudsman office. There are eighteen offices across India, in cities like Hyderabad, Bengaluru, Mumbai, Delhi and Kolkata. You pick the one that covers the place where you live, or the insurance company's branch that handled your policy.",
     "G08 Regional Offices board: Hyderabad lights first, then the rest (a directory board, not a map).",
     "18 OMBUDSMAN OFFICES [CIO OFFICE DIRECTORY]", "", ""),
    # was: "combine four documents into one clean P-D-F" (the portal has separate fields, PDF/JPG, 10 MB each)
    (C4, "Before you submit, keep these documents ready.", "G05 Document Checklist frame.", "", "", ""),
    (C4, "One. A copy of your insurance policy.", "G05 document 1 flies into its slot.", "", "Paper flick", ""),
    (C4, "Two. The hospital discharge summary and the itemised final bill.", "G05 document 2.", "", "Paper flick", ""),
    (C4, "Three. The company's rejection or deduction letter.", "G05 document 3.", "", "Paper flick", ""),
    (C4, "Four. A copy of the complaint you sent to the insurance company.", "G05 document 4.", "", "Paper flick", ""),
    (C4, "And five. Your I-D and address proof, and a photograph. Each file can be a P-D-F or a J-P-G, up to ten M-B.",
     "G05 extra slot; the portal's field list (credited capture).", "PDF / JPG · MAX 10 MB EACH [CIOINS.CO.IN]", "", ""),
    # was: "the system emails you a short one-page summary called Form Annexure Six-A. Sign it, upload it back, and your
    # case is registered!" (not confirmed as the current workflow; the portal says it verifies, then registers)
    (C4, "Check every detail, tick the declaration, and submit. Your complaint is verified first, and then registered. Save the acknowledgement and your complaint number.",
     "G07 step 4 review state; F10 saving the acknowledgement (no real complaint number).", "SIMULATION", "", ""),
    (C4, "Now, what happens next?", "", "", "", ""),
    # was: "In FY twenty twenty-four to twenty-five, over forty percent of health complaints were settled quickly through
    # Mediation under Rule Sixteen!" (40% not verified; CIO 2024-25 H3: 9,417 recommendations of 29,017 disposed =
    # about one in three, our calculation, fact-check row IO-24)
    (C4, "Many complaints end in mediation under Rule sixteen. The Ombudsman suggests a fair settlement, and if both sides agree, the case closes. Last year, about one in three health complaints that were closed, ended this way.",
     "Two document cards slide together (ILLUSTRATION); S01 Rules p10 crop.",
     "≈ 1 IN 3 · OUR CALCULATION [CIO ANNUAL REPORT | 2024–25]", "", ""),
    (C4, "Often, once the Ombudsman's notice reaches the insurer, the company agrees to pay before any hearing takes place.",
     "", "", "", ""),
    # was: "you get a link for a fifteen-minute video call" (no fixed duration; hearings can be in person or online)
    (C4, "If there is no settlement, there is a hearing. It can be in person, or online by video.",
     "F12 hearing room, labelled; F11 detail.", "ILLUSTRATIVE HEARING", "", ""),
    # was: "You can speak in simple English, Hindi, or your regional language. The Ombudsman asks three simple questions"
    # (no universal questionnaire; language claim not verified)
    (C4, "You don't need fancy legal words. Explain your case simply. When did you buy the policy? Why were you in the hospital? And how much did the company cut?",
     "F07 / F19 hand crop over papers.", "", "", ""),
    # new line, the honest answer to the owner's "sixty days": the same CIO 2024-25 figure Episode 01 used (E055)
    (C4, "And how long does it take? In twenty twenty-four to twenty-five, about eight out of ten health complaints were closed within three months.",
     "A calendar strip fills to three months; 8 of 10 files close.", "8 IN 10 WITHIN 3 MONTHS [CIO ANNUAL REPORT | 2024–25]", "", ""),
    (C4, "And here is why this law is built for you.", "", "", "", ""),
    # was: "Under Rule Seventeen ... it is one hundred percent legally binding on the insurance company!"
    (C4, "First. Under Rule seventeen, when the Ombudsman passes an award, it is binding on the insurance company.",
     "G04 insurer panel locks.", "[RULE 17 | INSURANCE OMBUDSMAN RULES]", "", ""),
    # was: "The award is binding on the company, but it is NOT binding on you! ... your right to go to Consumer Court is
    # still completely open." (other remedies may remain available; not promised as "completely open")
    (C4, "Wait... what if you are NOT happy with the award? You don't have to accept it. Other legal remedies, like the consumer forum, may still be open to you.",
     "G04 complainant panel: other remedies.", "", "", "[pause] before Wait (owner's rhythm)"),
    # was: "Under Chapter One, Paragraph Twenty of the twenty twenty-four I-R-D-A-I Health Master Circular... the insurance
    # company has exactly thirty days to pay your money." (the 30 days run from the insurer's receipt of the award)
    (C4, "And second. Under the I-R-D-A-I health master circular of twenty twenty-four, the insurance company must carry out the award within thirty days of receiving it.",
     "S01 Rules p11 / S06 FAQ crop; G06 receipt-date marker.", "30 DAYS FROM RECEIPT [IRDAI HEALTH MASTER CIRCULAR | 2024]", "", ""),
    # was: "plus penal interest at the R-B-I Bank Rate plus two percent!" (the formula is not printed in Rule 17;
    # pending fact-check row IO-31; "mandatory" kept out)
    (C4, "If it is late, it must pay you a penalty of five thousand rupees for every day of delay, on top of any interest that is due.",
     "G06 Delay Penalty: deadline marker.", "₹5,000 / DAY [IRDAI HEALTH FAQ 45]", "Small transient", ""),
    # was: "If they delay by fifty days, that is two and a half lakh rupees in penalty paid straight into your bank
    # account." (no automatic credit; days counted after the 30-day deadline)
    (C4, "Ten days late, that is fifty thousand rupees. Thirty days late, one lakh fifty thousand rupees.",
     "G06 counter: 1, 10, 30 days late.", "10 DAYS = ₹50,000 · 30 DAYS = ₹1,50,000 · OUR CALCULATION", "Ticks", ""),
    # was: "the Bombay High Court ruled in December twenty twenty-four that courts can order these delay penalties
    # recovered directly from the personal salaries of the defaulting insurance officers!" (Dedhia, 9 Dec 2024: case-
    # specific costs and interest, recovered from responsible officers after an inquiry; fact-check row IO-34)
    (C4, "And in December twenty twenty-four, in one case where a policyholder was made to fight for years, the Bombay High Court ordered the insurance company to pay costs, and said the money should be recovered from the officers responsible, after an inquiry.",
     "Court exterior still with slow push (credited), judgment text crop.", "[BHARAT HIRJI DEDHIA v. UNION OF INDIA | BOMBAY HC | 2024]", "", ""),
    (C4, "That is the power of knowing your rights. You don't need connections, and you don't need to pay twenty percent to middlemen.",
     "F14 Hyderabad dusk.", "", "", "[slight smile] (owner's cue)"),
    (C4, "Be smart. Be informed. And always... be practical.", "Logo.", "", "", ""),
    # was: "expose how hospitals inflate surgical consumables, and the exact government price caps they violate" (no
    # allegation in a teaser; NPPA caps exist only for some items)
    (C4, "In our next episode, we look at consumables, the gloves, masks and syringes on your bill. We will open a five lakh rupee hospital bill, line by line, look at what we pay for surgical consumables, and the price caps the government has set on some of them.",
     "F13 detail, bill close-up (SIMULATION).", "NEXT EPISODE", "", ""),
    (C4, "Hit the subscribe button, share this video with your family, and drop your questions below. I'll see you in the next video.",
     "End card.", "EDUCATIONAL ONLY · NOT LEGAL ADVICE", "", ""),
]

with open(HERE / "script.full.tsv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["id", "section", "te", "en", "emotion", "visual", "onscreen", "sound", "pacing"])
    for i, (sec, en, vis, ons, snd, pac) in enumerate(L, 1):
        w.writerow([f"O{i:03d}", sec, "", en, "", vis, ons, snd, pac])
print(len(L), "lines")
