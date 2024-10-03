
from dynamic.dynamic_accounts.report.accounts_receivables.accounts_receivables import ReceivablePayableReport


def execute(filters=None):
    args = {
        "party_type": "Supplier",
        "naming_by": ["Buying Settings", "supp_master_name"],
    }
    return ReceivablePayableReport(filters).run(args)
