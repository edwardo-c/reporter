def external_email(brand: str) -> str:
    return (
        f"<html><body>"
        f"<p><h3>Attached is your monthly <b>{brand}</b> price list.</h3></p>"
        f"<p>If you would like to be removed from, or add someone to, our distribution list, please reply to this email.</p>"
        f"<p>See the <b>Updates</b> tab for any changes from last month’s list.</p>"
        f"<p>- {brand} Sales Team</p>"
        f"</body></html>"
    )

def external_nep_email() -> str:
    return (
        f"<html><body>"
        f"<p><h3>Attached is your monthly Neptune price list.</h3></p>"
        f"<p>Neptune 65in. Full Sun is <strong>OUT OF STOCK</strong>. Stay tuned for additional information on <strong>NEW</strong> High Bright Full Sun Models.</p>"
        f"<p>If you would like to be removed from, or add someone to, our distribution list, please reply to this email.</p>"
        f"<p>See the <b>Updates</b> tab for any changes from last month’s list.</p>"
        f"<p>- Neptune Sales Team</p>"
        f"</body></html>"
    )

def internal_email(id: str) -> str:
    return (
        f"<html><body>"
        f"<p>The monthly price list for <b>{id}</b> has been created and posted to peernet.</p>"
        f"<p>This price list has NOT been delivered to the customer because the 'Pricelist Delivery To Salesperson' is filled in Salesforce</p>"
        f"<p>You are responsible for delivery of this price list to your customer</p>"
        f"<p>If you would like to change this, ensure a valid contact exists in Salesforce under the account record and leave 'Pricelist Delivery To Salesperson' blank</p>"
        f"<p>Let us know if you have any questions</p>"
        f"<p>- Sales Ops</p>"
        f"</body></html>"
    )

def correction_email() -> str:
    return (
        f"<html><body>"
        f"<p><h3>Attached is a remake of your monthly Peerless-AV price list.</h3></p>"
        f"<p>There was an error on the previous list that made discontinued parts appear active, specifically the XHB754</p>"
        f"<p>XHB754 is <strong>not</strong> available</p>"
        f"<p>Sorry for the duplicate email and any confusion this may have caused</p>"
        f"<p>- Peerless-AV Sales Ops Team</p>"
        f"</body></html>"
    )
