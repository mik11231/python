.PHONY: help audit lint-style lint-style-strict verify sync-answers verify-report

PYTHON ?= python3
YEAR ?=
TIMEOUT ?= 240

help:
	@echo "Common commands:"
	@echo "  make audit                         # static consistency audit"
	@echo "  make lint-style                    # lightweight style/convention linter (YEAR=2022 optional)"
	@echo "  make lint-style-strict             # fail on warnings too (YEAR=2022 optional)"
	@echo "  make verify                        # verify all accepted answers"
	@echo "  make verify YEAR=2025              # verify one year"
	@echo "  make verify TIMEOUT=300            # override per-script timeout"
	@echo "  make sync-answers                  # regenerate accepted_answers.json"
	@echo "  make verify-report                 # run full verify + audit + style lint"

audit:
	$(PYTHON) -m aoclib audit

lint-style:
	@if [ -n "$(YEAR)" ]; then \
		$(PYTHON) -m aoclib lint-style --year $(YEAR); \
	else \
		$(PYTHON) -m aoclib lint-style; \
	fi

lint-style-strict:
	@if [ -n "$(YEAR)" ]; then \
		$(PYTHON) -m aoclib lint-style --strict --year $(YEAR); \
	else \
		$(PYTHON) -m aoclib lint-style --strict; \
	fi

verify:
	@if [ -n "$(YEAR)" ]; then \
		$(PYTHON) -m aoclib verify --year $(YEAR) --timeout $(TIMEOUT); \
	else \
		$(PYTHON) -m aoclib verify --timeout $(TIMEOUT); \
	fi

sync-answers:
	$(PYTHON) -m aoclib sync-answers

verify-report: verify audit lint-style-strict
	@echo "Verification and audit completed. See tools/VERIFICATION_REPORT.md for latest snapshot format."
