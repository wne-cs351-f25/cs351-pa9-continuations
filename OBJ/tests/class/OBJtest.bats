#!/usr/bin/env bats

load '../../../../bin/relocate.bash'

@test "OBJ class" {
  relocate
  plccmk -c grammar > /dev/null
  RESULT="$(rep -n < ./tests/class/OBJ.input)"

  expected_output=$(< "./tests/class/OBJ.expected")
  [[ "$RESULT" == "$expected_output" ]]

}
