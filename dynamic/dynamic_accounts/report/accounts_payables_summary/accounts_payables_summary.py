from dynamic.dynamic_accounts.report.accounts_receivables_summary.accounts_receivables_summary import (
	AccountsReceivableSummary,
)


def execute(filters=None):
	args = {
		"party_type": "Supplier",
		"naming_by": ["Buying Settings", "supp_master_name"],
	}
	return AccountsReceivableSummary(filters).run(args)