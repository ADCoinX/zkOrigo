import datetime
import xml.etree.ElementTree as ET

def generate_pain001_from_result(result: dict) -> str:
    # Minimal pain.001 structure for MVP - includes AI risk in <Ustrd>
    msg_id = result.get("proof_id","zkorigo-msg") if result.get("proof_id") else "zkorigo-msg"
    cre_dt = result.get("timestamp", datetime.datetime.utcnow().isoformat() + "Z")
    # root
    ns = "urn:iso:std:iso:20022:tech:xsd:pain.001.001.03"
    doc = ET.Element("Document", xmlns=ns)
    ccti = ET.SubElement(doc, "CstmrCdtTrfInitn")
    grp = ET.SubElement(ccti, "GrpHdr")
    ET.SubElement(grp, "MsgId").text = msg_id
    ET.SubElement(grp, "CreDtTm").text = cre_dt
    ET.SubElement(grp, "NbOfTxs").text = "1"
    ET.SubElement(grp, "CtrlSum").text = "0.00"

    pmtinf = ET.SubElement(ccti, "PmtInf")
    ET.SubElement(pmtinf, "PmtInfId").text = msg_id + "-pmt"
    ET.SubElement(pmtinf, "PmtMtd").text = "TRF"
    cdt = ET.SubElement(pmtinf, "CdtTrfTxInf")
    pmtid = ET.SubElement(cdt, "PmtId")
    ET.SubElement(pmtid, "InstrId").text = msg_id + "-instr"
    ET.SubElement(pmtid, "EndToEndId").text = result.get("wallet","unknown")

    amt = ET.SubElement(cdt, "Amt")
    inamt = ET.SubElement(amt, "InstdAmt", Ccy=result.get("currency","USD"))
    inamt.text = str(result.get("amount","0.00"))

    dbtr = ET.SubElement(cdt, "Dbtr")
    ET.SubElement(dbtr, "Nm").text = "Wallet_" + result.get("wallet","unknown")[:8]
    acct = ET.SubElement(dbtr, "Acct")
    idd = ET.SubElement(acct, "Id")
    ET.SubElement(idd, "IBAN").text = result.get("wallet","unknown")

    cdtr = ET.SubElement(cdt, "Cdtr")
    ET.SubElement(cdtr, "Nm").text = "zkOrigoRecipient"
    acct2 = ET.SubElement(cdtr, "Acct")
    idd2 = ET.SubElement(acct2, "Id")
    ET.SubElement(idd2, "IBAN").text = "recipient-placeholder"

    rmt = ET.SubElement(cdt, "RmtInf")
    ustrd = "AI Risk Score: {} - {}".format(result.get("risk_score"), "; ".join(result.get("ai_reason",[])))
    ET.SubElement(rmt, "Ustrd").text = ustrd

    # pretty string
    xml_str = ET.tostring(doc, encoding="utf-8", method="xml")
    return xml_str.decode("utf-8")
