
TESTS := \
	test_key_value_database \
	test_collection_database \
	test_key_value_volatile_database \
	test_environment \
	test_workspace \
	test_task \
	test_requirements \

all: tests

tests: ${TESTS}

test_%:
	python3 -m unittest $@
