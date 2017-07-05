
SHELL=/bin/bash
VIRTUALENV=.virtualenv

FUNCTION=townclock-chime
SOURCE=lambda_function.py
ZIPFILE=lambda_function.zip

help: ## Show help text
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-10s %s\n", $$1, $$2}'

$(VIRTUALENV)/bin/activate:
	virtualenv --python $$(which python3.6) $(VIRTUALENV)
	source $(VIRTUALENV)/bin/activate; \
	pip install boto3

virtualenv:: $(VIRTUALENV)/bin/activate

setup:: ## Install development prerequisites and virtualenv
	sudo apt-get install python3.6
	sudo -H pip3 install virtualenv

setup:: virtualenv

$(ZIPFILE): $(SOURCE)
	zip --filesync $@ $^

deploy:: $(ZIPFILE) ## Deploy updated function code to existing AWS Lambda
	for region in us-east-1 us-west-2; do \
	  echo -n -e "$$region SNS topic: "; \
	  aws lambda update-function-code \
	    --region "$$region" \
	    --function-name "$(FUNCTION)" \
	    --zip-file "fileb://$(ZIPFILE)" \
	    --output text \
	    --query '[Environment.Variables.sns_topic_arn]'; \
	done

test:: ## Run in local dev environment
	source $(VIRTUALENV)/bin/activate; \
	./lambda_function.py

clean:: ## Cleanup local directory
	rm -rf $(VIRTUALENV)
