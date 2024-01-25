
TESTS := \
	test_key_value_database \
	test_collection_database \
	test_key_value_volatile_database \
	test_environment \
	test_workspace \
	test_task \
	test_requirements \
	test_git_tools \
	test_db_tools \

all: tests

tests: ${TESTS}

test_%:
	python3 -m unittest $@
