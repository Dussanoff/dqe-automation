import pytest
import re
"""
1. Write tests to validate the content of the CSV file:
Validate that file is not empty.
Validate the schema of the file (id, name, age, email).
Validate that the age column contains valid values (0-100).
Validate that the email column contains valid email addresses (format).
Validate there are no duplicate rows.
Validate that:is_active=False for id=1, is_active=True for id=2.
Same as previous one for id = 2, but without parametriz mark. 
•	Use custom error messages in assertions.

2. Use PyTest Hooks:
•	Implement a hook in conftest.py to dynamically mark tests that do not have explicit marks. The hook should assign tests without marks to a custom mark:unmarked.

3. Create fixtures in conftest.py:
•	A fixture to read the CSV file and return its content. Parameters: path_to_file.
•	A fixture to validate the schema of the file. Parameters: actual_schema, expected_schema.
•	Fixtures scope: session.

4. Use Custom and Predefined Marks:
•	Use predefined marks @pytest.mark.parametrize, @pytest.mark.skip, @pytest.mark.xfail and create custom marks.

5. Populate the pytest.ini file with custom marks and modify test discovery settings to only look for files prefixed with test_.
6. Configure PyTest to generate an HTML report upon test execution.
"""

def test_file_not_empty(file):#1                                            ready
    #print(file)
    assert not file.empty, "The CSV file must not be empty"


@pytest.mark.validate_csv
@pytest.mark.xfail(reason="xfail")
def test_duplicates(list_of_dict):#5                                        ready
    list_as_tuples = [tuple(d.items()) for d in list_of_dict]
    unique_items = set(list_as_tuples)
    assert len(unique_items) == len(list_of_dict), "Duplicate rows detected in the CSV file"


@pytest.mark.validate_csv
def test_validate_schema(list_of_dict, schema):#2                           ready
    schema()


@pytest.mark.validate_csv
@pytest.mark.skip(reason="skip")
def test_age_column_valid(list_of_dict):#3                                  ready
    for record in list_of_dict:
        age = record.get("age")
        assert 0 <= age <= 100


@pytest.mark.validate_csv
def test_email_column_valid(list_of_dict):#4                                ready
    for record in list_of_dict:
        email = record.get("email")
        #print(email)
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        assert re.fullmatch(pattern, email) is not None, f"Invalid email format: {email}"


@pytest.mark.parametrize("id, is_active", [(1, False), (2, True)])
def test_active_players(list_of_dict, id, is_active):#6                     ready
    assert active_payer_check(list_of_dict, id, is_active), f"Incorrect 'is_active' value for id={id}. Expected {is_active}."


def test_active_player(list_of_dict, players_data):#7                       ready
    for params in players_data:
        id, is_active = params
        assert active_payer_check(list_of_dict, id, is_active), f"Incorrect 'is_active' value for id={id}. Expected {is_active}."


def active_payer_check(list, id, is_active):
    for record in list:
        record_id = record.get("id")
        record_is_active = record.get("is_active")
        if record_id == id:
            return record_is_active == is_active
