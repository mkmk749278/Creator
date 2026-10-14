#!/usr/bin/env python3
"""One-off: script v2 from the owner's "Master Handoff & Fixes" (handoff/master-handoff-fixes.pdf, 2026-10-14).

The owner's text is kept word for word except (a) format: no `!`, double quotes or long dashes in TTS text, and the
square-bracket cues move to the emotion column; (b) the sentences listed in FIXES, changed only where claims.csv says the
original is wrong or unsourced. Picture, on-screen text and sound reuse the v1 rows (`v1/script.full.tsv`) named in V1.
From now on edit script.full.tsv directly and run build_script.py."""
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
v1 = {r["id"]: r for r in csv.DictReader(open(HERE / "v1/script.full.tsv", encoding="utf-8"), delimiter="\t")}
C1, C2, C3, C4 = ("1 The midnight bill", "2 Who really says no", "3 The five year rule and the clock",
                  "4 The four step plan and buyer rules")

# id, chapter, emotion, VO text (owner's, formatted), v1 row whose picture/on-screen/sound it uses, extra pacing note
R = [
 ("E001", C1, "", "Imagine this situation... it happens to thousands of middle-class families in India every single day.", "H001", ""),
 ("E002", C1, "", "You pay thirty-five thousand rupees every year for health insurance. You renew it on time for five or six straight years. You never miss a single payment.", "H002", ""),
 ("E003", C1, "", "Then, an emergency hits. Your loved one is admitted to the hospital.", "H003", ""),
 ("E004", C1, "", "Three days later, you are standing at the hospital billing counter at nine o'clock at night. The discharge papers are ready. Your bill is four point five lakh rupees.", "H004", ""),
 ("E005", C1, "", "And the desk clerk looks up at you and hands you a printed letter saying, Sorry sir, your cashless claim was rejected by the T-P-A due to non-disclosure of a pre-existing disease.", "H005", ""),
 ("E006", C1, "[sigh]", "Your heart drops. Your family panics.", "H006", ""),
 ("E007", C1, "", "It's night time, the banks are closed, and you are forced to break your fixed deposits, borrow from relatives, or swipe an emergency credit card just to get your loved one out of the hospital.", "H007", ""),
 ("E008", C1, "", "And you wonder, why did I pay insurance all these years if they abandon me the moment I need them?", "H008", ""),
 # FIX 1: 'a legal rule that makes most of these rejections completely illegal' (no source for 'most')
 ("E009", C1, "[pause]", "What your insurance agent never told you... is that under official regulations in India, there is a legal rule that makes this exact rejection illegal, once your policy has crossed five years.", "H009", ""),
 ("E010", C1, "", "Welcome to Be Practical with Kishore.", "H010", ""),
 # FIX 2: '... get your money back within sixty days' (no source; Ombudsman: 8 in 10 closed within three months)
 ("E011", C1, "", "In this video, we are not going to shout, and we are not going to promote any insurance policies. Today, let's look at the real I-R-D-A-I rules, see who really says no, and learn the step-by-step way to get your money back.", "H011", ""),
 ("E012", C1, "", "Let's break it down... in plain, simple English.", "H012", ""),

 ("E013", C2, "", "First... who actually says no to you at the hospital desk?", "H013", ""),
 ("E014", C2, "", "Most people think it's the insurance company sitting there evaluating your medical reports. But in reality, it's a middleman called a T-P-A... Third Party Administrator.", "H014", ""),
 # FIX 3: 'a private corporate agency' (one TPA is owned by state insurers) + 'let's be honest about corporate incentives'
 ("E015", C2, "", "Many think a T-P-A is a neutral government doctor. It is not. A T-P-A is a company hired and paid by the insurance company to process medical bills.", "H015", ""),
 # FIX 4: 'their default reaction ... automated query or a quick cashless denial letter' (no source) -> IRDAI 2024-25 data
 ("E016", C2, "", "In India, about seven out of every ten health claims are settled through T-P-As.", "H016", ""),
 ("E017", C2, "", "Under I-R-D-A-I rules, no claim can be rejected without the approval of the insurance company's own claims review committee. But here are the three excuses you will often see on these letters.", "H017", ""),
 ("E018", C2, "", "Excuse Number One. Non-disclosure of pre-existing condition.", "H020", ""),
 ("E019", C2, "", "Suppose you were admitted for a broken leg or dengue. A junior doctor writes one line in your notes. Patient has mild blood pressure.", "H021", ""),
 ("E020", C2, "", "The reviewer sees that one line. He opens your proposal form from five years ago, and says... You didn't declare blood pressure. Cashless denied.", "H022", ""),
 # FIX 5: 'But they use it anyway to deny your payout' (in the first five years non-disclosure is a lawful ground)
 ("E021", C2, "", "Wait... does blood pressure cause a broken leg or a dengue infection? Of course not. But in the first five years of your policy, the company can still use it. After five years, the rule changes.", "H023", ""),
 ("E022", C2, "", "Excuse Number Two. Not medically necessary. They say your treatment could have been done as an outpatient visit without staying in hospital.", "H024", ""),
 ("E023", C2, "", "And Excuse Number Three. Room rent limit, and proportionate deduction.", "H025", ""),
 ("E024", C2, "", "Say your policy allows a room of five thousand rupees a day, but you took an eight thousand rupee room. They don't just deduct the three thousand rupee difference.", "H026", ""),
 # FIX 6: 'a cut of about thirty-seven percent across your entire bill' (only room-linked charges; medicines are exempt)
 ("E025", C2, "", "They pay only five out of every eight rupees... on the surgery, doctor, and nursing charges too. That is a cut of about thirty-seven percent on those charges.", "H027", ""),
 ("E026", C2, "[sigh]", "When a family sees that technical rejection letter, they feel completely helpless. They think the door is closed forever.", "H029", ""),
 ("E027", C2, "", "It is not. A cashless denial... is NOT a claim rejection. Your legal right to the money is still alive.", "H018", ""),

 ("E028", C3, "", "Now listen carefully. This may be the single most important rule in Indian health insurance.", "H031", ""),
 ("E029", C3, "", "It is called the moratorium period.", "H032", ""),
 ("E030", C3, "", "Earlier, this period was eight years. But in twenty twenty-four, the I-R-D-A-I brought it down from eight years to five years.", "H033", ""),
 ("E031", C3, "", "That means sixty continuous months in a row, with no break in your policy.", "H034", ""),
 ("E032", C3, "", "So, what does it mean for you?", "H035", ""),
 # FIX 7: '... on grounds of non-disclosure or pre-existing diseases' (the moratorium covers non-disclosure and misrepresentation)
 ("E033", C3, "[pause]", "After five years of continuous cover, the insurance company legally CANNOT question your policy or your claim on grounds of non-disclosure, like an old disease you did not mention.", "H036", ""),
 ("E034", C3, "", "Read that again. After five years, an old health history cannot be used as an excuse.", "H037", ""),
 # FIX 8: 'proven criminal fraud that the company has to establish in court' (the clause says 'established fraud'; no court)
 ("E035", C3, "", "There is only one single exception. Proven fraud that the company has to establish. Not a forgotten fever, not an undiagnosed ache... active, deliberate fraud.", "H038", ""),
 ("E036", C3, "", "Your normal policy limits still apply, and if you port your policy to another insurer, your years move with you. If you cancel and buy a new one, the count resets to zero.", "H039", ""),
 ("E037", C3, "", "Now think about our family at the billing counter. Six years of continuous policy. A letter that says non-disclosure. That excuse directly violates the I-R-D-A-I rule.", "H040", ""),
 ("E038", C3, "", "And there is one more rule... a clock.", "H041", ""),
 # FIX 9: 'officially uploads the complete final discharge bill ... within exactly three hours' (circular: receipt of the discharge request)
 ("E039", C3, "", "When the hospital sends the final discharge request to the insurance company, the company must give final approval within three hours.", "H042", ""),
 # FIX 10: 'any extra room rent' -> 'any extra amount' (circular: 'the additional amount if any charged by the hospital')
 ("E040", C3, "", "I-R-D-A-I mandates that the patient should not be made to wait. If the approval comes later than three hours, any extra amount the hospital charges for that delay is paid by the insurance company from its own funds... not by you.", "H043", ""),
 ("E041", C3, "", "Remember this rule, and ask for it at the discharge counter.", "H044", ""),

 ("E042", C4, "", "So, what should you do if your cashless is denied at the counter tonight?", "H045", ""),
 ("E043", C4, "", "Do not shout at hospital staff. Do not panic. Follow these four steps.", "H046", ""),
 ("E044", C4, "", "Step One. Collect your papers before you leave.", "H047", ""),
 ("E045", C4, "", "If you have to pay the bill yourself, pay it. But before leaving the hospital, ask for copies of the discharge summary, the final itemized bill, all test reports, pharmacy receipts, and the written cashless denial letter.", "H049", ""),
 ("E046", C4, "", "If they claimed admission was not needed, ask your treating doctor for a short clinical justification certificate.", "H050", ""),
 ("E047", C4, "", "Step Two. File for reimbursement within fifteen to thirty days.", "H051", ""),
 # FIX 11: 'Principal Nodal Officer, the P-N-O' (not an insurance title; IRDAI names the Grievance Redressal Officer)
 #         + quote the moratorium only when the policy has crossed five years
 ("E048", C4, "", "If they reject it, write a calm, formal email to the company's Grievance Redressal Officer. State your policy number, claim number and amount, and if your policy has crossed five years, quote the I-R-D-A-I five-year moratorium rule. The company must reply within fourteen days.", "H052", ""),
 ("E049", C4, "", "Step Three. Register on Bima Bharosa.", "H054", ""),
 # FIX 12: 'tracked directly by government authorities' -> by the regulator
 ("E050", C4, "", "If the company ignores you or sends the same generic rejection, go to Bima Bharosa dot I-R-D-A-I dot gov dot in. This is the regulator's own portal, and complaints filed here are tracked directly by the I-R-D-A-I.", "H055", ""),
 ("E051", C4, "", "And Step Four. The Insurance Ombudsman.", "H056", ""),
 # FIX 13: 'do NOT go to a consumer court, and do NOT hire an expensive lawyer' (consumer court stays a valid option)
 ("E052", C4, "", "If the company still refuses after thirty days, you do NOT need a consumer court case, and you do NOT need an expensive lawyer.", "H057", ""),
 ("E053", C4, "", "Go to the official website, c-i-o-i-n-s dot co dot in.", "H058", ""),
 ("E054", C4, "", "The Insurance Ombudsman is a government body set up specifically to resolve insurance disputes. You can file online. It costs zero rupees. You do not need a lawyer.", "H060", ""),
 # FIX 14: 'the Ombudsman resolved over thirty-two thousand' (32,503 were received; 29,017 disposed)
 ("E055", C4, "", "In the financial year twenty twenty-four to twenty-five, the Ombudsman offices received over thirty-two thousand health complaints. Over seventy-five percent of decided cases went in favor of the policyholder. And eight out of ten complaints were closed within three months.", "H061", "Cut to H062 BOARD (76%) and H063 bar inside this line"),
 ("E056", C4, "", "The Ombudsman can award up to fifty lakh rupees, and the award is legally binding on the insurance company.", "H064", ""),
 ("E057", C4, "", "Finally... how do you prevent this before you even buy?", "H067", ""),
 ("E058", C4, "", "Rule One. Disclose everything in writing on the proposal form. If you smoke or take mild B-P medication, declare it. Once it's on paper, they can never call it non-disclosure.", "H070", ""),
 # FIX 15: 'Saving two thousand rupees on a policy with a room limit can cost you sixty thousand' (no source for the saving)
 ("E059", C4, "", "Rule Two. Choose a policy with No Room Rent Capping. In our example, one bigger room cost almost sixty thousand rupees through proportionate cuts.", "H073", ""),
 # FIX 16: 'can be five to fifteen percent ... An add-on cover of five hundred to eight hundred rupees covers them completely'
 #         (estimates vary, so attribute; no source for the price; riders have caps, e.g. New India: ₹1,500 a year, up to ₹15,000)
 ("E060", C4, "", "Rule Three. Ask about a Consumables Cover. Reports say gloves, masks, and syringes can be five to fifteen percent of a hospital bill. Some insurers sell an add-on cover for this. Check its price and its limit before you buy.", "H075", ""),
 ("E061", C4, "[slight smile]", "Remember, you pay for insurance so your family has peace of mind. Know the five-year rule. Use the Ombudsman. And protect your hard-earned savings.", "H077", ""),
 ("E062", C4, "", "Be smart. Be informed. And always... be practical.", "H078", ""),
 ("E063", C4, "", "If this helped you, share it with a family member who has health insurance, subscribe to Be Practical with Kishore, and ask your questions below.", "H079", ""),
 ("E064", C4, "", "I'll see you next time.", "H080", ""),
]

with open(HERE / "script.full.tsv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["id", "section", "te", "en", "emotion", "visual", "onscreen", "sound", "pacing"])
    for i, sec, emo, en, ref, note in R:
        b = v1[ref]
        pac = "; ".join(x for x in (b["pacing"], note) if x)
        w.writerow([i, sec, "", en, emo, f"[v1 {ref}] " + b["visual"], b["onscreen"], b["sound"], pac])
print(len(R), "rows")
