import datetime
import xml.etree.ElementTree as ET

def generate_pain001_from_result(result: dict) -> str:
    ns = "urn:iso:std:iso:20022:tech:xsd:pain.001.001.03"
    doc = ET.Element("Document", xmlns=ns)
    ccti = ET.SubElement(doc, "CstmrCdtTrfInitn")
    grp = ET.SubElement(ccti, "GrpHdr")
    ET.SubElement(grp, "MsgId").text = result.get("proof_id","zkorigo-msg")
    ET.SubElement(grp, "CreDtTm").text = result.get("timestamp", datetime.datetime.utcnow().isoformat()+"Z")
    ET.SubElement(grp, "NbOfTxs").text = "1"
    ET.SubElement(grp, "CtrlSum").text = "0.00"

    pmtinf = ET.SubElement(ccti, "PmtInf")
    ET.SubElement(pmtinf, "PmtInfId").text = result.get("proof_id","zkorigo")+"-pmt"
    ET.SubElement(pmtinf, "PmtMtd").text = "TRF"

    cdt = ET.SubElement(pmtinf, "CdtTrfTxInf")
    pmtid = ET.SubElement(cdt, "PmtId")
    ET.SubElement(pmtid, "InstrId").text = result.get("proof_id")+"-instr"
    ET.SubElement(pmtid, "EndToEndId").text = result.get("wallet","unknown")

    amt = ET.SubElement(cdt, "Amt")
    inamt = ET.SubElement(amt, "InstdAmt", Ccy="USD")
    inamt.text = "0.00"

    dbtr = ET.SubElement(cdt, "Dbtr")
    ET.SubElement(dbtr, "Nm").text = "Wallet_" + result.get("wallet","unknown")[:8]

    cdtr = ET.SubElement(cdt, "Cdtr")
    ET.SubElement(cdtr, "Nm").text = "zkOrigoRecipient"

    rmt = ET.SubElement(cdt, "RmtInf")
    ET.SubElement(rmt, "Ustrd").text = f"AI Risk Score: {result.get('risk_score')} - {', '.join(result.get('ai_reason',[]))}"

    return ET.tostring(doc, encoding="utf-8", method="xml").decode("utf-8")
