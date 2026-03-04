.PHONY: help audit verify sync-answers verify-report

PYTHON ?= python3
YEAR ?=
TIMEOUT ?= 240

help:
	@echo "Common commands:"
	@echo "  make audit                         # static consistency audit"
	@echo "  make verify                        # verify all accepted answers"
	@echo "  make verify YEAR=2025              # verify one year"
	@echo "  make verify TIMEOUT=300            # override per-script timeout"
	@echo "  make sync-answers                  # regenerate accepted_answers.json"
	@echo "  make verify-report                 # run full verify + audit"

audit:
	$(PYTHON) -m aoclib audit

verify:
	@if [ -n "$(YEAR)" ]; then \
		$(PYTHON) -m aoclib verify --year $(YEAR) --timeout $(TIMEOUT); \
	else \
		$(PYTHON) -m aoclib verify --timeout $(TIMEOUT); \
	fi

sync-answers:
	$(PYTHON) -m aoclib sync-answers

verify-report: verify audit
	@echo "Verification and audit completed. See tools/VERIFICATION_REPORT.md for latest snapshot format."
