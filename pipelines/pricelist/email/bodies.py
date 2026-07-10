def external_email(brand: str) -> str:
    return (
        f"<html><body>"
        f"<p><h3>Attached is your monthly <b>{brand}</b> price list.</h3></p>"
        f"<p>If you would like to be removed from, or add someone to, our distribution list, please reply to this email.</p>"
        f"<p>See the <b>Updates</b> tab for any changes from last month’s list.</p>"
        f"<p>- {brand} Sales Team</p>"
        f"</body></html>"
    )

def internal_email(id: str) -> str:
    return (
        f"<html><body>"
        f"<p>The monthly price list for <b>{id}</b> has been created and posted to peernet.</p>"
        f"<p>This price list has NOT been delivered to the customer because the 'Pricelist Delivery To Salesperson' is filled in Salesforce</p>"
        f"<p>You are responsible for delivery of this price list to your customer</p>"
        f"<p>If you would like to change this, ensure a valid contact exists in Salesforce under the account record and leave 'Pricelist Delivery To Salesperson' blank</p>"
        f"<p>Once sent, please log the email in salesforce to maintain an audit trail</p>"
        f"<p>Let us know if you have any questions</p>"
        f"<p>- Sales Ops</p>"
        f"</body></html>"
    )

def external_boilerplate_email(brand: str):
    return (
        f"<html><body>"
        f"<p><strong>Attached is your monthly {brand} price list.</strong></p>"
        f"<p>Each month, regardless if there are any price changes, these will be distributed at or near the 1st business day of the month.</p>"
        f"<p>See the Updates tab for any changes from last month’s list.</p>"
        f"<p>All End of Life, New Products or Pricing Changes will be called out each month. Here is a legend on how you will find each.</p>"
        f"<p><span style='background-color: red; color: white'>End Of Life (EOL)</span> are on the <span style='background-color: red; color: white'>Red</span> tab.</p>"
        f"<p><span style='background-color: #31FF21;'>New Products</span> will be highlighted on the price list tab in <span style='background-color: #31FF21;'>Green.</span> tab.</p>"
        f"<p><span style='background-color: yellow;'>Price Changes</span> will be highlighted on the price list tab in <span style='background-color: yellow;'>Yellow.</span> tab.</p>"
        f"<p><i><span style='color: #0070C0;'>If you would like to be removed from, or add another recipient to, our distribution list, please reply to this email.</span></i></p>"
        f"</body></html>"
    )

def external_price_increase_email_body(brand: str):
    return (
        f"<html><body>"
        f"<p><strong>Attached is your monthly {brand} price list.</strong></p>"
        f"<p>Pricing reflects adjustments made due to increased expenses.  Prices are in effect beginning July 1, 2026</p>"
        f"<p>All End of Life, New Products or Pricing Changes will be called out each month. Here is a legend on how you will find each.</p>"
        f"<p><span style='background-color: red; color: white'>End Of Life (EOL)</span> are on the <span style='background-color: red; color: white'>Red</span> tab.</p>"
        f"<p><span style='background-color: #31FF21;'>New Products</span> will be highlighted on the price list tab in <span style='background-color: #31FF21;'>Green.</span> tab.</p>"
        f"<p><span style='background-color: yellow;'>Price Changes</span> will be highlighted on the price list tab in <span style='background-color: yellow;'>Yellow.</span> tab.</p>"
        f"<p><i><span style='color: #0070C0;'>If you would like to be removed from, or add another recipient to, our distribution list, please reply to this email.</span></i></p>"
        f"</body></html>"
    )